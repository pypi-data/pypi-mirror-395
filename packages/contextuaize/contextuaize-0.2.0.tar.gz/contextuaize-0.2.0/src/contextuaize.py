#!/usr/bin/env python3
"""
Contextuaize - Smart codebase context extraction for LLMs

Features:
- Respects .gitignore by default
- Minimal universal exclusions
- Optional LLM-powered smart filtering (--smart)
- Query-driven context selection (--query)
- Smart summarization for large files
- Dependency-aware crawling
"""

import os
import sys
import argparse
import fnmatch
import subprocess
import json
import mimetypes
from pathlib import Path
from typing import Set, List, Dict, Optional, Tuple
from dataclasses import dataclass, field

# =============================================================================
# Configuration
# =============================================================================

# Minimal universal exclusions - things that are NEVER useful context
ALWAYS_IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                       '.tox', '.nox', '.mypy_cache', '.pytest_cache', '.ruff_cache',
                       '.eggs', '*.egg-info', '.cache'}

ALWAYS_IGNORE_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 
                        'poetry.lock', 'Pipfile.lock', 'composer.lock',
                        '.DS_Store', 'Thumbs.db', '*.pyc', '*.pyo'}

# Binary extensions to skip (not useful as text context)
BINARY_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.webp', '.svg',
                     '.woff', '.woff2', '.ttf', '.eot', '.otf',
                     '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                     '.zip', '.tar', '.gz', '.rar', '.7z',
                     '.exe', '.dll', '.so', '.dylib',
                     '.mp3', '.mp4', '.wav', '.avi', '.mov',
                     '.sqlite', '.db', '.pickle', '.pkl'}

# Default output filename
DEFAULT_OUTPUT = 'codebase_context.txt'

# Output modes
OUTPUT_FILE = 'file'
OUTPUT_CLIPBOARD = 'clipboard'
OUTPUT_STDOUT = 'stdout'

# Size thresholds
MAX_FILE_SIZE = 100 * 1024  # 100KB - files larger than this get summarized in smart mode
LARGE_FILE_THRESHOLD = 50 * 1024  # 50KB - warn about large files

# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class FileInfo:
    """Information about a file in the codebase."""
    path: str
    relative_path: str
    size: int
    extension: str
    content: Optional[str] = None
    summary: Optional[str] = None
    imports: List[str] = field(default_factory=list)
    relevance_score: float = 1.0

@dataclass 
class ProjectStructure:
    """Represents the project's file structure."""
    root: str
    files: List[FileInfo] = field(default_factory=list)
    tree: str = ""
    detected_stack: List[str] = field(default_factory=list)

# =============================================================================
# Gitignore Parser
# =============================================================================

class GitignoreParser:
    """Parse and apply .gitignore rules."""
    
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.patterns: List[Tuple[str, bool]] = []  # (pattern, is_negation)
        self._load_gitignore()
    
    def _load_gitignore(self):
        """Load .gitignore file if it exists."""
        gitignore_path = os.path.join(self.root_dir, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        is_negation = line.startswith('!')
                        pattern = line[1:] if is_negation else line
                        self.patterns.append((pattern, is_negation))
    
    def is_ignored(self, path: str) -> bool:
        """Check if a path should be ignored based on .gitignore rules."""
        relative = os.path.relpath(path, self.root_dir)
        ignored = False
        
        for pattern, is_negation in self.patterns:
            if self._matches(relative, pattern):
                ignored = not is_negation
        
        return ignored
    
    def _matches(self, path: str, pattern: str) -> bool:
        """Check if path matches a gitignore pattern."""
        # Handle directory patterns (ending with /)
        if pattern.endswith('/'):
            pattern = pattern[:-1]
            parts = path.split(os.sep)
            return any(fnmatch.fnmatch(part, pattern) for part in parts)
        
        # Handle patterns with /
        if '/' in pattern:
            return fnmatch.fnmatch(path, pattern)
        
        # Handle simple patterns - match against any path component
        parts = path.split(os.sep)
        return any(fnmatch.fnmatch(part, pattern) for part in parts) or fnmatch.fnmatch(path, pattern)

# =============================================================================
# File Scanner
# =============================================================================

class FileScanner:
    """Scan and filter files from a codebase."""
    
    def __init__(self, root_dir: str, respect_gitignore: bool = True,
                 include_patterns: List[str] = None, exclude_patterns: List[str] = None):
        self.root_dir = os.path.abspath(root_dir)
        self.respect_gitignore = respect_gitignore
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
        self.gitignore = GitignoreParser(root_dir) if respect_gitignore else None
    
    def scan(self) -> ProjectStructure:
        """Scan the directory and return project structure."""
        project = ProjectStructure(root=self.root_dir)
        project.tree = self._generate_tree()
        
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # Filter directories in-place
            dirnames[:] = [d for d in dirnames if not self._should_ignore_dir(d, dirpath)]
            
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, self.root_dir)
                
                if self._should_include_file(filename, full_path, relative_path):
                    _, ext = os.path.splitext(filename)
                    try:
                        size = os.path.getsize(full_path)
                    except OSError:
                        continue
                    
                    file_info = FileInfo(
                        path=full_path,
                        relative_path=relative_path,
                        size=size,
                        extension=ext.lower()
                    )
                    project.files.append(file_info)
        
        project.detected_stack = self._detect_stack(project.files)
        return project
    
    def _should_ignore_dir(self, dirname: str, dirpath: str) -> bool:
        """Check if directory should be ignored."""
        # Always ignore certain directories
        for pattern in ALWAYS_IGNORE_DIRS:
            if fnmatch.fnmatch(dirname, pattern):
                return True
        
        # Check gitignore
        if self.gitignore:
            full_path = os.path.join(dirpath, dirname)
            if self.gitignore.is_ignored(full_path):
                return True
        
        # Check custom exclude patterns
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(dirname, pattern):
                return True
        
        return False
    
    def _should_include_file(self, filename: str, full_path: str, relative_path: str) -> bool:
        """Check if file should be included."""
        # Skip always-ignored files
        for pattern in ALWAYS_IGNORE_FILES:
            if fnmatch.fnmatch(filename, pattern):
                return False
        
        # Skip binary files
        _, ext = os.path.splitext(filename)
        if ext.lower() in BINARY_EXTENSIONS:
            return False
        
        # Check gitignore
        if self.gitignore and self.gitignore.is_ignored(full_path):
            return False
        
        # Check custom exclude patterns
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(relative_path, pattern):
                return False
        
        # If include patterns specified, file must match one
        if self.include_patterns:
            matched = any(
                fnmatch.fnmatch(filename, p) or fnmatch.fnmatch(relative_path, p)
                for p in self.include_patterns
            )
            if not matched:
                return False
        
        # Check if file is text (not binary)
        if not self._is_text_file(full_path):
            return False
        
        return True
    
    def _is_text_file(self, filepath: str) -> bool:
        """Check if file is likely a text file."""
        try:
            with open(filepath, 'rb') as f:
                chunk = f.read(8192)
                # Check for null bytes (binary indicator)
                if b'\x00' in chunk:
                    return False
            return True
        except (IOError, OSError):
            return False
    
    def _generate_tree(self, max_depth: int = 4) -> str:
        """Generate a directory tree string."""
        lines = [os.path.basename(self.root_dir) + '/']
        self._tree_recursive(self.root_dir, '', lines, 0, max_depth)
        return '\n'.join(lines)
    
    def _tree_recursive(self, path: str, prefix: str, lines: List[str], depth: int, max_depth: int):
        if depth >= max_depth:
            return
        
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return
        
        # Filter entries
        dirs = []
        files = []
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                if not self._should_ignore_dir(entry, path):
                    dirs.append(entry)
            else:
                if self._should_include_file(entry, full_path, os.path.relpath(full_path, self.root_dir)):
                    files.append(entry)
        
        all_entries = dirs + files
        for i, entry in enumerate(all_entries):
            is_last = (i == len(all_entries) - 1)
            connector = '└── ' if is_last else '├── '
            
            if entry in dirs:
                lines.append(f"{prefix}{connector}{entry}/")
                new_prefix = prefix + ('    ' if is_last else '│   ')
                self._tree_recursive(os.path.join(path, entry), new_prefix, lines, depth + 1, max_depth)
            else:
                lines.append(f"{prefix}{connector}{entry}")
    
    def _detect_stack(self, files: List[FileInfo]) -> List[str]:
        """Detect the technology stack from files."""
        stack = set()
        filenames = {os.path.basename(f.path) for f in files}
        extensions = {f.extension for f in files}
        
        # Detect by config files
        if 'package.json' in filenames:
            stack.add('Node.js')
        if 'requirements.txt' in filenames or 'pyproject.toml' in filenames or 'setup.py' in filenames:
            stack.add('Python')
        if 'Cargo.toml' in filenames:
            stack.add('Rust')
        if 'go.mod' in filenames:
            stack.add('Go')
        if 'Gemfile' in filenames:
            stack.add('Ruby')
        if 'pom.xml' in filenames or 'build.gradle' in filenames:
            stack.add('Java')
        if 'Dockerfile' in filenames or 'docker-compose.yml' in filenames:
            stack.add('Docker')
        
        # Detect by extensions
        if '.tsx' in extensions or '.jsx' in extensions:
            stack.add('React')
        if '.vue' in extensions:
            stack.add('Vue')
        if '.svelte' in extensions:
            stack.add('Svelte')
        if '.ts' in extensions:
            stack.add('TypeScript')
        
        return sorted(stack)

# =============================================================================
# LLM Integration
# =============================================================================

class LLMClient:
    """Client for LLM API calls."""
    
    def __init__(self, api_key: str = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.model = model
        
        if not self.api_key:
            raise ValueError("No API key provided. Set ANTHROPIC_API_KEY or use --api-key")
    
    def complete(self, prompt: str, max_tokens: int = 4096) -> str:
        """Make a completion request to the API."""
        import urllib.request
        import urllib.error
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        data = json.dumps({
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['content'][0]['text']
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise RuntimeError(f"API error {e.code}: {error_body}")
        except Exception as e:
            raise RuntimeError(f"Request failed: {e}")

class SmartFilter:
    """LLM-powered intelligent file filtering."""
    
    def __init__(self, llm: LLMClient):
        self.llm = llm
    
    def filter_by_relevance(self, project: ProjectStructure, query: str = None) -> List[FileInfo]:
        """Use LLM to determine which files are most relevant."""
        
        # Build context about the project
        file_list = "\n".join([
            f"- {f.relative_path} ({f.size} bytes)"
            for f in project.files
        ])
        
        prompt = f"""Analyze this project structure and determine which files are essential for understanding the codebase.

PROJECT TREE:
{project.tree}

DETECTED STACK: {', '.join(project.detected_stack) if project.detected_stack else 'Unknown'}

ALL FILES:
{file_list}

{"USER TASK: " + query if query else "GOAL: General architecture understanding"}

Return a JSON object with this structure:
{{
    "essential": ["list of file paths that are ESSENTIAL - entry points, core logic, main components"],
    "important": ["list of file paths that are IMPORTANT - significant business logic, key utilities"],
    "optional": ["list of file paths that are OPTIONAL - tests, examples, configs that could help"],
    "skip": ["list of file paths to SKIP - generated files, boilerplate, redundant"]
}}

Be selective. For a typical project, essential + important should be 10-30 files max.
Focus on files that would help someone understand the architecture quickly."""

        response = self.llm.complete(prompt)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            result = json.loads(response[json_start:json_end])
            
            # Map relevance scores
            path_to_file = {f.relative_path: f for f in project.files}
            filtered = []
            
            for path in result.get('essential', []):
                if path in path_to_file:
                    path_to_file[path].relevance_score = 1.0
                    filtered.append(path_to_file[path])
            
            for path in result.get('important', []):
                if path in path_to_file:
                    path_to_file[path].relevance_score = 0.7
                    filtered.append(path_to_file[path])
            
            for path in result.get('optional', []):
                if path in path_to_file:
                    path_to_file[path].relevance_score = 0.4
                    filtered.append(path_to_file[path])
            
            return filtered
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not parse LLM response, using all files. Error: {e}")
            return project.files
    
    def summarize_large_file(self, file_info: FileInfo) -> str:
        """Generate a concise summary of a large file."""
        content = file_info.content or self._read_file(file_info.path)
        
        # Truncate for API limits
        truncated = content[:30000] if len(content) > 30000 else content
        
        prompt = f"""Summarize this code file concisely. Focus on:
1. What this file does (purpose)
2. Key classes/functions and their roles
3. Important dependencies/imports
4. How it fits in the larger system

FILE: {file_info.relative_path}
CONTENT:
```
{truncated}
```

Provide a summary in 50-150 lines that captures the essential logic. Include key function signatures."""

        return self.llm.complete(prompt, max_tokens=2000)
    
    def _read_file(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {e}]"

# =============================================================================
# Import Parser (for dependency-aware crawling)
# =============================================================================

class ImportParser:
    """Parse imports from various languages to understand dependencies."""
    
    @staticmethod
    def parse_imports(filepath: str, content: str) -> List[str]:
        """Extract import statements from file content."""
        imports = []
        ext = os.path.splitext(filepath)[1].lower()
        
        lines = content.split('\n')
        
        if ext == '.py':
            for line in lines:
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.append(line)
        
        elif ext in {'.js', '.jsx', '.ts', '.tsx'}:
            for line in lines:
                line = line.strip()
                if line.startswith('import ') or (line.startswith('const ') and 'require(' in line):
                    imports.append(line)
        
        elif ext == '.go':
            in_import_block = False
            for line in lines:
                line = line.strip()
                if line.startswith('import ('):
                    in_import_block = True
                elif in_import_block and line == ')':
                    in_import_block = False
                elif in_import_block or line.startswith('import '):
                    imports.append(line)
        
        elif ext == '.rs':
            for line in lines:
                line = line.strip()
                if line.startswith('use ') or line.startswith('mod '):
                    imports.append(line)
        
        return imports

# =============================================================================
# Context Builder
# =============================================================================

class ContextBuilder:
    """Build the final context output."""
    
    def __init__(self, smart_mode: bool = False, llm: LLMClient = None):
        self.smart_mode = smart_mode
        self.llm = llm
        self.smart_filter = SmartFilter(llm) if smart_mode and llm else None
    
    def build(self, project: ProjectStructure, output_path: str = None, 
              query: str = None, output_mode: str = OUTPUT_FILE) -> Tuple[int, str]:
        """Build context and return (file_count, content)."""
        
        files = project.files
        
        # Apply smart filtering if enabled
        if self.smart_filter:
            print("🧠 Analyzing project with LLM...", file=sys.stderr)
            files = self.smart_filter.filter_by_relevance(project, query)
            print(f"   Selected {len(files)} relevant files", file=sys.stderr)
        
        # Read and optionally summarize files
        for file_info in files:
            content = self._read_file(file_info.path)
            
            if self.smart_mode and self.llm and file_info.size > MAX_FILE_SIZE:
                print(f"📝 Summarizing large file: {file_info.relative_path}", file=sys.stderr)
                file_info.content = content
                file_info.summary = self.smart_filter.summarize_large_file(file_info)
            else:
                file_info.content = content
            
            # Parse imports for context
            file_info.imports = ImportParser.parse_imports(file_info.path, content)
        
        # Build content string
        import io
        buffer = io.StringIO()
        self._write_header(buffer, project, query)
        self._write_structure(buffer, project)
        self._write_files(buffer, files)
        content = buffer.getvalue()
        
        # Output based on mode
        if output_mode == OUTPUT_STDOUT:
            print(content)
        elif output_mode == OUTPUT_CLIPBOARD:
            self._copy_to_clipboard(content)
        elif output_mode == OUTPUT_FILE and output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return len(files), content
    
    def _copy_to_clipboard(self, content: str):
        """Copy content to system clipboard."""
        system = sys.platform
        
        try:
            if system == 'darwin':  # macOS
                subprocess.run(['pbcopy'], input=content.encode('utf-8'), check=True)
            elif system == 'win32':  # Windows
                subprocess.run(['clip'], input=content.encode('utf-16'), check=True)
            else:  # Linux/Unix
                # Try xclip first, then xsel, then wl-copy (Wayland)
                for cmd in [['xclip', '-selection', 'clipboard'], 
                            ['xsel', '--clipboard', '--input'],
                            ['wl-copy']]:
                    try:
                        subprocess.run(cmd, input=content.encode('utf-8'), check=True)
                        return
                    except FileNotFoundError:
                        continue
                raise RuntimeError("No clipboard tool found. Install xclip, xsel, or wl-copy")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to copy to clipboard: {e}")
    
    def _read_file(self, filepath: str) -> str:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception:
                return "[Error: Could not decode file]"
        except Exception as e:
            return f"[Error reading file: {e}]"
    
    def _write_header(self, outfile, project: ProjectStructure, query: str = None):
        outfile.write("=" * 80 + "\n")
        outfile.write("PROJECT CONTEXT SNAPSHOT\n")
        outfile.write("=" * 80 + "\n\n")
        
        if project.detected_stack:
            outfile.write(f"Detected Stack: {', '.join(project.detected_stack)}\n")
        
        if query:
            outfile.write(f"Context Focus: {query}\n")
        
        outfile.write(f"Total Files: {len(project.files)}\n")
        outfile.write("\n")
    
    def _write_structure(self, outfile, project: ProjectStructure):
        outfile.write("PROJECT STRUCTURE\n")
        outfile.write("-" * 40 + "\n")
        outfile.write(project.tree)
        outfile.write("\n\n")
    
    def _write_files(self, outfile, files: List[FileInfo]):
        outfile.write("=" * 80 + "\n")
        outfile.write("FILE CONTENTS\n")
        outfile.write("=" * 80 + "\n\n")
        
        # Sort by relevance score (highest first)
        sorted_files = sorted(files, key=lambda f: (-f.relevance_score, f.relative_path))
        
        for file_info in sorted_files:
            outfile.write(f"--- START FILE: {file_info.relative_path} ---\n")
            
            if file_info.summary:
                outfile.write(f"[SUMMARIZED - Original size: {file_info.size} bytes]\n\n")
                outfile.write(file_info.summary)
            else:
                outfile.write(file_info.content)
            
            outfile.write(f"\n--- END FILE: {file_info.relative_path} ---\n\n")

# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Contextuaize - Smart codebase context extraction for LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  contextuaize                          # Basic scan → codebase_context.txt
  contextuaize ./my-project -o ctx.txt  # Scan specific directory
  contextuaize -c                       # Copy to clipboard
  contextuaize --stdout                 # Print to stdout (pipe-friendly)
  contextuaize --stdout | pbcopy        # Pipe to clipboard (macOS)
  contextuaize --smart                  # Use LLM for intelligent filtering
  contextuaize --smart --query "auth"   # Focus on authentication-related code
  contextuaize --include "*.py"         # Only Python files
  contextuaize --exclude "test*"        # Exclude test files
        """
    )
    
    parser.add_argument('directory', nargs='?', default='.',
                        help='Directory to scan (default: current directory)')
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT,
                        help=f'Output file path (default: {DEFAULT_OUTPUT})')
    
    # Filtering options
    parser.add_argument('--include', action='append', default=[],
                        help='Include only files matching pattern (can use multiple times)')
    parser.add_argument('--exclude', action='append', default=[],
                        help='Exclude files matching pattern (can use multiple times)')
    parser.add_argument('--no-gitignore', action='store_true',
                        help='Do not respect .gitignore rules')
    
    # Smart mode options
    parser.add_argument('--smart', action='store_true',
                        help='Enable LLM-powered intelligent filtering')
    parser.add_argument('--query', '-q', type=str,
                        help='Focus context on specific task/feature (requires --smart)')
    parser.add_argument('--api-key', type=str,
                        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
    parser.add_argument('--model', type=str, default='claude-sonnet-4-20250514',
                        help='Model to use for smart mode')
    
    # Output options
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress progress output')
    parser.add_argument('--tree-only', action='store_true',
                        help='Only output the project tree, no file contents')
    
    # Output destination (mutually exclusive)
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('-c', '--clipboard', action='store_true',
                              help='Copy output to clipboard instead of file')
    output_group.add_argument('--stdout', action='store_true',
                              help='Print output to stdout instead of file')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.query and not args.smart:
        print("Warning: --query requires --smart mode. Enabling smart mode.")
        args.smart = True
    
    # Initialize LLM client if smart mode
    llm = None
    if args.smart:
        try:
            llm = LLMClient(api_key=args.api_key, model=args.model)
        except ValueError as e:
            print(f"Error: {e}")
            print("Smart mode requires an API key. Set ANTHROPIC_API_KEY or use --api-key")
            sys.exit(1)
    
    # Scan directory
    if not args.quiet:
        print(f"🚀 Scanning: {os.path.abspath(args.directory)}", file=sys.stderr)
    
    scanner = FileScanner(
        root_dir=args.directory,
        respect_gitignore=not args.no_gitignore,
        include_patterns=args.include,
        exclude_patterns=args.exclude
    )
    
    project = scanner.scan()
    
    if not args.quiet:
        print(f"   Found {len(project.files)} files", file=sys.stderr)
        if project.detected_stack:
            print(f"   Detected: {', '.join(project.detected_stack)}", file=sys.stderr)
    
    # Handle tree-only mode
    if args.tree_only:
        print(project.tree)
        return
    
    # Determine output mode
    if args.clipboard:
        output_mode = OUTPUT_CLIPBOARD
    elif args.stdout:
        output_mode = OUTPUT_STDOUT
    else:
        output_mode = OUTPUT_FILE
    
    # Build context
    builder = ContextBuilder(smart_mode=args.smart, llm=llm)
    
    try:
        file_count, content = builder.build(
            project, 
            args.output, 
            query=args.query,
            output_mode=output_mode
        )
    except Exception as e:
        print(f"Error building context: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not args.quiet:
        if output_mode == OUTPUT_CLIPBOARD:
            size_str = f"{len(content) / 1024:.1f}KB" if len(content) < 1024*1024 else f"{len(content) / (1024*1024):.1f}MB"
            print(f"\n✅ Done! {file_count} files → clipboard ({size_str})", file=sys.stderr)
        elif output_mode == OUTPUT_FILE:
            output_size = os.path.getsize(args.output)
            size_str = f"{output_size / 1024:.1f}KB" if output_size < 1024*1024 else f"{output_size / (1024*1024):.1f}MB"
            print(f"\n✅ Done! {file_count} files → '{args.output}' ({size_str})", file=sys.stderr)
        elif output_mode == OUTPUT_STDOUT:
            size_str = f"{len(content) / 1024:.1f}KB" if len(content) < 1024*1024 else f"{len(content) / (1024*1024):.1f}MB"
            print(f"\n✅ Done! {file_count} files ({size_str})", file=sys.stderr)

if __name__ == "__main__":
    main()
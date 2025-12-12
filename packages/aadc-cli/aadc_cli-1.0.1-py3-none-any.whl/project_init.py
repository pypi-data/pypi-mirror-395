"""
Project Initialization Module for AADC
Generates intelligent codebase summary for AI context
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Tuple
import json

# File extensions to analyze (code files)
CODE_EXTENSIONS = {
    # Web
    '.html', '.css', '.scss', '.sass', '.less',
    '.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte',
    # Backend
    '.py', '.rb', '.php', '.java', '.go', '.rs', '.c', '.cpp', '.h', '.hpp',
    '.cs', '.swift', '.kt', '.scala', '.clj',
    # Config/Data
    '.json', '.yaml', '.yml', '.toml', '.xml',
    # Docs
    '.md', '.rst',
    # Shell
    '.sh', '.bash', '.zsh', '.fish', '.ps1',
    # Other
    '.sql', '.graphql', '.proto',
}

# Directories to ignore
IGNORE_DIRS = {
    'node_modules', '__pycache__', '.git', '.svn', '.hg',
    'venv', 'env', '.venv', '.env',
    'dist', 'build', 'target', 'out', 'bin', 'obj',
    '.idea', '.vscode', '.vs',
    'coverage', '.nyc_output', 'htmlcov',
    '.next', '.nuxt', '.cache',
    'vendor', 'packages', '.aadc',
    'egg-info', '.egg-info', 'aadc_cli.egg-info',
}

# Files to ignore
IGNORE_FILES = {
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'Gemfile.lock', 'poetry.lock', 'Pipfile.lock',
    '.DS_Store', 'Thumbs.db',
    'aadc.md', '.aadc-summary.md',
}

# Patterns to ignore (for sensitive files)
IGNORE_PATTERNS = {
    '.env', '.env.local', '.env.production', '.env.development',
    '.secret', 'credentials', 'secrets',
}

# Summary file name
SUMMARY_FILE = "aadc.md"
OLD_SUMMARY_FILE = ".aadc-summary.md"

# Max file size to read (in bytes) - skip very large files
MAX_FILE_SIZE = 100 * 1024  # 100KB


def should_ignore_file(path: Path) -> bool:
    """Check if a file should be ignored (sensitive/env files)."""
    name_lower = path.name.lower()
    
    if path.name in IGNORE_FILES:
        return True
    
    for pattern in IGNORE_PATTERNS:
        if pattern in name_lower:
            return True
    
    if name_lower.startswith('.env'):
        return True
    
    return False


def should_include_file(path: Path) -> bool:
    """Check if a file should be included in analysis."""
    if should_ignore_file(path):
        return False
    
    if path.suffix.lower() in CODE_EXTENSIONS:
        return True
    
    if path.name in ['Dockerfile', 'Makefile', 'Rakefile', 'Gemfile', 'Procfile', 'requirements.txt']:
        return True
    
    return False


def read_file_content(file_path: Path, max_size: int = MAX_FILE_SIZE) -> Optional[str]:
    """Read file content, respecting size limits."""
    try:
        size = file_path.stat().st_size
        if size > max_size:
            return None
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return None


# ============== Code Analysis Functions ==============

def extract_python_info(content: str) -> Dict:
    """Extract classes, functions, and imports from Python code."""
    info = {"imports": [], "classes": [], "functions": [], "docstring": None}
    
    # Module docstring
    doc_match = re.match(r'^[\s]*["\']["\']["\'](.+?)["\']["\']["\']', content, re.DOTALL)
    if doc_match:
        info["docstring"] = doc_match.group(1).strip()[:200]
    
    # Imports
    for match in re.finditer(r'^(?:from\s+(\S+)\s+)?import\s+(.+)$', content, re.MULTILINE):
        module = match.group(1) or match.group(2).split(',')[0].split(' as ')[0].strip()
        if module and not module.startswith('.'):
            info["imports"].append(module.split('.')[0])
    info["imports"] = list(set(info["imports"]))[:10]
    
    # Classes with methods
    for match in re.finditer(r'^class\s+(\w+)(?:\([^)]*\))?:', content, re.MULTILINE):
        class_name = match.group(1)
        # Find methods in this class
        class_start = match.end()
        methods = []
        for method_match in re.finditer(r'^\s+def\s+(\w+)\s*\(', content[class_start:], re.MULTILINE):
            method_name = method_match.group(1)
            if not method_name.startswith('_') or method_name in ['__init__', '__str__', '__repr__']:
                methods.append(method_name)
            if len(methods) >= 5:
                break
        info["classes"].append({"name": class_name, "methods": methods})
    
    # Top-level functions
    for match in re.finditer(r'^def\s+(\w+)\s*\(([^)]*)\)', content, re.MULTILINE):
        func_name = match.group(1)
        params = match.group(2).strip()
        if not func_name.startswith('_'):
            param_list = [p.split(':')[0].split('=')[0].strip() for p in params.split(',') if p.strip() and p.strip() != 'self']
            info["functions"].append({"name": func_name, "params": param_list[:4]})
    
    return info


def extract_js_ts_info(content: str) -> Dict:
    """Extract exports, functions, and components from JS/TS code."""
    info = {"imports": [], "exports": [], "functions": [], "components": [], "hooks": []}
    
    # Imports (major packages only)
    for match in re.finditer(r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]', content):
        module = match.group(1)
        if not module.startswith('.'):
            info["imports"].append(module.split('/')[0])
    info["imports"] = list(set(info["imports"]))[:8]
    
    # React components (function components)
    for match in re.finditer(r'(?:export\s+)?(?:default\s+)?function\s+([A-Z]\w+)', content):
        info["components"].append(match.group(1))
    
    # Arrow function components
    for match in re.finditer(r'(?:export\s+)?const\s+([A-Z]\w+)\s*[=:][^=]*(?:=>|\bfunction\b)', content):
        if match.group(1) not in info["components"]:
            info["components"].append(match.group(1))
    
    # Hooks
    for match in re.finditer(r'(?:export\s+)?(?:const|function)\s+(use[A-Z]\w+)', content):
        info["hooks"].append(match.group(1))
    
    # Regular functions
    for match in re.finditer(r'(?:export\s+)?(?:async\s+)?function\s+([a-z]\w+)', content):
        info["functions"].append(match.group(1))
    
    # Exports
    for match in re.finditer(r'export\s+(?:default\s+)?(?:const|let|var|function|class)\s+(\w+)', content):
        if match.group(1) not in info["exports"]:
            info["exports"].append(match.group(1))
    
    return info


def extract_html_info(content: str) -> Dict:
    """Extract structure from HTML files."""
    info = {"title": None, "main_elements": [], "scripts": [], "styles": []}
    
    # Title
    title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
    if title_match:
        info["title"] = title_match.group(1).strip()
    
    # Key elements
    for tag in ['header', 'nav', 'main', 'footer', 'section', 'article', 'form']:
        if f'<{tag}' in content.lower():
            info["main_elements"].append(tag)
    
    # External scripts
    for match in re.finditer(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE):
        src = match.group(1)
        if not src.startswith('http'):
            info["scripts"].append(src.split('/')[-1])
    
    return info


def extract_css_info(content: str) -> Dict:
    """Extract key info from CSS files."""
    info = {"selectors": [], "variables": [], "media_queries": False}
    
    # CSS variables
    for match in re.finditer(r'--([a-zA-Z][\w-]+):', content):
        if match.group(1) not in info["variables"]:
            info["variables"].append(match.group(1))
            if len(info["variables"]) >= 5:
                break
    
    # Key class selectors
    for match in re.finditer(r'\.([a-zA-Z][\w-]+)\s*{', content):
        selector = match.group(1)
        if selector not in info["selectors"] and not selector.startswith('_'):
            info["selectors"].append(selector)
            if len(info["selectors"]) >= 10:
                break
    
    # Media queries
    info["media_queries"] = '@media' in content
    
    return info


def extract_json_info(content: str, filename: str) -> Dict:
    """Extract key info from JSON files."""
    info = {"type": "json", "keys": []}
    
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            info["keys"] = list(data.keys())[:10]
            
            # Special handling for package.json
            if filename == 'package.json':
                info["type"] = "package.json"
                info["name"] = data.get("name", "")
                info["scripts"] = list(data.get("scripts", {}).keys())[:5]
                deps = list(data.get("dependencies", {}).keys())[:8]
                dev_deps = list(data.get("devDependencies", {}).keys())[:5]
                info["dependencies"] = deps
                info["devDependencies"] = dev_deps
    except:
        pass
    
    return info


def extract_config_info(content: str, filename: str) -> Dict:
    """Extract info from config files."""
    info = {"type": "config", "purpose": ""}
    
    name_lower = filename.lower()
    if 'tsconfig' in name_lower:
        info["purpose"] = "TypeScript configuration"
    elif 'eslint' in name_lower:
        info["purpose"] = "ESLint configuration"
    elif 'prettier' in name_lower:
        info["purpose"] = "Prettier code formatting"
    elif 'webpack' in name_lower:
        info["purpose"] = "Webpack bundler config"
    elif 'vite' in name_lower:
        info["purpose"] = "Vite build config"
    elif 'tailwind' in name_lower:
        info["purpose"] = "Tailwind CSS config"
    elif 'docker' in name_lower:
        info["purpose"] = "Docker configuration"
    elif name_lower in ['pyproject.toml', 'setup.py', 'setup.cfg']:
        info["purpose"] = "Python package configuration"
    elif name_lower == 'requirements.txt':
        info["purpose"] = "Python dependencies"
        info["packages"] = [line.split('==')[0].split('>=')[0].strip() 
                          for line in content.split('\n') 
                          if line.strip() and not line.startswith('#')][:10]
    
    return info


def analyze_file(path: Path, content: str) -> Dict:
    """Analyze a file and extract relevant information."""
    ext = path.suffix.lower()
    name = path.name
    
    result = {
        "path": str(path),
        "lines": content.count('\n') + 1,
        "size": len(content),
    }
    
    if ext == '.py':
        result["type"] = "Python"
        result["analysis"] = extract_python_info(content)
    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        result["type"] = "JavaScript/TypeScript"
        result["analysis"] = extract_js_ts_info(content)
    elif ext == '.html':
        result["type"] = "HTML"
        result["analysis"] = extract_html_info(content)
    elif ext in ['.css', '.scss', '.sass']:
        result["type"] = "CSS"
        result["analysis"] = extract_css_info(content)
    elif ext == '.json':
        result["type"] = "JSON"
        result["analysis"] = extract_json_info(content, name)
    elif ext in ['.yaml', '.yml', '.toml']:
        result["type"] = "Config"
        result["analysis"] = extract_config_info(content, name)
    elif ext == '.md':
        result["type"] = "Markdown"
        # Extract first heading as title
        heading = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        result["analysis"] = {"title": heading.group(1) if heading else None}
    else:
        result["type"] = ext.upper().replace('.', '') if ext else "Unknown"
        result["analysis"] = {}
    
    return result


def analyze_project(root_path: str) -> Dict:
    """Analyze a project directory and collect file summaries."""
    root = Path(root_path)
    
    analysis = {
        "root": str(root.absolute()),
        "analyzed_at": datetime.now().isoformat(),
        "files": [],
        "stats": {
            "total_files": 0,
            "total_lines": 0,
            "by_extension": {},
            "by_type": {},
        }
    }
    
    # Walk the directory tree
    for item in sorted(root.rglob('*')):
        # Skip ignored directories
        skip = False
        for part in item.parts:
            if part in IGNORE_DIRS or part.endswith('.egg-info'):
                skip = True
                break
        if skip:
            continue
        
        if item.is_file() and should_include_file(item):
            rel_path = item.relative_to(root)
            content = read_file_content(item)
            
            if content:
                file_info = analyze_file(rel_path, content)
                analysis["files"].append(file_info)
                
                # Update stats
                analysis["stats"]["total_files"] += 1
                analysis["stats"]["total_lines"] += file_info["lines"]
                
                ext = item.suffix or "no_ext"
                analysis["stats"]["by_extension"][ext] = analysis["stats"]["by_extension"].get(ext, 0) + 1
                
                ftype = file_info["type"]
                analysis["stats"]["by_type"][ftype] = analysis["stats"]["by_type"].get(ftype, 0) + 1
    
    return analysis


def generate_summary_markdown(analysis: Dict) -> str:
    """Generate intelligent markdown summary of the codebase."""
    lines = []
    
    # Header
    lines.append("# AADC Project Summary")
    lines.append("")
    lines.append("> Auto-generated codebase analysis. The AI uses this to understand your project.")
    lines.append("> Regenerate with `/init`. Do not edit manually.")
    lines.append("")
    lines.append(f"**Generated:** {analysis['analyzed_at']}")
    lines.append(f"**Root:** `{analysis['root']}`")
    lines.append("")
    
    # Stats overview
    stats = analysis["stats"]
    lines.append("## 📊 Project Overview")
    lines.append("")
    lines.append(f"- **Total Files:** {stats['total_files']}")
    lines.append(f"- **Total Lines:** {stats['total_lines']:,}")
    lines.append("")
    
    # Detect project type
    project_type = []
    for f in analysis["files"]:
        name = Path(f["path"]).name
        if name == "package.json":
            pkg = f.get("analysis", {})
            deps = pkg.get("dependencies", []) + pkg.get("devDependencies", [])
            if "react" in deps:
                project_type.append("React")
            if "vue" in deps:
                project_type.append("Vue")
            if "next" in deps:
                project_type.append("Next.js")
            if "express" in deps:
                project_type.append("Express")
            if "vite" in deps:
                project_type.append("Vite")
            if "tailwindcss" in deps:
                project_type.append("Tailwind CSS")
        elif name in ["pyproject.toml", "setup.py", "requirements.txt"]:
            project_type.append("Python")
        elif name == "Cargo.toml":
            project_type.append("Rust")
        elif name == "go.mod":
            project_type.append("Go")
    
    if project_type:
        lines.append(f"**Stack:** {', '.join(set(project_type))}")
        lines.append("")
    
    # File types breakdown
    if stats["by_type"]:
        lines.append("### File Types")
        lines.append("")
        for ftype, count in sorted(stats["by_type"].items(), key=lambda x: -x[1]):
            lines.append(f"- {ftype}: {count} files")
        lines.append("")
    
    # Directory structure
    lines.append("## 📁 Structure")
    lines.append("")
    lines.append("```")
    
    # Build tree
    dirs_seen = set()
    for f in analysis["files"]:
        path = Path(f["path"])
        # Show directory structure
        for i, part in enumerate(path.parts[:-1]):
            dir_path = "/".join(path.parts[:i+1])
            if dir_path not in dirs_seen:
                indent = "  " * i
                lines.append(f"{indent}{part}/")
                dirs_seen.add(dir_path)
        # Show file
        indent = "  " * (len(path.parts) - 1)
        lines.append(f"{indent}{path.name}")
    lines.append("```")
    lines.append("")
    
    # Group files by directory for analysis
    files_by_dir = {}
    for f in analysis["files"]:
        path = Path(f["path"])
        dir_name = str(path.parent) if path.parent != Path('.') else "(root)"
        if dir_name not in files_by_dir:
            files_by_dir[dir_name] = []
        files_by_dir[dir_name].append(f)
    
    # Detailed file analysis
    lines.append("## 📄 File Analysis")
    lines.append("")
    
    for dir_name, files in files_by_dir.items():
        lines.append(f"### 📂 `{dir_name}`")
        lines.append("")
        
        for f in files:
            path = Path(f["path"])
            analysis_data = f.get("analysis", {})
            ftype = f["type"]
            file_lines = f["lines"]
            
            lines.append(f"#### `{path.name}`")
            lines.append(f"*{ftype} • {file_lines} lines*")
            lines.append("")
            
            # Python files
            if ftype == "Python":
                if analysis_data.get("docstring"):
                    lines.append(f"> {analysis_data['docstring'][:150]}...")
                    lines.append("")
                
                if analysis_data.get("imports"):
                    lines.append(f"**Imports:** `{', '.join(analysis_data['imports'][:6])}`")
                
                if analysis_data.get("classes"):
                    lines.append("**Classes:**")
                    for cls in analysis_data["classes"][:5]:
                        methods = ', '.join(cls['methods'][:4]) if cls['methods'] else 'none'
                        lines.append(f"- `{cls['name']}` → methods: {methods}")
                
                if analysis_data.get("functions"):
                    lines.append("**Functions:**")
                    for func in analysis_data["functions"][:8]:
                        params = ', '.join(func['params']) if func['params'] else ''
                        lines.append(f"- `{func['name']}({params})`")
            
            # JavaScript/TypeScript
            elif ftype == "JavaScript/TypeScript":
                if analysis_data.get("imports"):
                    lines.append(f"**Imports:** `{', '.join(analysis_data['imports'][:6])}`")
                
                if analysis_data.get("components"):
                    lines.append(f"**Components:** `{', '.join(analysis_data['components'][:5])}`")
                
                if analysis_data.get("hooks"):
                    lines.append(f"**Hooks:** `{', '.join(analysis_data['hooks'][:5])}`")
                
                if analysis_data.get("functions"):
                    lines.append(f"**Functions:** `{', '.join(analysis_data['functions'][:5])}`")
                
                if analysis_data.get("exports"):
                    lines.append(f"**Exports:** `{', '.join(analysis_data['exports'][:5])}`")
            
            # HTML
            elif ftype == "HTML":
                if analysis_data.get("title"):
                    lines.append(f"**Title:** {analysis_data['title']}")
                if analysis_data.get("main_elements"):
                    lines.append(f"**Structure:** `{', '.join(analysis_data['main_elements'])}`")
            
            # CSS
            elif ftype == "CSS":
                if analysis_data.get("variables"):
                    lines.append(f"**CSS Variables:** `{', '.join(analysis_data['variables'][:5])}`")
                if analysis_data.get("selectors"):
                    lines.append(f"**Key Selectors:** `{', '.join(analysis_data['selectors'][:5])}`")
                if analysis_data.get("media_queries"):
                    lines.append("*Has responsive media queries*")
            
            # package.json
            elif analysis_data.get("type") == "package.json":
                if analysis_data.get("name"):
                    lines.append(f"**Package:** `{analysis_data['name']}`")
                if analysis_data.get("scripts"):
                    lines.append(f"**Scripts:** `{', '.join(analysis_data['scripts'])}`")
                if analysis_data.get("dependencies"):
                    lines.append(f"**Dependencies:** `{', '.join(analysis_data['dependencies'])}`")
                if analysis_data.get("devDependencies"):
                    lines.append(f"**Dev Dependencies:** `{', '.join(analysis_data['devDependencies'])}`")
            
            # Config files
            elif ftype == "Config" and analysis_data.get("purpose"):
                lines.append(f"**Purpose:** {analysis_data['purpose']}")
                if analysis_data.get("packages"):
                    lines.append(f"**Packages:** `{', '.join(analysis_data['packages'][:8])}`")
            
            # JSON
            elif ftype == "JSON" and analysis_data.get("keys"):
                lines.append(f"**Keys:** `{', '.join(analysis_data['keys'][:8])}`")
            
            # Markdown
            elif ftype == "Markdown" and analysis_data.get("title"):
                lines.append(f"**Title:** {analysis_data['title']}")
            
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def init_project(root_path: str) -> Dict:
    """Initialize project analysis and save comprehensive summary."""
    try:
        # Analyze the project
        analysis = analyze_project(root_path)
        
        # Generate markdown summary
        summary_md = generate_summary_markdown(analysis)
        
        # Save to file
        summary_path = Path(root_path) / SUMMARY_FILE
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_md)
        
        # Remove old summary file if exists
        old_summary = Path(root_path) / OLD_SUMMARY_FILE
        if old_summary.exists():
            old_summary.unlink()
        
        return {
            "success": True,
            "message": f"Project analyzed! Summary saved to {SUMMARY_FILE}",
            "summary_path": str(summary_path),
            "stats": analysis["stats"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to initialize project: {str(e)}"
        }


def get_project_summary(root_path: str) -> Optional[str]:
    """Get existing project summary if available."""
    # Try new file first
    summary_path = Path(root_path) / SUMMARY_FILE
    if summary_path.exists():
        try:
            with open(summary_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            pass
    
    # Fall back to old file
    old_summary = Path(root_path) / OLD_SUMMARY_FILE
    if old_summary.exists():
        try:
            with open(old_summary, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            pass
    
    return None


def has_project_summary(root_path: str) -> bool:
    """Check if a project summary exists."""
    return (Path(root_path) / SUMMARY_FILE).exists() or (Path(root_path) / OLD_SUMMARY_FILE).exists()


def get_summary_age(root_path: str) -> Optional[float]:
    """Get the age of the summary file in hours."""
    summary_path = Path(root_path) / SUMMARY_FILE
    if not summary_path.exists():
        summary_path = Path(root_path) / OLD_SUMMARY_FILE
    
    if summary_path.exists():
        mtime = summary_path.stat().st_mtime
        age_seconds = datetime.now().timestamp() - mtime
        return age_seconds / 3600  # Convert to hours
    
    return None

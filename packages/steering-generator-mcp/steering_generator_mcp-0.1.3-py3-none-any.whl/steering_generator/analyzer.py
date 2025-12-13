"""Codebase analysis logic with large codebase support."""
import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from .detector import FrameworkType, get_important_files

# === CONFIGURATION ===
MAX_FILE_SIZE = 500 * 1024  # 500KB max per file
MAX_FILES_PER_PATTERN = 50  # Increased from 10
MAX_TOTAL_FILES = 200  # Total files to process
THREAD_POOL_SIZE = 8  # Parallel file reading

# Folders to always ignore
IGNORE_DIRS = {
    "node_modules", "vendor", ".git", ".svn", ".hg",
    "dist", "build", ".next", ".nuxt", ".output",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    "coverage", ".nyc_output", ".turbo", ".cache",
    "storage", "bootstrap/cache",  # Laravel
}

# === RIPGREP SUPPORT ===
def has_ripgrep() -> bool:
    """Check if ripgrep (rg) is available."""
    return shutil.which("rg") is not None


def ripgrep_find_files(base_path: Path, pattern: str, file_ext: str | None = None) -> list[Path]:
    """Use ripgrep to find files matching pattern. Much faster for large codebases."""
    try:
        cmd = ["rg", "--files", "--hidden"]
        
        # Add ignore patterns
        for ignore in IGNORE_DIRS:
            cmd.extend(["-g", f"!{ignore}/**"])
        
        # Filter by extension if provided
        if file_ext:
            cmd.extend(["-g", f"*.{file_ext}"])
        
        cmd.append(str(base_path))
        
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            files = [Path(f) for f in result.stdout.strip().split("\n") if f]
            return files[:MAX_FILES_PER_PATTERN]
    except Exception:
        pass
    return []


def ripgrep_search_content(base_path: Path, pattern: str, file_glob: str = "*") -> list[dict]:
    """Use ripgrep to search content in files."""
    try:
        cmd = [
            "rg", pattern,
            "--json",
            "-g", file_glob,
            "--max-count", "50",
        ]
        
        for ignore in IGNORE_DIRS:
            cmd.extend(["-g", f"!{ignore}/**"])
        
        cmd.append(str(base_path))
        
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
        
        matches = []
        for line in result.stdout.strip().split("\n"):
            if line:
                try:
                    data = json.loads(line)
                    if data.get("type") == "match":
                        matches.append({
                            "file": data["data"]["path"]["text"],
                            "line": data["data"]["line_number"],
                            "text": data["data"]["lines"]["text"].strip(),
                        })
                except json.JSONDecodeError:
                    continue
        return matches
    except Exception:
        return []


# === FILE OPERATIONS ===
def should_ignore_path(filepath: Path) -> bool:
    """Check if path should be ignored."""
    parts = filepath.parts
    return any(ignore in parts for ignore in IGNORE_DIRS)


def read_file_safe(filepath: Path, max_size: int = MAX_FILE_SIZE) -> str | None:
    """Safely read file content with size limit."""
    try:
        if not filepath.exists() or not filepath.is_file():
            return None
        
        # Skip large files
        if filepath.stat().st_size > max_size:
            return None
        
        # Skip ignored paths
        if should_ignore_path(filepath):
            return None
        
        return filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None


def read_files_parallel(filepaths: list[Path]) -> dict[Path, str]:
    """Read multiple files in parallel."""
    results = {}
    
    with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
        future_to_path = {
            executor.submit(read_file_safe, fp): fp 
            for fp in filepaths[:MAX_TOTAL_FILES]
        }
        
        for future in as_completed(future_to_path):
            filepath = future_to_path[future]
            try:
                content = future.result()
                if content:
                    results[filepath] = content
            except Exception:
                continue
    
    return results


def find_files_by_pattern(base_path: Path, pattern: str) -> list[Path]:
    """Find files matching glob pattern. Uses ripgrep if available."""
    
    # Try ripgrep first for better performance
    if has_ripgrep() and "*" in pattern:
        # Extract extension from pattern like "*.tsx" or "**/*.php"
        ext_match = re.search(r"\*\.(\w+)$", pattern)
        if ext_match:
            ext = ext_match.group(1)
            files = ripgrep_find_files(base_path, pattern, ext)
            if files:
                return files
    
    # Fallback to pathlib glob
    try:
        if "*" in pattern:
            all_files = []
            for filepath in base_path.glob(pattern):
                if not should_ignore_path(filepath) and filepath.is_file():
                    all_files.append(filepath)
                    if len(all_files) >= MAX_FILES_PER_PATTERN:
                        break
            return all_files
        else:
            filepath = base_path / pattern
            if filepath.exists() and not should_ignore_path(filepath):
                return [filepath]
            return []
    except Exception:
        return []


# === CONTENT EXTRACTORS ===
def extract_package_json_info(content: str) -> dict[str, Any]:
    """Extract info from package.json."""
    try:
        data = json.loads(content)
        return {
            "name": data.get("name", ""),
            "dependencies": list(data.get("dependencies", {}).keys()),
            "devDependencies": list(data.get("devDependencies", {}).keys()),
            "scripts": data.get("scripts", {}),
        }
    except Exception:
        return {}


def extract_composer_json_info(content: str) -> dict[str, Any]:
    """Extract info from composer.json."""
    try:
        data = json.loads(content)
        return {
            "name": data.get("name", ""),
            "require": list(data.get("require", {}).keys()),
            "requireDev": list(data.get("require-dev", {}).keys()),
            "scripts": data.get("scripts", {}),
        }
    except Exception:
        return {}


def extract_env_vars(content: str) -> list[str]:
    """Extract environment variable names from .env file."""
    vars_list = []
    for line in content.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            var_name = line.split("=")[0].strip()
            vars_list.append(var_name)
    return vars_list


def extract_typescript_types(content: str) -> list[dict[str, str]]:
    """Extract TypeScript interface/type definitions."""
    types = []
    
    # Match interfaces
    interface_pattern = r"(?:export\s+)?interface\s+(\w+)\s*(?:extends\s+[\w,\s]+)?\s*\{([^}]+)\}"
    for match in re.finditer(interface_pattern, content, re.MULTILINE):
        types.append({
            "kind": "interface",
            "name": match.group(1),
            "preview": match.group(0)[:200],
        })
    
    # Match type aliases
    type_pattern = r"(?:export\s+)?type\s+(\w+)\s*=\s*([^;]+);"
    for match in re.finditer(type_pattern, content, re.MULTILINE):
        types.append({
            "kind": "type",
            "name": match.group(1),
            "preview": match.group(0)[:200],
        })
    
    return types


def extract_php_models(content: str) -> dict[str, Any]:
    """Extract Laravel model info."""
    info: dict[str, Any] = {"class": "", "table": "", "fillable": [], "relations": []}
    
    # Class name
    class_match = re.search(r"class\s+(\w+)\s+extends", content)
    if class_match:
        info["class"] = class_match.group(1)
    
    # Table name
    table_match = re.search(r"\$table\s*=\s*['\"](\w+)['\"]", content)
    if table_match:
        info["table"] = table_match.group(1)
    
    # Fillable fields
    fillable_match = re.search(r"\$fillable\s*=\s*\[([^\]]+)\]", content)
    if fillable_match:
        fields = re.findall(r"['\"](\w+)['\"]", fillable_match.group(1))
        info["fillable"] = fields
    
    # Relations
    relation_patterns = ["hasMany", "hasOne", "belongsTo", "belongsToMany"]
    for rel_pattern in relation_patterns:
        matches = re.findall(
            rf"function\s+(\w+)\s*\([^)]*\)[^{{]*\{{\s*return\s+\$this->{rel_pattern}",
            content
        )
        for match in matches:
            info["relations"].append({"name": match, "type": rel_pattern})
    
    return info


def extract_routes_laravel(content: str) -> list[dict[str, str]]:
    """Extract Laravel routes."""
    routes = []
    pattern = r"Route::(get|post|put|patch|delete)\s*\(\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(pattern, content, re.IGNORECASE):
        routes.append({"method": match.group(1).upper(), "path": match.group(2)})
    return routes[:30]  # Increased limit


def extract_vue_components(content: str) -> dict[str, Any]:
    """Extract Vue component info."""
    info: dict[str, Any] = {"props": [], "emits": [], "composables": []}
    
    # Props
    props_match = re.findall(r"defineProps<\{([^}]+)\}>", content)
    if props_match:
        info["props"] = re.findall(r"(\w+)\s*[?:]", props_match[0])
    
    # Emits
    emits_match = re.findall(r"defineEmits<\{([^}]+)\}>", content)
    if emits_match:
        info["emits"] = re.findall(r"(\w+)\s*:", emits_match[0])
    
    # Composables used
    composables = re.findall(r"use(\w+)\s*\(", content)
    info["composables"] = list(set(composables))
    
    return info


# === MAIN ANALYZER ===
def analyze_codebase(project_path: str, framework: FrameworkType) -> dict[str, Any]:
    """Analyze codebase and return structured data. Optimized for large codebases."""
    path = Path(project_path)
    important_files = get_important_files(framework)
    
    analysis: dict[str, Any] = {
        "framework": framework,
        "projectPath": str(path.absolute()),
        "techStack": {},
        "envVars": [],
        "types": [],
        "routes": [],
        "models": [],
        "components": [],
        "scripts": {},
        "stats": {
            "filesScanned": 0,
            "ripgrepAvailable": has_ripgrep(),
        },
    }
    
    files_scanned = 0
    
    # === CONFIG FILES ===
    for pattern in important_files.get("config", []):
        for filepath in find_files_by_pattern(path, pattern):
            content = read_file_safe(filepath)
            if not content:
                continue
            
            files_scanned += 1
            filename = filepath.name
            
            if filename == "package.json":
                pkg_info = extract_package_json_info(content)
                analysis["techStack"]["dependencies"] = pkg_info.get("dependencies", [])
                analysis["techStack"]["devDependencies"] = pkg_info.get("devDependencies", [])
                analysis["scripts"] = pkg_info.get("scripts", {})
            elif filename == "composer.json":
                composer_info = extract_composer_json_info(content)
                analysis["techStack"]["require"] = composer_info.get("require", [])
                analysis["techStack"]["requireDev"] = composer_info.get("requireDev", [])
                analysis["scripts"] = composer_info.get("scripts", {})
            elif filename.startswith(".env"):
                analysis["envVars"].extend(extract_env_vars(content))
    
    # === TYPE DEFINITIONS (parallel reading) ===
    type_files: list[Path] = []
    for pattern in important_files.get("types", []):
        type_files.extend(find_files_by_pattern(path, pattern))
    
    if type_files:
        contents = read_files_parallel(type_files)
        for filepath, content in contents.items():
            files_scanned += 1
            types = extract_typescript_types(content)
            for t in types:
                t["file"] = str(filepath.relative_to(path))
            analysis["types"].extend(types)
    
    # === LARAVEL SPECIFIC ===
    if framework == "laravel":
        # Models (parallel)
        model_files: list[Path] = []
        for pattern in important_files.get("models", []):
            model_files.extend(find_files_by_pattern(path, pattern))
        
        if model_files:
            contents = read_files_parallel(model_files)
            for filepath, content in contents.items():
                files_scanned += 1
                model_info = extract_php_models(content)
                model_info["file"] = str(filepath.relative_to(path))
                if model_info.get("class"):
                    analysis["models"].append(model_info)
        
        # Routes
        for pattern in important_files.get("routes", []):
            for filepath in find_files_by_pattern(path, pattern):
                content = read_file_safe(filepath)
                if content:
                    files_scanned += 1
                    routes = extract_routes_laravel(content)
                    analysis["routes"].extend(routes)
    
    # === COMPONENTS (just list paths, don't read all) ===
    for pattern in important_files.get("components", []):
        for filepath in find_files_by_pattern(path, pattern):
            rel_path = str(filepath.relative_to(path))
            analysis["components"].append(rel_path)
    
    # === COMPOSABLES/HOOKS ===
    hook_patterns = important_files.get("hooks", []) or important_files.get("composables", [])
    for pattern in hook_patterns:
        for filepath in find_files_by_pattern(path, pattern):
            rel_path = str(filepath.relative_to(path))
            if rel_path not in analysis["components"]:
                analysis["components"].append(rel_path)
    
    # === FINALIZE ===
    analysis["envVars"] = list(set(analysis["envVars"]))
    analysis["stats"]["filesScanned"] = files_scanned
    analysis["stats"]["typesFound"] = len(analysis["types"])
    analysis["stats"]["modelsFound"] = len(analysis["models"])
    analysis["stats"]["routesFound"] = len(analysis["routes"])
    analysis["stats"]["componentsFound"] = len(analysis["components"])
    
    return analysis


def search_codebase(project_path: str, pattern: str, file_glob: str = "*") -> list[dict]:
    """
    Search for a pattern across the codebase.
    Uses ripgrep if available, falls back to Python regex.
    """
    path = Path(project_path)
    
    # Try ripgrep first
    if has_ripgrep():
        return ripgrep_search_content(path, pattern, file_glob)
    
    # Fallback: Python-based search (slower)
    results = []
    for filepath in find_files_by_pattern(path, f"**/{file_glob}"):
        content = read_file_safe(filepath)
        if content:
            for i, line in enumerate(content.split("\n"), 1):
                if re.search(pattern, line):
                    results.append({
                        "file": str(filepath.relative_to(path)),
                        "line": i,
                        "text": line.strip()[:200],
                    })
                    if len(results) >= 50:
                        return results
    
    return results

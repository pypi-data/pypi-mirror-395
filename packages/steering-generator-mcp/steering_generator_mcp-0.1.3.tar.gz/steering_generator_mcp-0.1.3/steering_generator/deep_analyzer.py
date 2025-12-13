"""Deep codebase analysis for comprehensive context extraction."""
import re
import json
from pathlib import Path
from typing import Any

from .analyzer import read_file_safe, find_files_by_pattern, read_files_parallel

# === LIBRARY CATEGORIZATION ===
# Map common packages to categories and purposes
LIBRARY_CATEGORIES = {
    # Frameworks
    "next": ("Framework", "Next.js - React framework with SSR/SSG"),
    "react": ("Framework", "React - UI library"),
    "vue": ("Framework", "Vue.js - Progressive framework"),
    "nuxt": ("Framework", "Nuxt - Vue framework with SSR"),
    "laravel/framework": ("Framework", "Laravel - PHP framework"),
    
    # Database
    "@supabase/supabase-js": ("Database", "Supabase - PostgreSQL backend"),
    "@supabase/ssr": ("Database", "Supabase SSR helpers"),
    "prisma": ("Database", "Prisma - Type-safe ORM"),
    "@prisma/client": ("Database", "Prisma client"),
    "mongoose": ("Database", "MongoDB ODM"),
    "typeorm": ("Database", "TypeORM - SQL ORM"),
    "drizzle-orm": ("Database", "Drizzle - Lightweight ORM"),
    
    # UI Libraries
    "tailwindcss": ("UI & Styling", "Tailwind CSS - Utility-first CSS"),
    "@radix-ui/react-": ("UI & Styling", "Radix UI - Accessible primitives"),
    "shadcn": ("UI & Styling", "shadcn/ui - Component library"),
    "@headlessui/react": ("UI & Styling", "Headless UI - Unstyled components"),
    "lucide-react": ("UI & Styling", "Lucide - Icon library"),
    "@heroicons/react": ("UI & Styling", "Heroicons - Icon library"),
    
    # Forms & Validation
    "react-hook-form": ("Forms", "React Hook Form - Form handling"),
    "zod": ("Forms", "Zod - Schema validation"),
    "yup": ("Forms", "Yup - Schema validation"),
    "@hookform/resolvers": ("Forms", "Form validation resolvers"),
    "formik": ("Forms", "Formik - Form library"),
    
    # State Management
    "zustand": ("State", "Zustand - Lightweight state"),
    "jotai": ("State", "Jotai - Atomic state"),
    "recoil": ("State", "Recoil - State management"),
    "@reduxjs/toolkit": ("State", "Redux Toolkit - State management"),
    "redux": ("State", "Redux - State container"),
    "pinia": ("State", "Pinia - Vue state management"),
    
    # Data Fetching
    "@tanstack/react-query": ("Data Fetching", "TanStack Query - Server state"),
    "swr": ("Data Fetching", "SWR - Data fetching"),
    "axios": ("Data Fetching", "Axios - HTTP client"),
    
    # Auth
    "next-auth": ("Auth", "NextAuth.js - Authentication"),
    "@auth/core": ("Auth", "Auth.js - Authentication"),
    "@clerk/nextjs": ("Auth", "Clerk - Auth & user management"),
    
    # Utilities
    "date-fns": ("Utilities", "date-fns - Date utilities"),
    "dayjs": ("Utilities", "Day.js - Date library"),
    "lodash": ("Utilities", "Lodash - Utility functions"),
    "clsx": ("Utilities", "clsx - Class name utility"),
    "class-variance-authority": ("Utilities", "CVA - Variant styling"),
    
    # Charts & Visualization
    "recharts": ("Charts", "Recharts - Chart library"),
    "chart.js": ("Charts", "Chart.js - Charts"),
    "@nivo/core": ("Charts", "Nivo - Data visualization"),
    
    # Notifications
    "sonner": ("Notifications", "Sonner - Toast notifications"),
    "react-hot-toast": ("Notifications", "React Hot Toast - Toasts"),
    "react-toastify": ("Notifications", "React Toastify - Toasts"),
    
    # Theme
    "next-themes": ("Theme", "next-themes - Theme management"),
}


def categorize_dependencies(deps: list[str]) -> dict[str, list[dict[str, str]]]:
    """Categorize dependencies by purpose."""
    categorized: dict[str, list[dict[str, str]]] = {}
    uncategorized = []
    
    for dep in deps:
        found = False
        for pattern, (category, description) in LIBRARY_CATEGORIES.items():
            if dep == pattern or dep.startswith(pattern):
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append({
                    "name": dep,
                    "purpose": description if dep == pattern else f"{description.split(' - ')[0]} component"
                })
                found = True
                break
        
        if not found:
            uncategorized.append(dep)
    
    if uncategorized:
        categorized["Other"] = [{"name": d, "purpose": ""} for d in uncategorized[:10]]
    
    return categorized


# === README EXTRACTION ===
def extract_readme_info(path: Path) -> dict[str, Any]:
    """Extract product info from README."""
    info = {
        "title": "",
        "description": "",
        "features": [],
        "hasReadme": False,
    }
    
    readme_names = ["README.md", "readme.md", "README.MD", "Readme.md"]
    for name in readme_names:
        readme_path = path / name
        content = read_file_safe(readme_path)
        if content:
            info["hasReadme"] = True
            
            # Extract title (first # heading)
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if title_match:
                info["title"] = title_match.group(1).strip()
            
            # Extract description (first paragraph after title)
            desc_match = re.search(r"^#\s+.+\n\n(.+?)(?:\n\n|\n#)", content, re.MULTILINE | re.DOTALL)
            if desc_match:
                info["description"] = desc_match.group(1).strip()[:500]
            
            # Extract features (bullet points under Features heading)
            features_match = re.search(r"##\s*Features?\s*\n((?:[-*]\s+.+\n?)+)", content, re.IGNORECASE)
            if features_match:
                features = re.findall(r"[-*]\s+(.+)", features_match.group(1))
                info["features"] = features[:10]
            
            break
    
    return info


# === ARCHITECTURE PATTERN DETECTION ===
def detect_architecture_patterns(path: Path, framework: str) -> dict[str, Any]:
    """Detect common architecture patterns in the codebase."""
    patterns = {
        "stateManagement": None,
        "dataFetching": None,
        "authentication": None,
        "styling": None,
        "apiPattern": None,
        "componentPattern": None,
    }
    
    # Check package.json for clues
    pkg_content = read_file_safe(path / "package.json")
    if pkg_content:
        try:
            pkg = json.loads(pkg_content)
            all_deps = list(pkg.get("dependencies", {}).keys()) + list(pkg.get("devDependencies", {}).keys())
            
            # State management
            if "zustand" in all_deps:
                patterns["stateManagement"] = "Zustand (lightweight stores)"
            elif "@reduxjs/toolkit" in all_deps:
                patterns["stateManagement"] = "Redux Toolkit"
            elif "jotai" in all_deps:
                patterns["stateManagement"] = "Jotai (atomic state)"
            elif "recoil" in all_deps:
                patterns["stateManagement"] = "Recoil"
            elif "pinia" in all_deps:
                patterns["stateManagement"] = "Pinia (Vue)"
            
            # Data fetching
            if "@tanstack/react-query" in all_deps:
                patterns["dataFetching"] = "TanStack Query (server state)"
            elif "swr" in all_deps:
                patterns["dataFetching"] = "SWR (stale-while-revalidate)"
            elif "axios" in all_deps:
                patterns["dataFetching"] = "Axios (HTTP client)"
            
            # Auth
            if "next-auth" in all_deps or "@auth/core" in all_deps:
                patterns["authentication"] = "NextAuth.js / Auth.js"
            elif "@clerk/nextjs" in all_deps:
                patterns["authentication"] = "Clerk"
            elif "@supabase/supabase-js" in all_deps:
                patterns["authentication"] = "Supabase Auth"
            
            # Styling
            if "tailwindcss" in all_deps:
                patterns["styling"] = "Tailwind CSS (utility-first)"
                if any("@radix-ui" in d for d in all_deps):
                    patterns["styling"] += " + Radix UI primitives"
            elif "styled-components" in all_deps:
                patterns["styling"] = "Styled Components (CSS-in-JS)"
            elif "@emotion/react" in all_deps:
                patterns["styling"] = "Emotion (CSS-in-JS)"
                
        except json.JSONDecodeError:
            pass
    
    # Detect patterns from code
    if framework in ["nextjs", "react"]:
        # Check for Context pattern
        context_files = find_files_by_pattern(path, "**/*context*.tsx") + find_files_by_pattern(path, "**/*provider*.tsx")
        if context_files:
            patterns["componentPattern"] = "React Context for state sharing"
        
        # Check for custom hooks pattern
        hook_files = find_files_by_pattern(path, "**/use-*.ts") + find_files_by_pattern(path, "**/use*.ts")
        if len(hook_files) > 2:
            if patterns["componentPattern"]:
                patterns["componentPattern"] += " + Custom hooks"
            else:
                patterns["componentPattern"] = "Custom hooks pattern"
    
    # API pattern
    if framework == "nextjs":
        api_routes = find_files_by_pattern(path, "app/api/**/route.ts")
        if api_routes:
            patterns["apiPattern"] = "Next.js Route Handlers (App Router)"
        else:
            api_pages = find_files_by_pattern(path, "pages/api/**/*.ts")
            if api_pages:
                patterns["apiPattern"] = "Next.js API Routes (Pages Router)"
    elif framework == "laravel":
        patterns["apiPattern"] = "Laravel Controllers + Routes"
    
    return patterns


# === KEY FILE CONTENT EXTRACTION ===
def extract_key_file_snippets(path: Path, framework: str) -> dict[str, str]:
    """Extract important code snippets for context."""
    snippets = {}
    
    # Data store / main state file
    data_store_patterns = [
        "lib/data-store.ts", "lib/store.ts", "store/index.ts",
        "src/store/index.ts", "src/lib/store.ts",
    ]
    for pattern in data_store_patterns:
        content = read_file_safe(path / pattern)
        if content:
            # Get first 100 lines or class definition
            lines = content.split("\n")[:100]
            snippets["dataStore"] = "\n".join(lines)
            break
    
    # Types file
    type_patterns = [
        "lib/types.ts", "types/index.ts", "src/types/index.ts",
        "src/lib/types.ts", "types.ts",
    ]
    for pattern in type_patterns:
        content = read_file_safe(path / pattern)
        if content:
            snippets["types"] = content[:3000]  # First 3000 chars
            break
    
    # Main layout/app file
    if framework == "nextjs":
        layout_content = read_file_safe(path / "app/layout.tsx")
        if layout_content:
            snippets["layout"] = layout_content[:2000]
    elif framework == "react":
        app_content = read_file_safe(path / "src/App.tsx") or read_file_safe(path / "src/main.tsx")
        if app_content:
            snippets["app"] = app_content[:2000]
    
    return snippets


# === BUSINESS LOGIC EXTRACTION ===
def extract_business_entities(types_content: str) -> list[dict[str, Any]]:
    """Extract detailed entity information from types file."""
    entities = []
    
    # Better regex: match interface blocks properly
    # This handles multi-line interfaces with nested braces
    interface_pattern = r"(?:export\s+)?interface\s+(\w+)\s*(?:extends\s+([\w,\s]+))?\s*\{"
    
    # Find all interface starts
    for match in re.finditer(interface_pattern, types_content):
        name = match.group(1)
        extends = match.group(2)
        start_pos = match.end()
        
        # Find matching closing brace
        brace_count = 1
        end_pos = start_pos
        while brace_count > 0 and end_pos < len(types_content):
            if types_content[end_pos] == '{':
                brace_count += 1
            elif types_content[end_pos] == '}':
                brace_count -= 1
            end_pos += 1
        
        body = types_content[start_pos:end_pos-1]
        
        # Extract fields - each line that has fieldName: type pattern
        fields = []
        for line in body.split('\n'):
            line = line.strip()
            if not line or line.startswith('//') or line.startswith('/*'):
                continue
            
            # Match: fieldName?: Type or fieldName: Type
            field_match = re.match(r'^(\w+)(\?)?\s*:\s*(.+?)(?:\s*//.*)?$', line)
            if field_match:
                field_name = field_match.group(1)
                optional = field_match.group(2) == '?'
                field_type = field_match.group(3).strip()
                
                # Clean up type (remove trailing comments)
                if '//' in field_type:
                    field_type = field_type.split('//')[0].strip()
                
                fields.append({
                    "name": field_name,
                    "optional": optional,
                    "type": field_type,
                })
        
        entities.append({
            "name": name,
            "extends": extends.strip() if extends else None,
            "fields": fields,
        })
    
    return entities


def extract_status_enums(content: str) -> list[dict[str, Any]]:
    """Extract status/enum-like type definitions from interfaces."""
    enums = []
    seen_values = set()
    
    # Match union types in type definitions
    # e.g., type Status = "pending" | "approved" | "rejected"
    type_pattern = r"type\s+(\w+)\s*=\s*([\"'][^\"']+[\"'](?:\s*\|\s*[\"'][^\"']+[\"'])+)"
    for match in re.finditer(type_pattern, content):
        name = match.group(1)
        values_str = match.group(2)
        values = re.findall(r"[\"']([^\"']+)[\"']", values_str)
        if values:
            enums.append({"name": name, "values": values})
            seen_values.add(tuple(values))
    
    # Also extract inline union types from interface fields
    # e.g., status: "pending" | "approved" | "rejected"
    inline_pattern = r'(\w+)\s*[?]?\s*:\s*(["\'][^"\']+["\'](?:\s*\|\s*["\'][^"\']+["\'])+)'
    for match in re.finditer(inline_pattern, content):
        field_name = match.group(1)
        values_str = match.group(2)
        values = re.findall(r"[\"']([^\"']+)[\"']", values_str)
        
        if values and tuple(values) not in seen_values:
            # Generate a name from field name
            enum_name = field_name[0].upper() + field_name[1:]
            if not enum_name.endswith('Status') and not enum_name.endswith('Type'):
                if 'status' in field_name.lower():
                    enum_name = field_name.replace('status', 'Status').replace('Status', 'Status')
                elif 'type' in field_name.lower():
                    pass
                else:
                    enum_name = f"{enum_name}Values"
            
            enums.append({"name": enum_name, "values": values})
            seen_values.add(tuple(values))
    
    return enums


# === MAIN DEEP ANALYZER ===
def deep_analyze_codebase(project_path: str, framework: str, basic_analysis: dict[str, Any]) -> dict[str, Any]:
    """Perform deep analysis to extract comprehensive context."""
    path = Path(project_path)
    
    deep_analysis = {
        # Categorized dependencies
        "categorizedDeps": categorize_dependencies(
            basic_analysis.get("techStack", {}).get("dependencies", [])
        ),
        
        # README info
        "readme": extract_readme_info(path),
        
        # Architecture patterns
        "patterns": detect_architecture_patterns(path, framework),
        
        # Key code snippets
        "codeSnippets": extract_key_file_snippets(path, framework),
        
        # Detailed entities
        "entities": [],
        
        # Status enums
        "statusEnums": [],
    }
    
    # Extract detailed entities from types
    if deep_analysis["codeSnippets"].get("types"):
        deep_analysis["entities"] = extract_business_entities(
            deep_analysis["codeSnippets"]["types"]
        )
        deep_analysis["statusEnums"] = extract_status_enums(
            deep_analysis["codeSnippets"]["types"]
        )
    
    return deep_analysis

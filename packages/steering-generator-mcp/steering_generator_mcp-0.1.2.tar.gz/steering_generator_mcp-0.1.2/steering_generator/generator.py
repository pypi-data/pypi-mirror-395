"""Steering document generator with deep analysis support.

Generates foundational steering files like Kiro IDE:
- product.md - Product overview, target users, key features, business objectives
- tech.md - Technology stack, frameworks, libraries, dev tools, constraints
- structure.md - File organization, naming conventions, import patterns, architecture

Supports inclusion modes:
- always (default) - Loaded into every interaction
- fileMatch - Conditional based on file pattern
- manual - On-demand via #steering-file-name

Supports file references: #[[file:<relative_file_name>]]
"""
from typing import Any, Literal

OutputFormat = Literal["kiro", "cursor", "copilot", "windsurf", "cline", "aider", "markdown"]
InclusionMode = Literal["always", "fileMatch", "manual"]

# IDE-specific file locations and formats
IDE_CONFIGS = {
    "kiro": {
        "path": ".kiro/steering/",
        "multiple_files": True,
        "description": "Kiro IDE - Multiple .md files in .kiro/steering/",
        "files": ["product.md", "tech.md", "structure.md"],
    },
    "cursor": {
        "path": ".cursor/rules/",
        "filename": "project.mdc",
        "multiple_files": False,
        "description": "Cursor IDE - .cursor/rules/*.mdc",
    },
    "copilot": {
        "path": ".github/",
        "filename": "copilot-instructions.md",
        "multiple_files": False,
        "description": "GitHub Copilot - .github/copilot-instructions.md",
    },
    "windsurf": {
        "path": "",
        "filename": ".windsurfrules",
        "multiple_files": False,
        "description": "Windsurf/Codeium - .windsurfrules in root",
    },
    "cline": {
        "path": "",
        "filename": ".clinerules",
        "multiple_files": False,
        "description": "Cline - .clinerules in root",
    },
    "aider": {
        "path": "",
        "filename": "CONVENTIONS.md",
        "multiple_files": False,
        "description": "Aider - CONVENTIONS.md",
    },
    "markdown": {
        "path": "",
        "filename": "STEERING.md",
        "multiple_files": False,
        "description": "Generic markdown - Single STEERING.md file",
    },
}

FRAMEWORK_NAMES = {
    "nextjs": "Next.js 15 (App Router)",
    "nextjs-pages": "Next.js 15 (Pages Router)",
    "laravel": "Laravel 12",
    "react": "React 19 (Vite)",
    "vue": "Vue.js 3 (Vite)",
    "nuxt": "Nuxt 3",
}


def generate_tech_md(deep_analysis: dict[str, Any]) -> str:
    """Generate tech.md - Technology stack documentation.
    
    Documents chosen frameworks, libraries, development tools, and technical constraints.
    When AI suggests implementations, it will prefer established stack over alternatives.
    """
    framework = deep_analysis.get("framework", "unknown")
    categorized = deep_analysis.get("categorizedDependencies", {}) or deep_analysis.get("categorizedDeps", {})
    patterns = deep_analysis.get("architecturePatterns", {})
    scripts = deep_analysis.get("scripts", {})
    env_vars = deep_analysis.get("envVars", [])
    
    lines = ["# Technology Stack\n"]
    lines.append("This document defines the technology choices for this project. ")
    lines.append("Use these technologies when generating code and suggestions.\n")
    
    # Framework & Runtime
    lines.append("## Framework & Runtime\n")
    lines.append(f"- **Framework**: {FRAMEWORK_NAMES.get(framework, framework)}")
    if framework in ["nextjs", "nextjs-pages", "react"]:
        lines.append("- **UI Library**: React 19")
        lines.append("- **Language**: TypeScript 5")
        lines.append("- **Runtime**: Node.js 20+")
    elif framework in ["vue", "nuxt"]:
        lines.append("- **UI Library**: Vue 3 (Composition API)")
        lines.append("- **Language**: TypeScript 5")
        lines.append("- **Runtime**: Node.js 20+")
    elif framework == "laravel":
        lines.append("- **Language**: PHP 8.2+")
        lines.append("- **Runtime**: PHP-FPM / Laravel Octane")
    lines.append("")
    
    # Database & Backend
    if categorized.get("Database"):
        lines.append("## Database & Backend\n")
        added_db = set()  # Track what we've already added
        for dep in categorized["Database"]:
            purpose = dep.get("purpose", "")
            name = dep.get("name", "")
            if "supabase" in name.lower() and "supabase" not in added_db:
                lines.append("- **Database**: Supabase (PostgreSQL)")
                lines.append("- **Auth**: Supabase Auth")
                lines.append("- **Storage**: Supabase Storage")
                added_db.add("supabase")
            elif "prisma" in name.lower() and "prisma" not in added_db:
                lines.append("- **ORM**: Prisma")
                added_db.add("prisma")
            elif "drizzle" in name.lower() and "drizzle" not in added_db:
                lines.append("- **ORM**: Drizzle ORM")
                added_db.add("drizzle")
            elif purpose and name not in added_db:
                lines.append(f"- {purpose}")
                added_db.add(name)
        lines.append("")
    
    # UI & Styling
    if categorized.get("UI & Styling"):
        lines.append("## UI & Styling\n")
        
        has_tailwind = any("tailwind" in d["name"].lower() for d in categorized["UI & Styling"])
        radix_count = sum(1 for d in categorized["UI & Styling"] if "@radix-ui" in d["name"])
        
        if has_tailwind:
            lines.append("- **CSS Framework**: Tailwind CSS (utility-first)")
        
        if radix_count > 5 and has_tailwind:
            lines.append("- **Component Library**: shadcn/ui (built on Radix UI)")
        elif radix_count > 0:
            lines.append("- **UI Primitives**: Radix UI")
        
        for dep in categorized["UI & Styling"]:
            if dep["name"] == "lucide-react":
                lines.append("- **Icons**: Lucide React")
            elif dep["name"] == "@heroicons/react":
                lines.append("- **Icons**: Heroicons")
        
        if categorized.get("Other"):
            for dep in categorized["Other"]:
                if dep["name"] == "geist":
                    lines.append("- **Font**: Geist font family")
        
        lines.append("")
    
    # Key Libraries
    key_libs = []
    
    if categorized.get("Forms"):
        for dep in categorized["Forms"]:
            name = dep["name"].split("/")[-1]
            if name == "zod":
                key_libs.append("**Validation**: Zod (schema validation)")
            elif "react-hook-form" in dep["name"]:
                key_libs.append("**Forms**: React Hook Form")
    
    if categorized.get("State"):
        for dep in categorized["State"]:
            name = dep["name"]
            if name == "zustand":
                key_libs.append("**State Management**: Zustand")
            elif name == "jotai":
                key_libs.append("**State Management**: Jotai (atomic)")
            elif "@reduxjs/toolkit" in name:
                key_libs.append("**State Management**: Redux Toolkit")
    
    if categorized.get("Data Fetching"):
        for dep in categorized["Data Fetching"]:
            name = dep["name"]
            if "@tanstack/react-query" in name:
                key_libs.append("**Data Fetching**: TanStack Query")
            elif name == "swr":
                key_libs.append("**Data Fetching**: SWR")
    
    if categorized.get("Utilities"):
        for dep in categorized["Utilities"]:
            name = dep["name"]
            if name == "date-fns":
                key_libs.append("**Date Utilities**: date-fns")
            elif name == "dayjs":
                key_libs.append("**Date Utilities**: Day.js")
    
    if categorized.get("Charts"):
        for dep in categorized["Charts"]:
            key_libs.append(f"**Charts**: {dep['name']}")
    
    if categorized.get("Notifications"):
        for dep in categorized["Notifications"]:
            if dep["name"] == "sonner":
                key_libs.append("**Notifications**: Sonner (toast)")
            else:
                key_libs.append(f"**Notifications**: {dep['name']}")
    
    if categorized.get("Theme"):
        for dep in categorized["Theme"]:
            if dep["name"] == "next-themes":
                key_libs.append("**Theming**: next-themes")
    
    if key_libs:
        lines.append("## Key Libraries\n")
        for lib in key_libs:
            lines.append(f"- {lib}")
        lines.append("")
    
    # Development Commands
    if scripts:
        lines.append("## Development Commands\n")
        lines.append("```bash")
        if "dev" in scripts:
            lines.append("npm run dev       # Start development server")
        if "build" in scripts:
            lines.append("npm run build     # Build for production")
        if "start" in scripts:
            lines.append("npm run start     # Start production server")
        if "lint" in scripts:
            lines.append("npm run lint      # Run linter")
        if "test" in scripts:
            lines.append("npm run test      # Run tests")
        lines.append("```\n")
    
    # Environment Variables
    if env_vars:
        lines.append("## Environment Variables\n")
        lines.append("Required environment variables (`.env.local`):\n")
        lines.append("| Variable | Description |")
        lines.append("|----------|-------------|")
        for var in env_vars:
            desc = _get_env_var_description(var)
            lines.append(f"| `{var}` | {desc} |")
        lines.append("")
    
    # Technical Constraints
    lines.append("## Technical Constraints\n")
    lines.append("When generating code, follow these constraints:\n")
    if framework in ["nextjs", "nextjs-pages"]:
        lines.append("- Use Server Components by default, Client Components only when needed")
        lines.append("- Prefer Server Actions for mutations")
        lines.append("- Use `next/image` for images, `next/link` for navigation")
    if has_tailwind if 'has_tailwind' in dir() else False:
        lines.append("- Use Tailwind CSS classes, avoid inline styles")
    lines.append("- Follow TypeScript strict mode")
    lines.append("")
    
    return "\n".join(lines)


def _get_env_var_description(var: str) -> str:
    """Get description for common environment variables."""
    descriptions = {
        "DATABASE_URL": "Database connection string",
        "NEXT_PUBLIC_SUPABASE_URL": "Supabase project URL",
        "NEXT_PUBLIC_SUPABASE_ANON_KEY": "Supabase anonymous key (public)",
        "SUPABASE_SERVICE_ROLE_KEY": "Supabase service role key (server-only)",
        "NEXTAUTH_SECRET": "NextAuth.js secret",
        "NEXTAUTH_URL": "NextAuth.js URL",
        "OPENAI_API_KEY": "OpenAI API key",
        "STRIPE_SECRET_KEY": "Stripe secret key",
        "STRIPE_PUBLISHABLE_KEY": "Stripe publishable key",
    }
    
    # Check exact match first
    if var in descriptions:
        return descriptions[var]
    
    # Pattern matching
    var_upper = var.upper()
    if "SUPABASE" in var_upper and "URL" in var_upper:
        return "Supabase project URL"
    elif "SUPABASE" in var_upper and "ANON" in var_upper:
        return "Supabase anonymous key"
    elif "SUPABASE" in var_upper and "SERVICE" in var_upper:
        return "Supabase service role key"
    elif "DATABASE" in var_upper or "DB_" in var_upper:
        return "Database connection"
    elif "API_KEY" in var_upper or "APIKEY" in var_upper:
        return "API key"
    elif "SECRET" in var_upper:
        return "Secret key"
    elif "URL" in var_upper:
        return "Service URL"
    
    return "Required"


def generate_structure_md(deep_analysis: dict[str, Any]) -> str:
    """Generate structure.md - Project structure documentation.
    
    Outlines file organization, naming conventions, import patterns, and 
    architectural decisions. Ensures generated code fits seamlessly into 
    existing codebase.
    """
    framework = deep_analysis.get("framework", "unknown")
    patterns = deep_analysis.get("architecturePatterns", {})
    components = deep_analysis.get("components", [])
    
    lines = ["# Project Structure\n"]
    lines.append("This document defines the project organization and architectural patterns.")
    lines.append("Follow these conventions when creating new files and components.\n")
    
    # Framework-specific structure
    lines.append("## Directory Structure\n")
    
    structures = {
        "nextjs": """```
├── app/                    # Next.js App Router
│   ├── (routes)/          # Route groups
│   ├── api/               # API Route Handlers
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
│
├── components/            # React components
│   ├── ui/               # Reusable UI primitives
│   └── [feature]/        # Feature-specific components
│
├── hooks/                 # Custom React hooks
│   └── use-*.ts          # Hook files (use- prefix)
│
├── lib/                   # Core utilities
│   ├── types.ts          # TypeScript type definitions
│   ├── utils.ts          # Utility functions
│   └── [service].ts      # Service modules
│
├── public/               # Static assets
│
└── config files          # next.config.ts, tailwind.config.ts, etc.
```""",
        "nextjs-pages": """```
├── pages/                 # Next.js Pages Router
│   ├── api/              # API routes
│   ├── _app.tsx          # App wrapper
│   ├── _document.tsx     # Document wrapper
│   └── [route].tsx       # Page components
│
├── components/            # React components
│   ├── ui/               # Reusable UI primitives
│   └── [feature]/        # Feature-specific components
│
├── hooks/                 # Custom React hooks
├── lib/                   # Core utilities
├── styles/               # CSS/SCSS files
└── public/               # Static assets
```""",
        "laravel": """```
├── app/
│   ├── Http/
│   │   ├── Controllers/   # Request handlers
│   │   ├── Middleware/    # HTTP middleware
│   │   └── Requests/      # Form requests
│   ├── Models/            # Eloquent models
│   └── Services/          # Business logic
│
├── config/                # Configuration files
├── database/
│   ├── migrations/        # Database migrations
│   └── seeders/          # Database seeders
│
├── resources/
│   └── views/            # Blade templates
│
├── routes/
│   ├── web.php           # Web routes
│   └── api.php           # API routes
│
└── public/               # Public assets
```""",
        "react": """```
├── src/
│   ├── components/        # React components
│   │   ├── ui/           # Reusable UI components
│   │   └── [feature]/    # Feature components
│   ├── hooks/            # Custom hooks
│   ├── store/            # State management
│   ├── services/         # API services
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   ├── App.tsx           # Root component
│   └── main.tsx          # Entry point
│
├── public/               # Static assets
└── vite.config.ts        # Vite configuration
```""",
        "vue": """```
├── src/
│   ├── components/        # Vue components
│   │   ├── ui/           # Reusable UI components
│   │   └── [feature]/    # Feature components
│   ├── composables/      # Composition API hooks
│   ├── stores/           # Pinia stores
│   ├── router/           # Vue Router config
│   ├── types/            # TypeScript types
│   ├── App.vue           # Root component
│   └── main.ts           # Entry point
│
├── public/               # Static assets
└── vite.config.ts        # Vite configuration
```""",
        "nuxt": """```
├── pages/                 # File-based routing (auto-imported)
├── components/            # Vue components (auto-imported)
│   ├── ui/               # Reusable UI components
│   └── [feature]/        # Feature components
├── composables/          # Composition API hooks (auto-imported)
├── server/
│   ├── api/              # Server API routes
│   └── middleware/       # Server middleware
├── stores/               # Pinia stores
├── public/               # Static assets
└── nuxt.config.ts        # Nuxt configuration
```""",
    }
    
    lines.append(structures.get(framework, "```\n# Project structure varies by framework\n```"))
    lines.append("")
    
    # Naming Conventions
    lines.append("## Naming Conventions\n")
    
    if framework in ["nextjs", "nextjs-pages", "react"]:
        lines.append("| Type | Convention | Example |")
        lines.append("|------|------------|---------|")
        lines.append("| Components | PascalCase | `UserProfile.tsx` |")
        lines.append("| Hooks | camelCase with `use` prefix | `useAuth.ts` |")
        lines.append("| Utilities | camelCase | `formatDate.ts` |")
        lines.append("| Types | PascalCase | `User`, `ApiResponse` |")
        lines.append("| Constants | SCREAMING_SNAKE_CASE | `MAX_ITEMS` |")
        lines.append("| Files | kebab-case or PascalCase | `user-profile.tsx` |")
    elif framework in ["vue", "nuxt"]:
        lines.append("| Type | Convention | Example |")
        lines.append("|------|------------|---------|")
        lines.append("| Components | PascalCase | `UserProfile.vue` |")
        lines.append("| Composables | camelCase with `use` prefix | `useAuth.ts` |")
        lines.append("| Stores | camelCase | `userStore.ts` |")
        lines.append("| Types | PascalCase | `User`, `ApiResponse` |")
    elif framework == "laravel":
        lines.append("| Type | Convention | Example |")
        lines.append("|------|------------|---------|")
        lines.append("| Controllers | PascalCase + Controller | `UserController.php` |")
        lines.append("| Models | PascalCase singular | `User.php` |")
        lines.append("| Migrations | snake_case with timestamp | `2024_01_01_create_users_table.php` |")
        lines.append("| Routes | kebab-case | `/user-profile` |")
    lines.append("")
    
    # Architecture Patterns
    if any(patterns.values()):
        lines.append("## Architecture Patterns\n")
        
        if patterns.get("stateManagement"):
            lines.append(f"**State Management**: {patterns['stateManagement']}\n")
        
        if patterns.get("dataFetching"):
            lines.append(f"**Data Fetching**: {patterns['dataFetching']}\n")
        
        if patterns.get("authentication"):
            lines.append(f"**Authentication**: {patterns['authentication']}\n")
        
        if patterns.get("apiPattern"):
            lines.append(f"**API Pattern**: {patterns['apiPattern']}\n")
        
        if patterns.get("componentPattern"):
            lines.append(f"**Component Pattern**: {patterns['componentPattern']}\n")
        
        if patterns.get("styling"):
            lines.append(f"**Styling**: {patterns['styling']}\n")
    
    # Import Patterns
    lines.append("## Import Conventions\n")
    
    if framework in ["nextjs", "nextjs-pages", "react"]:
        lines.append("```typescript")
        lines.append("// 1. React/Next imports")
        lines.append("import { useState, useEffect } from 'react'")
        lines.append("")
        lines.append("// 2. Third-party libraries")
        lines.append("import { z } from 'zod'")
        lines.append("")
        lines.append("// 3. Internal imports (use path aliases)")
        lines.append("import { Button } from '@/components/ui/button'")
        lines.append("import { useAuth } from '@/hooks/use-auth'")
        lines.append("import { cn } from '@/lib/utils'")
        lines.append("import type { User } from '@/lib/types'")
        lines.append("```\n")
    elif framework in ["vue", "nuxt"]:
        lines.append("```typescript")
        lines.append("// 1. Vue imports")
        lines.append("import { ref, computed } from 'vue'")
        lines.append("")
        lines.append("// 2. Third-party libraries")
        lines.append("import { z } from 'zod'")
        lines.append("")
        lines.append("// 3. Internal imports")
        lines.append("import { useAuth } from '@/composables/useAuth'")
        lines.append("import type { User } from '@/types'")
        lines.append("```\n")
    
    # File References
    lines.append("## Key Files\n")
    lines.append("Reference these files for implementation patterns:\n")
    
    if framework in ["nextjs", "nextjs-pages"]:
        lines.append("- Types: #[[file:lib/types.ts]]")
        lines.append("- Utilities: #[[file:lib/utils.ts]]")
        lines.append("- Root Layout: #[[file:app/layout.tsx]]")
    elif framework == "react":
        lines.append("- Types: #[[file:src/types/index.ts]]")
        lines.append("- App Entry: #[[file:src/App.tsx]]")
    elif framework in ["vue", "nuxt"]:
        lines.append("- Types: #[[file:types/index.ts]]")
        lines.append("- App Config: #[[file:nuxt.config.ts]]" if framework == "nuxt" else "- App Entry: #[[file:src/App.vue]]")
    
    lines.append("")
    
    return "\n".join(lines)


def generate_product_md(deep_analysis: dict[str, Any]) -> str:
    """Generate product.md - Product overview documentation.
    
    Defines product's purpose, target users, key features, and business objectives.
    Helps AI understand the "why" behind technical decisions and suggest solutions 
    aligned with product goals.
    """
    readme = deep_analysis.get("readme", {})
    entities = deep_analysis.get("entities", [])
    status_enums = deep_analysis.get("statusEnums", [])
    framework = deep_analysis.get("framework", "unknown")
    
    lines = ["# Product Overview\n"]
    lines.append("This document defines the product context and business domain.")
    lines.append("Use this information to understand the purpose behind code decisions.\n")
    
    # Product Name & Description
    if readme.get("title") and "deploy" not in readme["title"].lower():
        lines.append(f"## Product: {readme['title']}\n")
    else:
        lines.append("## Product\n")
    
    if readme.get("description"):
        lines.append(readme["description"])
        lines.append("")
    else:
        lines.append("*Add product description to README.md for better context.*\n")
    
    # Target Users (infer from entities/features if possible)
    lines.append("## Target Users\n")
    if readme.get("description"):
        # Try to infer from description
        desc_lower = readme["description"].lower()
        if any(word in desc_lower for word in ["admin", "dashboard", "management"]):
            lines.append("- Administrators / Internal teams")
        if any(word in desc_lower for word in ["customer", "user", "client"]):
            lines.append("- End users / Customers")
        if any(word in desc_lower for word in ["developer", "api", "integration"]):
            lines.append("- Developers / Technical users")
        if not any(word in desc_lower for word in ["admin", "customer", "user", "developer"]):
            lines.append("- *Define target users based on product requirements*")
    else:
        lines.append("- *Define target users based on product requirements*")
    lines.append("")
    
    # Key Features
    if readme.get("features"):
        lines.append("## Key Features\n")
        for feature in readme["features"][:10]:
            lines.append(f"- {feature}")
        lines.append("")
    else:
        lines.append("## Key Features\n")
        lines.append("*Add features section to README.md or define here:*\n")
        lines.append("- Feature 1")
        lines.append("- Feature 2")
        lines.append("")
    
    # Core Domain Entities
    if entities:
        lines.append("## Core Entities\n")
        lines.append("The main data models in this application:\n")
        
        for entity in entities[:8]:
            name = entity.get("name", "")
            fields = entity.get("fields", [])
            
            if name:
                # Skip internal/utility types
                if name.endswith("Props") or name.endswith("State") or name.startswith("_"):
                    continue
                
                lines.append(f"### {name}\n")
                
                if fields:
                    # Show key fields
                    key_fields = [f for f in fields if not f.get("optional", False)][:5]
                    optional_fields = [f for f in fields if f.get("optional", False)][:3]
                    
                    if key_fields:
                        lines.append("**Required fields:**")
                        for field in key_fields:
                            lines.append(f"- `{field['name']}`: {field['type']}")
                    
                    if optional_fields:
                        lines.append("\n**Optional fields:**")
                        for field in optional_fields:
                            lines.append(f"- `{field['name']}?`: {field['type']}")
                    
                    lines.append("")
        
        lines.append("")
    
    # Business Rules / Status Values
    if status_enums:
        lines.append("## Status Values & Workflows\n")
        lines.append("Important status values used in the application:\n")
        
        for enum in status_enums[:5]:
            lines.append(f"**{enum['name']}**: {' → '.join(f'`{v}`' for v in enum['values'])}\n")
        
        lines.append("")
    
    # Business Objectives
    lines.append("## Business Objectives\n")
    lines.append("When implementing features, consider these goals:\n")
    lines.append("- Maintain data integrity and validation")
    lines.append("- Ensure good user experience and accessibility")
    lines.append("- Follow security best practices")
    lines.append("- Keep code maintainable and testable")
    lines.append("")
    
    return "\n".join(lines)


def _wrap_kiro_format(
    content: str, 
    inclusion: InclusionMode = "always",
    file_match_pattern: str | None = None
) -> str:
    """Wrap content with Kiro front-matter.
    
    Inclusion modes:
    - always: Loaded into every interaction (default)
    - fileMatch: Conditional based on file pattern
    - manual: On-demand via #steering-file-name
    """
    if inclusion == "fileMatch" and file_match_pattern:
        return f"""---
inclusion: fileMatch
fileMatchPattern: "{file_match_pattern}"
---

{content}"""
    elif inclusion == "manual":
        return f"""---
inclusion: manual
---

{content}"""
    else:
        return f"""---
inclusion: always
---

{content}"""


def _wrap_cursor_format(content: str, description: str) -> str:
    """Wrap content with Cursor MDC front-matter."""
    return f"""---
description: {description}
alwaysApply: true
---

{content}"""


def _wrap_copilot_format(content: str) -> str:
    """Format for GitHub Copilot instructions."""
    return f"""# GitHub Copilot Instructions

{content}

---
*Generated by Steering Generator MCP*
"""


def generate_steering_docs_deep(
    deep_analysis: dict[str, Any],
    output_format: OutputFormat = "kiro"
) -> dict[str, str]:
    """Generate comprehensive steering docs from deep analysis.
    
    For Kiro format, generates 3 foundational files:
    - product.md - Product overview, target users, features, business objectives
    - tech.md - Technology stack, frameworks, libraries, constraints
    - structure.md - File organization, naming conventions, architecture
    """
    
    framework = deep_analysis.get("framework", "unknown")
    
    # Generate 3 foundational docs (like Kiro)
    docs = {
        "product.md": generate_product_md(deep_analysis),
        "tech.md": generate_tech_md(deep_analysis),
        "structure.md": generate_structure_md(deep_analysis),
    }
    
    config = IDE_CONFIGS.get(output_format, IDE_CONFIGS["markdown"])
    
    # === KIRO: Multiple files with front-matter ===
    if output_format == "kiro":
        result = {}
        for name, content in docs.items():
            wrapped = _wrap_kiro_format(content, inclusion="always")
            result[f"{config['path']}{name}"] = wrapped
        return result
    
    # === CURSOR: Single .mdc file ===
    if output_format == "cursor":
        combined = "\n\n---\n\n".join(docs.values())
        wrapped = _wrap_cursor_format(
            combined, 
            f"Project steering for {FRAMEWORK_NAMES.get(framework, framework)}"
        )
        return {f"{config['path']}{config['filename']}": wrapped}
    
    # === COPILOT: .github/copilot-instructions.md ===
    if output_format == "copilot":
        combined = "\n\n---\n\n".join(docs.values())
        wrapped = _wrap_copilot_format(combined)
        return {f"{config['path']}{config['filename']}": wrapped}
    
    # === All others: plain markdown ===
    combined = "\n\n---\n\n".join(docs.values())
    filename = config.get("filename", "STEERING.md")
    path = config.get("path", "")
    return {f"{path}{filename}": combined}


# Keep old function for backward compatibility
def generate_steering_docs(
    analysis: dict[str, Any],
    output_format: OutputFormat = "kiro"
) -> dict[str, str]:
    """Generate steering docs (basic version for backward compatibility)."""
    # If deep analysis data is present, use new generator
    if "categorizedDependencies" in analysis:
        return generate_steering_docs_deep(analysis, output_format)
    
    # Otherwise use simple generation
    from .analyzer import analyze_codebase
    from .deep_analyzer import deep_analyze_codebase
    
    framework = analysis.get("framework", "unknown")
    project_path = analysis.get("projectPath", ".")
    
    # Do deep analysis
    deep = deep_analyze_codebase(project_path, framework, analysis)
    
    # Merge
    deep["framework"] = framework
    deep["scripts"] = analysis.get("scripts", {})
    deep["envVars"] = analysis.get("envVars", [])
    deep["components"] = analysis.get("components", [])
    
    return generate_steering_docs_deep(deep, output_format)


def get_supported_ides() -> dict[str, dict]:
    """Return info about all supported IDEs."""
    return IDE_CONFIGS

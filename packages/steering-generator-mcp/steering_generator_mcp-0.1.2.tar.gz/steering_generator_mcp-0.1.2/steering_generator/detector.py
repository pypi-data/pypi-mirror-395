"""Framework detection logic."""
import os
from pathlib import Path
from typing import Literal

FrameworkType = Literal["nextjs", "laravel", "react", "vue", "nuxt", "unknown"]

# Signature files untuk detect framework
FRAMEWORK_SIGNATURES = {
    "nextjs": [
        ("next.config.js", None),
        ("next.config.mjs", None),
        ("next.config.ts", None),
        ("package.json", '"next"'),
    ],
    "nuxt": [
        ("nuxt.config.js", None),
        ("nuxt.config.ts", None),
        ("package.json", '"nuxt"'),
    ],
    "laravel": [
        ("artisan", None),
        ("composer.json", '"laravel/framework"'),
    ],
    "vue": [
        ("vite.config.js", "vue"),
        ("vite.config.ts", "vue"),
        ("package.json", '"vue"'),
    ],
    "react": [
        ("vite.config.js", "react"),
        ("vite.config.ts", "react"),
        ("package.json", '"react"'),
    ],
}

def detect_framework(project_path: str) -> FrameworkType:
    """Detect framework dari project directory."""
    path = Path(project_path)
    
    if not path.exists():
        return "unknown"
    
    # Check each framework in priority order
    for framework, signatures in FRAMEWORK_SIGNATURES.items():
        for filename, content_check in signatures:
            filepath = path / filename
            if filepath.exists():
                if content_check is None:
                    return framework
                try:
                    content = filepath.read_text(encoding="utf-8")
                    if content_check in content:
                        return framework
                except Exception:
                    continue
    
    return "unknown"

def get_important_files(framework: FrameworkType) -> dict[str, list[str]]:
    """Return list of important files to read based on framework."""
    
    files_map = {
        "nextjs": {
            "config": ["package.json", "tsconfig.json", "next.config.mjs", "next.config.js", ".env.example", ".env.local"],
            "types": ["lib/types.ts", "types/index.ts", "src/types/index.ts", "src/lib/types.ts"],
            "routes": ["app/page.tsx", "app/layout.tsx", "pages/index.tsx", "pages/_app.tsx"],
            "api": ["app/api/*/route.ts", "pages/api/*.ts"],
            "components": ["components/*.tsx", "src/components/*.tsx"],
            "lib": ["lib/*.ts", "src/lib/*.ts", "utils/*.ts"],
        },
        "laravel": {
            "config": ["composer.json", ".env.example", "config/app.php", "config/database.php"],
            "models": ["app/Models/*.php"],
            "controllers": ["app/Http/Controllers/*.php"],
            "routes": ["routes/web.php", "routes/api.php"],
            "migrations": ["database/migrations/*.php"],
            "middleware": ["app/Http/Middleware/*.php"],
        },
        "react": {
            "config": ["package.json", "tsconfig.json", "vite.config.ts", "vite.config.js", ".env.example"],
            "types": ["src/types/*.ts", "types/*.ts"],
            "components": ["src/components/*.tsx", "src/components/**/*.tsx"],
            "hooks": ["src/hooks/*.ts", "src/hooks/*.tsx"],
            "store": ["src/store/*.ts", "src/redux/*.ts", "src/context/*.tsx"],
            "api": ["src/api/*.ts", "src/services/*.ts"],
        },
        "vue": {
            "config": ["package.json", "tsconfig.json", "vite.config.ts", "vite.config.js", ".env.example"],
            "types": ["src/types/*.ts", "types/*.ts"],
            "components": ["src/components/*.vue", "src/components/**/*.vue"],
            "composables": ["src/composables/*.ts"],
            "store": ["src/stores/*.ts", "src/store/*.ts"],
            "router": ["src/router/index.ts", "src/router/*.ts"],
        },
        "nuxt": {
            "config": ["package.json", "nuxt.config.ts", "nuxt.config.js", ".env.example"],
            "types": ["types/*.ts", "types/*.d.ts"],
            "pages": ["pages/*.vue", "pages/**/*.vue"],
            "components": ["components/*.vue", "components/**/*.vue"],
            "composables": ["composables/*.ts"],
            "server": ["server/api/*.ts", "server/routes/*.ts"],
        },
        "unknown": {
            "config": ["package.json", "composer.json", "requirements.txt", "Cargo.toml", "go.mod"],
        },
    }
    
    return files_map.get(framework, files_map["unknown"])

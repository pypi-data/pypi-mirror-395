"""FastMCP Server for Steering Generator.

Generates foundational steering files like Kiro IDE:
- product.md - Product overview, target users, key features, business objectives
- tech.md - Technology stack, frameworks, libraries, dev tools, constraints  
- structure.md - File organization, naming conventions, import patterns, architecture

Supports multiple IDE output formats and inclusion modes.
"""
from fastmcp import FastMCP
from typing import Literal
import json

from .detector import detect_framework, get_important_files, FrameworkType
from .analyzer import analyze_codebase
from .deep_analyzer import deep_analyze_codebase
from .generator import (
    generate_steering_docs, 
    OutputFormat, 
    InclusionMode,
    get_supported_ides, 
    IDE_CONFIGS,
    _wrap_kiro_format,
)

mcp = FastMCP(
    name="Steering Generator",
    instructions="""
    This MCP server auto-generates steering/context documentation from codebases,
    similar to Kiro IDE's built-in steering generation feature.
    
    ## Foundational Steering Files
    
    Generates 3 core files (like Kiro):
    - product.md - Product overview, target users, features, business objectives
    - tech.md - Technology stack, frameworks, libraries, constraints
    - structure.md - File organization, naming conventions, architecture
    
    ## Supported Frameworks
    Next.js (App Router & Pages), Laravel, React, Vue, Nuxt
    
    ## Workflow
    1. Call `generate_steering(project_path, output_format)` to generate all docs
    2. Or use `deep_analyze_project` first for detailed analysis
    
    ## Output Formats
    - kiro: Multiple .md files in .kiro/steering/ (with front-matter)
    - cursor: Single .cursor/rules/project.mdc
    - copilot: .github/copilot-instructions.md
    - windsurf: .windsurfrules
    - cline: .clinerules
    - aider: CONVENTIONS.md
    - markdown: Single STEERING.md
    
    ## Inclusion Modes (Kiro format)
    - always: Loaded into every interaction (default)
    - fileMatch: Conditional based on file pattern
    - manual: On-demand via #steering-file-name
    
    ## File References
    Use #[[file:<relative_path>]] to reference workspace files
    """
)

@mcp.tool
def detect_project_framework(project_path: str) -> dict:
    """
    Detect the framework used in a project directory.
    
    Args:
        project_path: Absolute or relative path to the project root
        
    Returns:
        Dictionary with detected framework and important files to analyze
    """
    framework = detect_framework(project_path)
    important_files = get_important_files(framework)
    
    return {
        "framework": framework,
        "importantFiles": important_files,
        "supported": framework != "unknown",
    }

@mcp.tool
def analyze_project(project_path: str, framework: str | None = None) -> dict:
    """
    Analyze a codebase and extract structured information.
    
    Args:
        project_path: Absolute or relative path to the project root
        framework: Optional framework override (nextjs, laravel, react, vue, nuxt).
                   If not provided, will auto-detect.
    
    Returns:
        Structured analysis including tech stack, types, routes, models, etc.
    """
    if framework is None:
        framework = detect_framework(project_path)
    
    analysis = analyze_codebase(project_path, framework)
    return analysis

@mcp.tool
def generate_steering(
    project_path: str,
    output_format: str = "all",
    framework: str | None = None,
    write_files: bool = True,
) -> dict:
    """
    Generate steering documentation from a codebase and write to disk.
    
    Args:
        project_path: Absolute or relative path to the project root
        output_format: Output format:
                       - "all" (default) - Generate for ALL IDEs at once
                       - "kiro" - .kiro/steering/*.md
                       - "cursor" - .cursor/rules/project.mdc
                       - "copilot" - .github/copilot-instructions.md
                       - "windsurf" - .windsurfrules
                       - "cline" - .clinerules
                       - "aider" - CONVENTIONS.md
                       - "markdown" - STEERING.md
        framework: Optional framework override. If not provided, will auto-detect.
        write_files: If True (default), automatically write files to disk.
    
    Returns:
        Dictionary with generated files info and status
    """
    from pathlib import Path
    
    if framework is None:
        framework = detect_framework(project_path)
    
    analysis = analyze_codebase(project_path, framework)
    
    # Determine which formats to generate
    all_formats = ["kiro", "cursor", "copilot", "windsurf", "cline", "aider"]
    
    if output_format == "all":
        formats_to_generate = all_formats
    elif output_format in all_formats + ["markdown"]:
        formats_to_generate = [output_format]
    else:
        formats_to_generate = all_formats  # Default to all
    
    # Generate docs for each format
    all_docs = {}
    for fmt in formats_to_generate:
        docs = generate_steering_docs(analysis, fmt)
        all_docs.update(docs)
    
    # Write files to disk
    written_files = []
    errors = []
    
    if write_files:
        base_path = Path(project_path).resolve()
        
        for file_path, content in all_docs.items():
            full_path = base_path / file_path
            
            try:
                # Create directory if needed
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write file
                full_path.write_text(content, encoding="utf-8")
                written_files.append(str(file_path))
            except Exception as e:
                errors.append({"file": file_path, "error": str(e)})
    
    return {
        "framework": framework,
        "outputFormats": formats_to_generate,
        "filesWritten": written_files,
        "errors": errors if errors else None,
        "success": len(errors) == 0,
        "message": f"Generated steering docs for {len(formats_to_generate)} IDEs, wrote {len(written_files)} files",
    }

@mcp.tool
def deep_analyze_project(project_path: str, framework: str | None = None) -> dict:
    """
    Perform deep analysis of a codebase for comprehensive context.
    
    This extracts much more detail than analyze_project, including:
    - Categorized dependencies with purposes
    - README/product info
    - Architecture patterns (state management, auth, styling)
    - Key code snippets
    - Detailed entity definitions with fields
    - Status enums and workflows
    
    Use this when you need to generate detailed steering docs like Kiro does.
    
    Args:
        project_path: Absolute or relative path to the project root
        framework: Optional framework override. If not provided, will auto-detect.
    
    Returns:
        Comprehensive analysis with categorized deps, patterns, code snippets, etc.
    """
    if framework is None:
        framework = detect_framework(project_path)
    
    # Get basic analysis first
    basic_analysis = analyze_codebase(project_path, framework)
    
    # Perform deep analysis
    deep_analysis = deep_analyze_codebase(project_path, framework, basic_analysis)
    
    # Merge results
    return {
        "framework": framework,
        "projectPath": basic_analysis.get("projectPath"),
        
        # Basic info
        "scripts": basic_analysis.get("scripts", {}),
        "envVars": basic_analysis.get("envVars", []),
        "components": basic_analysis.get("components", []),
        
        # Deep analysis
        "categorizedDependencies": deep_analysis.get("categorizedDeps", {}),
        "readme": deep_analysis.get("readme", {}),
        "architecturePatterns": deep_analysis.get("patterns", {}),
        "codeSnippets": deep_analysis.get("codeSnippets", {}),
        "entities": deep_analysis.get("entities", []),
        "statusEnums": deep_analysis.get("statusEnums", []),
        
        # Stats
        "stats": basic_analysis.get("stats", {}),
    }


@mcp.tool
def list_supported_frameworks() -> dict:
    """
    List all supported frameworks and their detection signatures.
    
    Returns:
        Dictionary of supported frameworks with detection info
    """
    return {
        "frameworks": [
            {
                "id": "nextjs",
                "name": "Next.js",
                "signatures": ["next.config.js", "next.config.mjs", "next.config.ts"],
            },
            {
                "id": "laravel",
                "name": "Laravel",
                "signatures": ["artisan", "composer.json with laravel/framework"],
            },
            {
                "id": "react",
                "name": "React (Vite/CRA)",
                "signatures": ["vite.config with react plugin", "package.json with react"],
            },
            {
                "id": "vue",
                "name": "Vue.js",
                "signatures": ["vite.config with vue plugin", "package.json with vue"],
            },
            {
                "id": "nuxt",
                "name": "Nuxt.js",
                "signatures": ["nuxt.config.js", "nuxt.config.ts"],
            },
        ]
    }


@mcp.tool
def list_supported_ides() -> dict:
    """
    List all supported IDEs and their steering file formats.
    
    Returns:
        Dictionary of supported IDEs with file path info
    """
    ides = []
    for ide_id, config in IDE_CONFIGS.items():
        ides.append({
            "id": ide_id,
            "description": config["description"],
            "path": config.get("path", "") + config.get("filename", "*.md"),
            "multipleFiles": config.get("multiple_files", False),
        })
    
    return {"ides": ides}


@mcp.tool
def create_custom_steering(
    filename: str,
    content: str,
    inclusion: str = "always",
    file_match_pattern: str | None = None,
    scope: str = "workspace",
) -> dict:
    """
    Create a custom steering file with specified inclusion mode.
    
    Use this to create domain-specific steering files like:
    - api-standards.md - REST conventions, error formats
    - testing-standards.md - Unit test patterns, mocking approaches
    - code-conventions.md - Naming patterns, file organization
    - security-policies.md - Auth requirements, validation rules
    
    Args:
        filename: Name of the steering file (e.g., "api-standards.md")
        content: Markdown content for the steering file
        inclusion: Inclusion mode - "always" (default), "fileMatch", or "manual"
        file_match_pattern: Glob pattern for fileMatch mode (e.g., "app/api/**/*")
        scope: "workspace" (.kiro/steering/) or "global" (~/.kiro/steering/)
    
    Returns:
        Dictionary with file path and wrapped content
    
    Examples:
        # Always included
        create_custom_steering("api-standards.md", "# API Standards\\n...", "always")
        
        # Only when working with API files
        create_custom_steering(
            "api-standards.md", 
            "# API Standards\\n...", 
            "fileMatch", 
            "app/api/**/*"
        )
        
        # Manual inclusion via #api-standards
        create_custom_steering("api-standards.md", "# API Standards\\n...", "manual")
    """
    # Validate inclusion mode
    valid_inclusions = ["always", "fileMatch", "manual"]
    if inclusion not in valid_inclusions:
        inclusion = "always"
    
    # Validate fileMatch has pattern
    if inclusion == "fileMatch" and not file_match_pattern:
        return {
            "error": "fileMatch inclusion requires file_match_pattern parameter",
            "example": 'file_match_pattern="app/api/**/*"'
        }
    
    # Wrap content with front-matter
    wrapped = _wrap_kiro_format(content, inclusion, file_match_pattern)
    
    # Determine path
    if scope == "global":
        path = f"~/.kiro/steering/{filename}"
    else:
        path = f".kiro/steering/{filename}"
    
    return {
        "path": path,
        "content": wrapped,
        "inclusion": inclusion,
        "fileMatchPattern": file_match_pattern,
        "scope": scope,
        "note": "Use fsWrite tool to save this file to the specified path"
    }


@mcp.tool
def get_steering_template(template_type: str) -> dict:
    """
    Get a template for common steering file types.
    
    Args:
        template_type: Type of template - "api", "testing", "security", 
                       "code-style", "deployment", "components"
    
    Returns:
        Template content and suggested filename
    """
    templates = {
        "api": {
            "filename": "api-standards.md",
            "inclusion": "fileMatch",
            "fileMatchPattern": "app/api/**/*",
            "content": """# API Standards

## REST Conventions

- Use plural nouns for resources: `/users`, `/posts`
- Use HTTP methods correctly: GET (read), POST (create), PUT (update), DELETE (remove)
- Return appropriate status codes: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found)

## Response Format

```json
{
  "data": { ... },
  "error": null,
  "meta": { "timestamp": "..." }
}
```

## Error Handling

```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [...]
  }
}
```

## Authentication

- Use Bearer tokens in Authorization header
- Validate tokens on every request
- Return 401 for invalid/expired tokens
"""
        },
        "testing": {
            "filename": "testing-standards.md",
            "inclusion": "fileMatch",
            "fileMatchPattern": "**/*.test.*",
            "content": """# Testing Standards

## Unit Tests

- Test one thing per test
- Use descriptive test names: `should_return_user_when_valid_id`
- Mock external dependencies
- Aim for 80%+ coverage on business logic

## Test Structure

```typescript
describe('ComponentName', () => {
  beforeEach(() => {
    // Setup
  })

  it('should do something when condition', () => {
    // Arrange
    // Act
    // Assert
  })
})
```

## Mocking

- Mock API calls with MSW or similar
- Mock time-dependent functions
- Reset mocks between tests
"""
        },
        "security": {
            "filename": "security-policies.md",
            "inclusion": "always",
            "content": """# Security Policies

## Authentication

- Never store passwords in plain text
- Use secure session management
- Implement rate limiting on auth endpoints

## Data Validation

- Validate all user input on server side
- Sanitize data before database queries
- Use parameterized queries to prevent SQL injection

## Sensitive Data

- Never log sensitive information
- Use environment variables for secrets
- Encrypt sensitive data at rest

## API Security

- Implement CORS properly
- Use HTTPS only
- Validate Content-Type headers
"""
        },
        "code-style": {
            "filename": "code-conventions.md",
            "inclusion": "always",
            "content": """# Code Conventions

## Naming

- Components: PascalCase (`UserProfile`)
- Functions: camelCase (`getUserById`)
- Constants: SCREAMING_SNAKE_CASE (`MAX_RETRIES`)
- Files: kebab-case (`user-profile.tsx`)

## File Organization

- One component per file
- Co-locate tests with source files
- Group by feature, not by type

## Comments

- Explain "why", not "what"
- Use JSDoc for public APIs
- Keep comments up to date

## Error Handling

- Always handle errors explicitly
- Use custom error classes
- Log errors with context
"""
        },
        "deployment": {
            "filename": "deployment-workflow.md",
            "inclusion": "manual",
            "content": """# Deployment Workflow

## Environments

- `development` - Local development
- `staging` - Pre-production testing
- `production` - Live environment

## Build Process

```bash
npm run build      # Build application
npm run test       # Run tests
npm run lint       # Check code quality
```

## Deployment Steps

1. Create PR with changes
2. Pass CI checks
3. Get code review approval
4. Merge to main
5. Auto-deploy to staging
6. Manual promotion to production

## Rollback

- Keep previous 3 deployments
- One-click rollback available
- Monitor error rates post-deploy
"""
        },
        "components": {
            "filename": "component-patterns.md",
            "inclusion": "fileMatch",
            "fileMatchPattern": "components/**/*.tsx",
            "content": """# Component Patterns

## Component Structure

```tsx
// 1. Imports
import { useState } from 'react'
import { cn } from '@/lib/utils'

// 2. Types
interface Props {
  title: string
  onAction?: () => void
}

// 3. Component
export function ComponentName({ title, onAction }: Props) {
  // Hooks first
  const [state, setState] = useState(false)
  
  // Handlers
  const handleClick = () => {
    onAction?.()
  }
  
  // Render
  return (
    <div className="...">
      {title}
    </div>
  )
}
```

## Best Practices

- Keep components small and focused
- Extract reusable logic to hooks
- Use composition over inheritance
- Memoize expensive computations
"""
        }
    }
    
    template = templates.get(template_type)
    if not template:
        return {
            "error": f"Unknown template type: {template_type}",
            "available": list(templates.keys())
        }
    
    return template


def main():
    """Entry point for the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()

# Steering Generator MCP Server

[![PyPI version](https://badge.fury.io/py/steering-generator-mcp.svg)](https://pypi.org/project/steering-generator-mcp/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP Server to auto-generate steering/context docs from codebases — like Kiro IDE's built-in feature, but for **all AI IDEs** (Cursor, VS Code, Windsurf, Cline, Aider, etc).

---

## 🚀 Quick Install

### Option 1: pip install (Recommended)

```bash
pip install steering-generator-mcp
```

Then add to your MCP config:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "steering-generator"
    }
  }
}
```

### Option 2: uvx (No install needed)

If you have [uv](https://docs.astral.sh/uv/getting-started/installation/) installed:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "uvx",
      "args": ["steering-generator-mcp"]
    }
  }
}
```

### Option 3: Python module

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "python",
      "args": ["-m", "steering_generator"]
    }
  }
}
```

---

### Config File Locations

| IDE | Config File |
|-----|-------------|
| **Kiro** | `.kiro/settings/mcp.json` |
| **Cursor** | `.cursor/mcp.json` |
| **VS Code** | `.vscode/mcp.json` |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` |
| **Claude Desktop** | `claude_desktop_config.json` |
| **Cline** | Cline MCP settings in VS Code |

---

## 💬 Usage

Just chat with your AI:

```
"Generate steering docs for this project"
```

Done! AI will generate context files automatically.

---

## What Does It Generate?

### 3 Foundational Steering Files (like Kiro)

| File | Purpose |
|------|---------|
| `product.md` | Product overview, target users, key features, business objectives |
| `tech.md` | Technology stack, frameworks, libraries, dev tools, constraints |
| `structure.md` | File organization, naming conventions, import patterns, architecture |

### Output Formats per IDE

| IDE | Output Location |
|-----|-----------------|
| **Kiro** | `.kiro/steering/*.md` (multiple files) |
| **Cursor** | `.cursor/rules/project.mdc` |
| **GitHub Copilot** | `.github/copilot-instructions.md` |
| **Windsurf** | `.windsurfrules` |
| **Cline** | `.clinerules` |
| **Aider** | `CONVENTIONS.md` |

---

## Supported Frameworks

- ✅ Next.js (App Router & Pages)
- ✅ React (Vite/CRA)
- ✅ Vue.js (Vite)
- ✅ Nuxt.js
- ✅ Laravel 12

---

## Features

### Inclusion Modes

Control when steering files are loaded:

```yaml
---
inclusion: always          # Always loaded (default)
---
```

```yaml
---
inclusion: fileMatch
fileMatchPattern: "app/api/**/*"   # Only when working on matching files
---
```

```yaml
---
inclusion: manual          # On-demand via #steering-file-name
---
```

### File References

Reference other files in your steering docs:

```markdown
#[[file:lib/types.ts]]
#[[file:api/openapi.yaml]]
```

### Custom Steering Templates

Built-in templates for common patterns:
- `api` - REST API standards
- `testing` - Testing conventions
- `security` - Security policies
- `code-style` - Code conventions
- `deployment` - Deployment workflow
- `components` - Component patterns

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `generate_steering` | Generate foundational steering docs |
| `deep_analyze_project` | Deep analysis with categorized deps, patterns, entities |
| `create_custom_steering` | Create custom steering with inclusion mode |
| `get_steering_template` | Get template for common patterns |
| `detect_project_framework` | Detect framework (nextjs/react/vue/laravel) |
| `list_supported_frameworks` | List supported frameworks |
| `list_supported_ides` | List supported IDE output formats |

---

## Example Output

### `.kiro/steering/tech.md`

```markdown
---
inclusion: always
---

# Technology Stack

## Framework & Runtime

- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 19
- **Language**: TypeScript 5

## Database & Backend

- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth

## UI & Styling

- **CSS Framework**: Tailwind CSS
- **Component Library**: shadcn/ui
- **Icons**: Lucide React

## Key Libraries

- **Validation**: Zod
- **Forms**: React Hook Form
- **State**: Zustand

## Development Commands

```bash
npm run dev       # Start dev server
npm run build     # Build for production
```
```

---

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (for `uvx` command) OR pip

### Optional: Ripgrep

For faster scanning on large codebases:

```bash
# Windows
winget install BurntSushi.ripgrep

# Mac
brew install ripgrep

# Linux
sudo apt install ripgrep
```

---

## License

MIT

---

## Links

- [PyPI Package](https://pypi.org/project/steering-generator-mcp/)
- [GitHub Repository](https://github.com/yourusername/steering-generator-mcp)
- [Report Issues](https://github.com/yourusername/steering-generator-mcp/issues)

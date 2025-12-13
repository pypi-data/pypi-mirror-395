# Steering Generator MCP - Development Summary

## Tujuan
Membuat MCP Server yang bisa **auto-generate steering docs** persis seperti fitur bawaan Kiro IDE, tapi untuk **semua AI IDE** (Cursor, GitHub Copilot, Windsurf, Cline, Aider, dll).

## Fitur Utama (Sesuai Kiro Official Docs)

### 3 Foundational Steering Files

| File | Fungsi |
|------|--------|
| `product.md` | Product overview, target users, key features, business objectives |
| `tech.md` | Technology stack, frameworks, libraries, dev tools, constraints |
| `structure.md` | File organization, naming conventions, import patterns, architecture |

### Inclusion Modes

```yaml
# Always included (default)
---
inclusion: always
---

# Conditional - load saat kerja di file tertentu
---
inclusion: fileMatch
fileMatchPattern: "app/api/**/*"
---

# Manual - on-demand via #steering-file-name
---
inclusion: manual
---
```

### File References

```markdown
#[[file:lib/types.ts]]
#[[file:api/openapi.yaml]]
```

## MCP Tools

| Tool | Fungsi |
|------|--------|
| `generate_steering` | Generate 3 foundational steering docs |
| `deep_analyze_project` | Deep analysis dengan categorized deps, patterns, entities |
| `create_custom_steering` | Buat custom steering dengan inclusion mode |
| `get_steering_template` | Get template (api, testing, security, code-style, dll) |
| `detect_project_framework` | Detect framework (nextjs/laravel/react/vue/nuxt) |
| `list_supported_frameworks` | List frameworks yang di-support |
| `list_supported_ides` | List IDE output formats |

## Supported Frameworks
- Next.js (App Router & Pages)
- Laravel 12
- React (Vite/CRA)
- Vue.js (Vite)
- Nuxt.js

## Supported IDE Output Formats

| IDE | Output File |
|-----|-------------|
| Kiro | `.kiro/steering/*.md` (multiple files dengan front-matter) |
| Cursor | `.cursor/rules/project.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurfrules` |
| Cline | `.clinerules` |
| Aider | `CONVENTIONS.md` |
| Generic | `STEERING.md` |

## Arsitektur

```
mcp/steering-generator/
├── pyproject.toml              # Package config
├── README.md                   # Dokumentasi lengkap
├── summary.md                  # File ini
└── steering_generator/
    ├── __init__.py
    ├── server.py               # FastMCP server + 7 tools
    ├── detector.py             # Framework detection
    ├── analyzer.py             # Basic analysis + ripgrep
    ├── deep_analyzer.py        # Deep analysis (deps, patterns, entities)
    └── generator.py            # Generate .md files per IDE format
```

## Cara Install & Pakai

### Install
```bash
cd mcp/steering-generator
pip install -e .
```

### MCP Config (Kiro/Cursor/dll)
```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "python",
      "args": ["-m", "steering_generator"],
      "cwd": "D:/path/to/mcp/steering-generator"
    }
  }
}
```

### Usage di Chat
```
User: "Generate steering docs untuk project ini"
AI: *calls generate_steering(project_path=".", output_format="kiro")*
AI: "Done! Generated:
     - .kiro/steering/product.md
     - .kiro/steering/tech.md
     - .kiro/steering/structure.md"
```

## Output Quality

| File | Quality | Notes |
|------|---------|-------|
| tech.md | ✅ 95% | Hampir identik dengan Kiro |
| structure.md | ✅ 90% | Good dengan naming conventions & import patterns |
| product.md | ⚠️ 70% | Butuh README yang bagus untuk context |

## Tech Stack MCP Ini

- Python 3.10+
- FastMCP 2.x
- pathlib + concurrent.futures
- Optional: ripgrep untuk fast scanning

---

*Updated: December 2024 - Sesuai Kiro Official Steering Docs*

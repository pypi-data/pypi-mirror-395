# Steering Generator MCP Server

MCP Server untuk auto-generate steering/context docs dari codebase — mirip fitur bawaan Kiro IDE, tapi bisa dipakai di **semua AI IDE** (Cursor, GitHub Copilot, Windsurf, Cline, Aider, dll).

## Apa Ini?

MCP ini scan codebase lo, extract info penting (tech stack, types, routes, dll), terus generate "steering docs" yang bisa dibaca AI. Hasilnya: AI jadi lebih akurat karena udah paham context project.

## Foundational Steering Files

Generate 3 file utama (seperti Kiro):

| File | Fungsi |
|------|--------|
| `product.md` | Product overview, target users, key features, business objectives |
| `tech.md` | Technology stack, frameworks, libraries, dev tools, constraints |
| `structure.md` | File organization, naming conventions, import patterns, architecture |

## Inclusion Modes

Steering files bisa dikonfigurasi kapan di-load:

```yaml
---
inclusion: always          # Default - selalu di-load
---
```

```yaml
---
inclusion: fileMatch
fileMatchPattern: "app/api/**/*"   # Conditional - hanya saat kerja di file tertentu
---
```

```yaml
---
inclusion: manual          # On-demand via #steering-file-name
---
```

## File References

Reference file lain dalam steering docs:

```markdown
#[[file:lib/types.ts]]
#[[file:api/openapi.yaml]]
```

---

## Supported Frameworks

- Next.js (App Router & Pages)
- Laravel 12
- React (Vite/CRA)
- Vue.js (Vite)
- Nuxt.js

## Supported IDEs / Output Formats

| IDE | Output File | Format |
|-----|-------------|--------|
| **Kiro** | `.kiro/steering/*.md` | Multiple files dengan front-matter |
| **Cursor** | `.cursor/rules/project.mdc` | Single file |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Single file |
| **Windsurf** | `.windsurfrules` | Single file |
| **Cline** | `.clinerules` | Single file |
| **Aider** | `CONVENTIONS.md` | Single file |
| **Generic** | `STEERING.md` | Single file |

---

## Installation

### Prerequisites

- Python 3.10+
- pip atau uv

### Option 1: Install dari Source (Development)

```bash
cd mcp/steering-generator
pip install -e .

# Test run
steering-generator
```

### Option 2: Run langsung tanpa install

```bash
cd mcp/steering-generator
python -m steering_generator
```

### Optional: Install Ripgrep (Recommended)

Ripgrep bikin scanning 10x lebih cepat untuk codebase besar.

```bash
# Windows
winget install BurntSushi.ripgrep

# Mac
brew install ripgrep

# Linux
sudo apt install ripgrep
```

---

## MCP Configuration

### Kiro IDE

Edit `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "python",
      "args": ["-m", "steering_generator"],
      "cwd": "C:/path/to/mcp/steering-generator"
    }
  }
}
```

### Cursor IDE

Edit `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "python",
      "args": ["-m", "steering_generator"],
      "cwd": "/path/to/mcp/steering-generator"
    }
  }
}
```

---

## Tools Available

### `generate_steering`
Generate foundational steering docs.

```
Input:  { 
  "project_path": ".",
  "output_format": "kiro"  // kiro, cursor, copilot, windsurf, cline, aider, markdown
}
Output: {
  "framework": "nextjs",
  "files": {
    ".kiro/steering/product.md": "---\ninclusion: always\n---\n# Product Overview\n...",
    ".kiro/steering/tech.md": "...",
    ".kiro/steering/structure.md": "..."
  }
}
```

### `deep_analyze_project`
Deep analysis untuk context lengkap.

```
Input:  { "project_path": "." }
Output: {
  "framework": "nextjs",
  "categorizedDependencies": { "Database": [...], "UI & Styling": [...] },
  "architecturePatterns": { "stateManagement": "Zustand", ... },
  "entities": [...],
  "statusEnums": [...]
}
```

### `create_custom_steering`
Buat custom steering file dengan inclusion mode.

```
Input:  { 
  "filename": "api-standards.md",
  "content": "# API Standards\n...",
  "inclusion": "fileMatch",
  "file_match_pattern": "app/api/**/*"
}
Output: {
  "path": ".kiro/steering/api-standards.md",
  "content": "---\ninclusion: fileMatch\nfileMatchPattern: \"app/api/**/*\"\n---\n\n# API Standards\n..."
}
```

### `get_steering_template`
Get template untuk common steering types.

```
Input:  { "template_type": "api" }  // api, testing, security, code-style, deployment, components
Output: {
  "filename": "api-standards.md",
  "inclusion": "fileMatch",
  "fileMatchPattern": "app/api/**/*",
  "content": "# API Standards\n..."
}
```

### `detect_project_framework`
Detect framework dari project.

### `list_supported_frameworks`
List semua framework yang di-support.

### `list_supported_ides`
List semua IDE dan format output.

---

## Example Workflow

### Generate Foundational Docs

```
User: "Generate steering docs untuk project ini"

AI: *calls generate_steering(project_path=".", output_format="kiro")*

AI: "Done! Generated 3 foundational steering files:
     - .kiro/steering/product.md
     - .kiro/steering/tech.md
     - .kiro/steering/structure.md"
```

### Create Custom Steering

```
User: "Buat steering untuk API standards, load hanya saat kerja di API files"

AI: *calls get_steering_template(template_type="api")*
AI: *calls create_custom_steering(
      filename="api-standards.md",
      content="...",
      inclusion="fileMatch",
      file_match_pattern="app/api/**/*"
    )*
AI: *writes file to .kiro/steering/api-standards.md*

AI: "Done! Created api-standards.md with fileMatch inclusion.
     Will auto-load when you work on files in app/api/"
```

---

## Output Example

### `.kiro/steering/tech.md`

```markdown
---
inclusion: always
---

# Technology Stack

This document defines the technology choices for this project.
Use these technologies when generating code and suggestions.

## Framework & Runtime

- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 19
- **Language**: TypeScript 5
- **Runtime**: Node.js 20+

## Database & Backend

- **Database**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth
- **Storage**: Supabase Storage

## UI & Styling

- **CSS Framework**: Tailwind CSS (utility-first)
- **Component Library**: shadcn/ui (built on Radix UI)
- **Icons**: Lucide React

## Key Libraries

- **Validation**: Zod (schema validation)
- **Forms**: React Hook Form
- **Notifications**: Sonner (toast)

## Development Commands

\`\`\`bash
npm run dev       # Start development server
npm run build     # Build for production
npm run lint      # Run linter
\`\`\`

## Environment Variables

Required environment variables (`.env.local`):

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anonymous key (public) |

## Technical Constraints

When generating code, follow these constraints:

- Use Server Components by default, Client Components only when needed
- Prefer Server Actions for mutations
- Use `next/image` for images, `next/link` for navigation
- Follow TypeScript strict mode
```

---

## License

MIT

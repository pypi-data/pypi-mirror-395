# How to Publish to PyPI

## Prerequisites

1. Create account di [PyPI](https://pypi.org/account/register/)
2. Create API token di [PyPI Account Settings](https://pypi.org/manage/account/token/)
3. Install build tools:
   ```bash
   pip install build twine
   ```

## Steps to Publish

### 1. Update Version

Edit `pyproject.toml`:
```toml
version = "0.1.0"  # Increment this
```

### 2. Update Author Info

Edit `pyproject.toml`:
```toml
authors = [
    {name = "Your Name", email = "your@email.com"}
]

[project.urls]
Homepage = "https://github.com/yourusername/steering-generator-mcp"
```

### 3. Build Package

```bash
cd mcp/steering-generator
python -m build
```

This creates:
- `dist/steering_generator_mcp-0.1.0.tar.gz`
- `dist/steering_generator_mcp-0.1.0-py3-none-any.whl`

### 4. Test Upload (Optional)

Upload to TestPyPI first:
```bash
python -m twine upload --repository testpypi dist/*
```

Test install:
```bash
pip install --index-url https://test.pypi.org/simple/ steering-generator-mcp
```

### 5. Upload to PyPI

```bash
python -m twine upload dist/*
```

Enter your PyPI username (`__token__`) and API token when prompted.

### 6. Verify

```bash
pip install steering-generator-mcp
steering-generator --help
```

---

## After Publishing

Users can install with:

```bash
# Option 1: Install globally
pip install steering-generator-mcp

# Option 2: Use with uvx (no install needed)
uvx steering-generator-mcp
```

MCP Config becomes:

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

Or if installed via pip:

```json
{
  "mcpServers": {
    "steering-generator": {
      "command": "steering-generator"
    }
  }
}
```

---

## Updating

1. Increment version in `pyproject.toml`
2. Delete old dist: `rm -rf dist/`
3. Build: `python -m build`
4. Upload: `python -m twine upload dist/*`

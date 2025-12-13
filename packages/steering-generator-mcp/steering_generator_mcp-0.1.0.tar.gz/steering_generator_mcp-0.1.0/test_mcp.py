"""Test script untuk simulasi MCP steering generator."""
import sys
import json

sys.path.insert(0, ".")

from steering_generator.detector import detect_framework
from steering_generator.analyzer import analyze_codebase, has_ripgrep
from steering_generator.generator import generate_steering_docs
from steering_generator.deep_analyzer import deep_analyze_codebase

def main():
    # Get absolute path to workspace root
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.dirname(os.path.dirname(script_dir))  # Go up 2 levels
    print(f"Project path: {project_path}")
    
    print("=" * 50)
    print("STEERING GENERATOR MCP - TEST RUN")
    print("=" * 50)
    print()
    
    # Step 1: Detect framework
    print("=== STEP 1: DETECT FRAMEWORK ===")
    framework = detect_framework(project_path)
    print(f"Detected framework: {framework}")
    print(f"Ripgrep available: {has_ripgrep()}")
    print()
    
    # Step 2: Analyze codebase
    print("=== STEP 2: ANALYZE CODEBASE ===")
    analysis = analyze_codebase(project_path, framework)
    
    tech = analysis.get("techStack", {})
    print(f"Dependencies: {len(tech.get('dependencies', []))}")
    print(f"Dev Dependencies: {len(tech.get('devDependencies', []))}")
    print(f"Types found: {len(analysis.get('types', []))}")
    print(f"Components found: {len(analysis.get('components', []))}")
    print(f"Env vars found: {len(analysis.get('envVars', []))}")
    print(f"Stats: {analysis.get('stats', {})}")
    print()
    
    # Show some details
    if tech.get("dependencies"):
        print("Top dependencies:")
        for dep in tech["dependencies"][:10]:
            print(f"  - {dep}")
        print()
    
    if analysis.get("types"):
        print("Types found:")
        for t in analysis["types"][:5]:
            print(f"  - {t['name']} ({t['kind']})")
        print()
    
    if analysis.get("envVars"):
        print("Env vars:")
        for var in analysis["envVars"][:10]:
            print(f"  - {var}")
        print()
    
    # Step 3: Deep Analysis (NEW!)
    print("=== STEP 3: DEEP ANALYSIS ===")
    deep = deep_analyze_codebase(project_path, framework, analysis)
    
    print("\nCategorized Dependencies:")
    for category, deps in deep.get("categorizedDeps", {}).items():
        print(f"  {category}:")
        for d in deps[:3]:
            purpose = f" - {d['purpose']}" if d.get('purpose') else ""
            print(f"    - {d['name']}{purpose}")
    
    print("\nREADME Info:")
    readme = deep.get("readme", {})
    print(f"  Title: {readme.get('title', 'N/A')}")
    print(f"  Description: {readme.get('description', 'N/A')[:100]}...")
    
    print("\nArchitecture Patterns:")
    patterns = deep.get("patterns", {})
    for key, value in patterns.items():
        if value:
            print(f"  {key}: {value}")
    
    print("\nEntities (detailed):")
    for entity in deep.get("entities", [])[:3]:
        print(f"  {entity['name']}:")
        for field in entity.get("fields", [])[:5]:
            opt = "?" if field.get("optional") else ""
            print(f"    - {field['name']}{opt}: {field['type']}")
    
    print("\nStatus Enums:")
    for enum in deep.get("statusEnums", []):
        print(f"  {enum['name']}: {', '.join(enum['values'])}")
    
    print("\nCode Snippets Available:")
    for key in deep.get("codeSnippets", {}).keys():
        print(f"  - {key}")
    
    # Step 4: Generate steering docs
    print("\n=== STEP 4: GENERATE STEERING DOCS ===")
    
    # Test all formats
    for fmt in ["kiro", "cursor", "copilot", "markdown"]:
        docs = generate_steering_docs(analysis, fmt)
        print(f"\n{fmt.upper()} format:")
        for filename, content in docs.items():
            print(f"  {filename}: {len(content)} chars")
    
    print()
    print("=" * 50)
    print("TEST COMPLETE!")
    print("=" * 50)
    
    # Save deep analysis as JSON
    print("\n\nDEEP ANALYSIS JSON OUTPUT:")
    print("-" * 40)
    # Remove large code snippets for display
    display_deep = {k: v for k, v in deep.items() if k != "codeSnippets"}
    print(json.dumps(display_deep, indent=2, default=str)[:3000])

if __name__ == "__main__":
    main()

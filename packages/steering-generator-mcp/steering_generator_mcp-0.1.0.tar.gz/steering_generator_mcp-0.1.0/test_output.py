"""Test script to show generated steering docs."""
from steering_generator.detector import detect_framework
from steering_generator.analyzer import analyze_codebase
from steering_generator.deep_analyzer import deep_analyze_codebase
from steering_generator.generator import generate_steering_docs_deep
import os

# Test di folder parent (atau current folder)
project_path = "."

# Detect framework
framework = detect_framework(project_path)
print(f"Framework: {framework}")

# Basic analysis
basic = analyze_codebase(project_path, framework)
deps = basic.get("techStack", {}).get("dependencies", [])
print(f"Dependencies found: {len(deps)}")

# Deep analysis
deep = deep_analyze_codebase(project_path, framework, basic)

# Merge
deep["framework"] = framework
deep["scripts"] = basic.get("scripts", {})
deep["envVars"] = basic.get("envVars", [])
deep["components"] = basic.get("components", [])

# Generate docs
docs = generate_steering_docs_deep(deep, "kiro")

print(f"\n=== Generated {len(docs)} files ===\n")

# Save to output folder
os.makedirs("output", exist_ok=True)

for path, content in docs.items():
    filename = path.split("/")[-1]
    output_path = f"output/GENERATED-{filename}"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"--- {path} ---")
    print(content)
    print("\n" + "="*60 + "\n")

print("Files saved to output/ folder")

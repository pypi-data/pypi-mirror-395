"""Quick test - generate and save output."""
import sys
import os

sys.path.insert(0, ".")

from steering_generator.detector import detect_framework
from steering_generator.analyzer import analyze_codebase
from steering_generator.deep_analyzer import deep_analyze_codebase
from steering_generator.generator import generate_steering_docs_deep

# Get project path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(os.path.dirname(script_dir))

print(f"Analyzing: {project_path}")

# Detect & analyze
fw = detect_framework(project_path)
print(f"Framework: {fw}")

basic = analyze_codebase(project_path, fw)
print(f"Basic analysis done")

deep = deep_analyze_codebase(project_path, fw, basic)
print(f"Deep analysis done")

# Merge
deep["framework"] = fw
deep["scripts"] = basic.get("scripts", {})
deep["envVars"] = basic.get("envVars", [])
deep["components"] = basic.get("components", [])

# Generate docs
docs = generate_steering_docs_deep(deep, "kiro")
print(f"\nGenerated {len(docs)} files:")

# Save to output folder
os.makedirs("output", exist_ok=True)

for filepath, content in docs.items():
    # Save with flat name
    filename = filepath.replace(".kiro/steering/", "GENERATED-")
    output_path = f"output/{filename}"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Saved: {output_path} ({len(content)} chars)")

# Print tech.md content
print("\n" + "=" * 50)
print("GENERATED tech.md:")
print("=" * 50)
for filepath, content in docs.items():
    if "tech.md" in filepath:
        print(content)
        break

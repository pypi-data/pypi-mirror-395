import sys
import os
import json

# Add the src directory to sys.path to allow importing cs_framework
# Assuming this script is run from the skill directory or project root
# We try to find the project root relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.cs_framework.tools.architect import generate_concept
except ImportError:
    # Fallback if installed as package
    from cs_framework.tools.architect import generate_concept

if __name__ == "__main__":
    # Simple CLI wrapper for the tool
    # Expecting JSON input from stdin or args if called by Claude
    # For now, let's assume it might be called with args
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--actions", nargs="*")
    parser.add_argument("--events", nargs="*")
    parser.add_argument("--output", default=".")
    
    args = parser.parse_args()
    
    generate_concept(args.name, args.actions, args.events, args.output)

import argparse
import os
import shutil
import sys
# import pkg_resources # Deprecated
import importlib.resources
from .tools.architect import generate_concept
from .tools.speckit_integration import run_integration
from .tools.linter import run_linter
# Import run_scenario_tool from fuzzer script. 
# Since it's not in a package structure that is easily importable relative to here without sys.path hacks or moving it,
# we will try to import it assuming the package structure is preserved.
# The fuzzer script is at src/cs_framework/skills/fuzzer/scripts/run_scenario.py
# This is not ideal for a library. Ideally tools should be in cs_framework.tools.
# For now, we will import it dynamically or assume it's installed.
from .skills.fuzzer.scripts.run_scenario import run_scenario_tool

# For GUI, it's in src/cs_gui/main.py. This is outside cs_framework package usually?
# In setup.py: packages=find_packages(where="src"), package_dir={"": "src"}
# So cs_gui is a top level package.
try:
    from cs_gui.main import run_gui
except ImportError:
    run_gui = None

def install_skills(args):
    target_dir = args.target
    
    # If target is not specified, default to .claude/skills/csfw in the current directory
    if not target_dir:
        target_dir = os.path.join(os.getcwd(), ".claude", "skills", "csfw")

    print(f"Installing Claude Skills to: {target_dir}")

    # Get the path to the bundled skills directory
    try:
        # Modern way using importlib.resources
        # Assuming python 3.9+
        if sys.version_info >= (3, 9):
            source_dir = importlib.resources.files('cs_framework').joinpath('skills')
        else:
            # Fallback for older python or if not installed as package
            source_dir = os.path.join(os.path.dirname(__file__), 'skills')
    except Exception:
        source_dir = os.path.join(os.path.dirname(__file__), 'skills')

    # Convert Traversable to path string if needed
    if hasattr(source_dir, 'joinpath'): 
         # It's a Traversable, we need to iterate or copy from it. 
         # But for simplicity in this script, let's assume file system access or use as_file
         # For now, let's stick to the simple os.path fallback if it's a local script
         pass
    
    # Re-evaluating source_dir for simplicity in this context
    # Since we are likely running from source or simple install
    source_dir_path = str(source_dir)
    if not os.path.exists(source_dir_path):
         # Try relative path
         source_dir_path = os.path.join(os.path.dirname(__file__), 'skills')

    if not os.path.exists(source_dir_path):
        print(f"Error: Skills directory not found at {source_dir_path}")
        sys.exit(1)

    try:
        os.makedirs(target_dir, exist_ok=True)
        # Copy all skill directories
        # We look for directories that contain SKILL.md
        for item in os.listdir(source_dir_path):
            src_item_path = os.path.join(source_dir_path, item)
            if os.path.isdir(src_item_path):
                skill_md = os.path.join(src_item_path, "SKILL.md")
                if os.path.exists(skill_md):
                    dst_item_path = os.path.join(target_dir, item)
                    if os.path.exists(dst_item_path):
                        shutil.rmtree(dst_item_path)
                    shutil.copytree(src_item_path, dst_item_path)
                    print(f"  - Installed skill: {item}")
        
        print("\nSuccess! Skills installed.")
        print("Please restart Claude Desktop to load the new skills.")
        
    except Exception as e:
        print(f"Error installing skills: {e}")
        sys.exit(1)

def scaffold(args):
    generate_concept(
        name=args.name,
        actions=args.actions,
        events=args.events,
        output_dir=args.output
    )

def main():
    parser = argparse.ArgumentParser(description="C-S Framework CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # install-skills command
    parser_skills = subparsers.add_parser("install-skills", help="Install Claude Skills definitions")
    parser_skills.add_argument("--target", help="Target directory for skills (default: ./.claude/skills/csfw)")
    parser_skills.set_defaults(func=install_skills)

    # scaffold command
    parser_scaffold = subparsers.add_parser("scaffold", help="Scaffold a new Concept")
    parser_scaffold.add_argument("name", help="Name of the Concept class")
    parser_scaffold.add_argument("--actions", "-a", nargs="*", help="List of actions")
    parser_scaffold.add_argument("--events", "-e", nargs="*", help="List of events")
    parser_scaffold.add_argument("--output", "-o", default=".", help="Output directory")
    parser_scaffold.set_defaults(func=scaffold)

    # integrate-speckit command
    parser_speckit = subparsers.add_parser("integrate-speckit", help="Integrate CSFW with Spec-Kit")
    parser_speckit.set_defaults(func=lambda args: run_integration())

    # lint command
    parser_lint = subparsers.add_parser("lint", help="Run the CSFW Linter")
    parser_lint.add_argument("--path", default=".", help="Path to scan (default: .)")
    parser_lint.set_defaults(func=lambda args: run_linter(args.path))

    # run-scenario command
    parser_scenario = subparsers.add_parser("run-scenario", help="Run a scenario test")
    parser_scenario.add_argument("setup_file", help="Path to Python file that exports 'runner'")
    parser_scenario.add_argument("scenario_file", help="Path to YAML/JSON scenario file")
    parser_scenario.set_defaults(func=lambda args: run_scenario_tool(args.setup_file, args.scenario_file))

    # gui command
    if run_gui:
        parser_gui = subparsers.add_parser("gui", help="Run the Debugger GUI")
        parser_gui.add_argument("--log", default="execution.ttl", help="Path to the RDF log file")
        parser_gui.set_defaults(func=lambda args: run_gui(args.log))

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

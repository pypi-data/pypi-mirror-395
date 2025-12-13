import sys
import os
import json
import argparse

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.cs_framework.tools.debugger import LogQueryEngine
except ImportError:
    from cs_framework.tools.debugger import LogQueryEngine

def main():
    parser = argparse.ArgumentParser(description="C-S Framework Debugger Tool")
    parser.add_argument("--log_file", required=True, help="Path to the .ttl log file")
    parser.add_argument("--query", required=True, help="SPARQL query to execute")
    
    args = parser.parse_args()
    
    engine = LogQueryEngine(args.log_file)
    results = engine.execute_query(args.query)
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()

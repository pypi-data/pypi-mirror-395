import sys
import os
import json
import argparse
import re

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.cs_framework.tools.debugger import LogQueryEngine
except ImportError:
    from cs_framework.tools.debugger import LogQueryEngine

def analyze_collision_issue(log_file):
    engine = LogQueryEngine(log_file)
    
    # 1. Find all 'moved' events for Pacman
    query = """
    PREFIX cs: <http://cs-framework.org/schema/>
    SELECT ?event ?state WHERE {
        ?event a cs:Event ;
               cs:hasName "moved" ;
               cs:hasState ?state .
    }
    """
    results = engine.execute_query(query)
    
    print("Analyzing Pacman movements...")
    for r in results:
        state_str = r.get("state", "{}").strip('"').replace("'", '"')
        try:
            state = json.loads(state_str)
            if "name" not in state: # Assuming Pacman doesn't have name in payload, Ghost does
                print(f"Pacman moved to: {state}")
                # Check if there was a collision check triggered by this event
                event_uri = r.get("event")
                # Query for actions triggered by this event
                q2 = f"""
                PREFIX cs: <http://cs-framework.org/schema/>
                SELECT ?actionName WHERE {{
                    ?action a cs:Action ;
                            cs:hasName ?actionName ;
                            cs:triggeredBy <{event_uri}> .
                }}
                """
                actions = engine.execute_query(q2)
                action_names = [a["actionName"] for a in actions]
                print(f"  -> Triggered actions: {action_names}")
                
                if "check_collision" in action_names:
                    # Check if collision_detected event followed
                    # This is harder because check_collision emits it, but we don't have direct link from Action to Event in RDF easily without ID
                    # But we can check if ANY collision_detected happened
                    pass
        except json.JSONDecodeError:
            pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log_file", required=True)
    args = parser.parse_args()
    analyze_collision_issue(args.log_file)

if __name__ == "__main__":
    main()

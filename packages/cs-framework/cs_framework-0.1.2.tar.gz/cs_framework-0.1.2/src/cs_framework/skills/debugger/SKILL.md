---
name: Debugger
description: Tools for debugging C-S Framework execution logs (RDF).
version: 1.0.0
---

# Overview
The Debugger skill allows you to query execution logs (RDF/Turtle format) to understand the system's behavior.
The logs contain information about Concepts, Actions, Events, and Synchronizations.

# Usage
Use this skill when you need to investigate:
- Why an event didn't trigger an action.
- The sequence of events leading to a state.
- The state of concepts at a specific point in time.

# Tools

## query_logs
Executes a SPARQL query against the execution log.

**Parameters:**
- `query` (string, required): The SPARQL query.
- `log_file` (string, required): Path to the .ttl log file (e.g., "execution.ttl").

**Common Queries:**

*List all events:*
```sparql
PREFIX cs: <http://cs-framework.org/schema/>
SELECT ?name ?timestamp WHERE {
  ?event a cs:Event ;
         cs:hasName ?name .
}
```

*Find actions triggered by a specific event:*
```sparql
PREFIX cs: <http://cs-framework.org/schema/>
SELECT ?actionName WHERE {
  ?action a cs:Action ;
          cs:hasName ?actionName ;
          cs:triggeredBy ?event .
  ?event cs:hasName "SpecificEventName" .
}
```

**Example:**
```python
query_logs(
    log_file="execution.ttl",
    query="PREFIX cs: <http://cs-framework.org/schema#> SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"
)
```

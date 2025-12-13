---
name: Architect
description: Generates Python code for new C-S Framework Concepts based on natural language specifications.
version: 1.0.0
---

# Overview
The Architect skill helps you scaffold new Concept classes for the C-S Framework. It generates a Python file containing the class definition, action methods, and event documentation.

# Usage
Use this skill when you need to create a new Concept. Provide the concept name, a list of actions, and a list of events.

# Tools

## scaffold_concept
Generates the Python file.

**Parameters:**
- `name` (string, required): The name of the Concept class (e.g., "UserManager").
- `actions` (array of strings, optional): List of action names to generate methods for.
- `events` (array of strings, optional): List of event names this concept will emit.
- `output_dir` (string, optional): Directory to save the file (default: current directory).

**Example:**
```python
scaffold_concept(name="UserManager", actions=["login", "logout"], events=["LoggedIn", "LoggedOut"])
```

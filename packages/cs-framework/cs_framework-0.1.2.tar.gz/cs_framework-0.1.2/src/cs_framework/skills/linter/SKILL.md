---
name: Linter
description: Analyzes C-S Framework projects for structural issues like disconnected events or undefined actions.
version: 1.0.0
---

# Overview
The Linter skill statically analyzes your Python code to ensure your C-S Framework implementation is robust. It checks for:
- **Disconnected Events**: Events that are emitted by a Concept but never used in a Synchronization.
- **Undefined Actions**: Actions referenced in a Synchronization that do not exist in the target Concept.

# Usage
Run this skill on your project source directory to get a report of potential issues.

# Tools

## run_linter
Executes the linter analysis.

**Parameters:**
- `path` (string, required): The root directory of the source code to analyze.

**Example:**
```python
run_linter(path="src")
```

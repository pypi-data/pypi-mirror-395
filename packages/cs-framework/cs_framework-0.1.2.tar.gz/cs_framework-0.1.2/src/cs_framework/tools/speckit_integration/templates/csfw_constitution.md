# Project Constitution

## C-S Framework Integration Rules

You are operating within a project that uses the **Concept-Synchronization Framework (CSFW)**.
You MUST adhere to the following rules when planning and implementing features:

1.  **Architecture Compliance**:
    *   All logic must be encapsulated in **Concepts** (`src/concepts/*.py`).
    *   Concepts communicate ONLY via **Events**.
    *   Interactions between Concepts are defined in **Synchronization Rules** (`src/sync/rules.yaml`).
    *   Do NOT write spaghetti code or tightly coupled classes.

2.  **Tool Usage (Mandatory)**:
    *   **Scaffolding**: When creating a new Concept, you MUST use the Architect Skill:
        `csfw scaffold --name <Name> ...`
    *   **Validation**: After modifying code or rules, you MUST run the Linter Skill:
        `csfw lint --path src/`
    *   **Testing**: Use the Fuzzer Skill for scenario-based testing:
        `csfw run-scenario ...`

3.  **Implementation Flow**:
    *   **Plan Phase**: Define Concepts, Events, and Sync Rules in `plan.md`.
    *   **Task Phase**: Create tasks for scaffolding, implementing logic, and defining sync rules.
    *   **Implement Phase**: Execute the tasks using the CSFW tools.

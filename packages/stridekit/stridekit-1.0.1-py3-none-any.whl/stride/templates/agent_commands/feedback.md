---
description: Apply mid-sprint changes by updating plan/design and logging feedback without altering completed work.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If `$ARGUMENTS` (sprint name and/or feedback details) is not provided:

1. **Auto-Detect Sprint**:
   - Scan `.stride/sprints/` for sprint folders
   - Filter for IN_PROGRESS state: has `implementation.md` but NO `retrospective.md`
   
2. **Sprint Selection Logic**:
   - If exactly ONE in-progress sprint found → use it automatically
   - If MULTIPLE in-progress sprints found → ask:
     ```
     Multiple sprints in progress:
     1. sprint-auth (Authentication system) - 75% complete
     2. sprint-search (Search functionality) - 40% complete
     
     Which sprint needs feedback? (Enter number or name)
     ```
   - If ZERO in-progress sprints found → stop and suggest:
     ```
     No active sprints found. Use `/stride-implement sprint-[name]` to start implementation first.
     ```

3. **Gather Feedback Details** (if not provided):
   - Ask: "What changes or adjustments are needed?"
   - Wait for user to describe:
     - Tasks to add/remove/modify
     - Design changes required
     - Approach adjustments
     - Scope clarifications
   - If feedback is ambiguous → ask ONE clarifying question

4. **Validate Selection**:
   - Confirm sprint exists
   - Confirm sprint is in Implementation Phase
   - Confirm feedback is actionable and clear

5. **Proceed** with resolved sprint name and feedback details

---

**Guardrails**
- `/stride-feedback` is the ONLY command allowed to modify `plan.md` or `design.md` after planning.
- Must never undo, rewrite, or delete previously completed implementation logs.
- All modifications to planning files must respect templates and maintain section boundaries.
- Only adjust tasks, Strides, or design elements necessary to satisfy user feedback.
- Never introduce new tasks unrelated to feedback.
- Do not continue implementation in this command.
- Feedback must be captured as an append-only entry in `implementation.md`.

---

**Steps**

1. **Verify Sprint State**
   - Confirm the sprint has:
     - `proposal.md`
     - `plan.md`
     - `implementation.md`
     - `design.md` (if originally required)
   - Ensure the sprint is in **Implementation Phase**.
   - If the sprint is in Planning, Present, Review, or Complete → deny and suggest the correct command.

2. **Interpret User Feedback**
   - Identify whether feedback affects:
     - Strides (ordering, clarity, missing tasks)
     - Tasks (corrections, additions, removals)
     - Design (architecture, API, data model, security)
   - If feedback is ambiguous, ask **one clarifying question** before editing files.

3. **Update plan.md**
   - Modify ONLY what feedback requires:
     - Add/edit/remove tasks
     - Adjust Stride sequence or scope
     - Clarify tasks with more precise descriptions
   - Ensure:
     - Strides remain sequential
     - Tasks remain atomic and outcome-driven
     - Template structure stays intact
   - Do NOT:
     - Introduce unrelated tasks
     - Reorder Strides without contextual justification

4. **Update design.md (Conditional)**
   Modify design.md ONLY if feedback impacts:
   - Architecture
   - Data flow
   - API contracts
   - Security rules
   - Module boundaries
   - Data models or schemas

   All changes must:
   - Stay high-level (no implementation details)
   - Maintain section boundaries exactly
   - Remain consistent with `.stride/project.md`

5. **Log Feedback in implementation.md**
   Append a log entry using the strict template:

   ```markdown
   ## [Timestamp] Feedback Received
   ### Summary
   - [Short explanation of the feedback]

   ### Changes Applied
   - plan.md: [Description]
   - design.md: [Description or “No changes required”]

   ### Notes
   - [Any clarifications, constraints, or follow-up requirements]
    ```

6. **Reconfirm Stride Integrity**
   After applying feedback:

   * Ensure all existing Strides remain coherent.
   * Ensure each task still maps cleanly to an implementation log.
   * Ensure no Stride or task internally contradicts `.stride/project.md`.

7. **Update `.stride/project.md` (Conditional)**
   
   If feedback reveals **major changes** that affect project-wide understanding, update `.stride/project.md` immediately:
   
   **Triggers for project.md updates:**
   - New domain knowledge discovered (entities, relationships, business rules)
   - Technical constraints identified (library issues, version limits, platform restrictions)
   - Architecture decisions that should be standardized project-wide
   - Risk assumptions proven incorrect or new risks identified
   - Security or compliance requirements changed
   - Performance characteristics that affect project expectations
   
   **Which sections to update:**
   - **Section 7**: Domain entities, relationships, business rules, edge cases
   - **Section 8.1**: Technical constraints (libraries, versions, platforms)
   - **Section 8.2**: Business constraints (deadlines, budget, resources)
   - **Section 8.3**: Operational constraints (offline, hardware, network)
   - **Section 11**: Risk validations, new risks, assumption updates
   
   **Update process:**
   - Read current `.stride/project.md`
   - Navigate to affected section(s)
   - Append new learnings (preserve all existing content)
   - Use traceability format: `- [Description] (sprint-[NAME]): [Details]`
   - Be factual, specific, and actionable
   
   **Log in implementation.md:**
   Under "Changes Applied", add:
   ```
   - project.md: Updated Section [X] - [Brief description]
   ```

8. **Do Not Continue Implementation**

   * After applying feedback, stop.
   * Tell the user:
     **"Feedback applied. Continue with `/stride-implement sprint-[NAME]`."**

---

**When to Trigger**
Trigger this command when user says things like:

* “Change the plan…”
* “Adjust the tasks…”
* “Update the design…”
* “Modify the Stride sequence…”
* “This approach needs to be updated…”
* “We need to add/remove/replace this task…”
* “Revise the architecture for this sprint…”

---

**When NOT to Trigger**

* When user wants to start coding → use `/stride-implement`
* When user wants a new sprint → use `/stride-plan`
* When user wants plan presentation → use `/stride-present`
* After sprint completion → forbidden
* To fix incomplete planning → rerun `/stride-plan` instead

---

**Reference**

* `.stride/project.md` — global constraints & rules
* `.stride/sprints/sprint-[NAME]/plan.md` — Stride & task definitions
* `.stride/sprints/sprint-[NAME]/design.md` — technical blueprint
* `.stride/templates/implementation.md` — append-only logging standard
* Stride Instructions — authoritative phase & template rules

<!-- STRIDE:END -->

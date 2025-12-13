---
description: Execute the sprint by completing Strides in order and updating implementation.md in an append-only log.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If `$ARGUMENTS` (sprint name) is not provided:

1. **Auto-Detection**:
   - Scan `.stride/sprints/` for sprint folders
   - Filter for PLANNED/APPROVED state: has `plan.md` and `design.md` but NO `implementation.md` OR has `implementation.md` with incomplete tasks
   
2. **Selection Logic**:
   - If exactly ONE planned sprint found → use it automatically
   - If MULTIPLE planned sprints found → ask:
     ```
     Multiple sprints ready for implementation:
     1. sprint-auth (Authentication system) - PLANNED
     2. sprint-search (Search functionality) - IN PROGRESS (60% complete)
     
     Which sprint should I implement? (Enter number or name)
     ```
   - If ZERO planned sprints found → stop and suggest:
     ```
     No sprints ready for implementation. Use `/stride-plan [description]` to create one first.
     ```

3. **Validate Selection**:
   - Confirm sprint exists
   - Confirm sprint has `plan.md` with defined Strides
   - Confirm `/stride-present` was completed (user reviewed the plan)
   - If not presented → stop and suggest: "Run `/stride-present sprint-[name]` to review before implementing"

4. **Proceed** with resolved sprint name

---

**Guardrails**
- Implementation MUST follow the sequence defined in `plan.md`. No skipping or reordering Strides.
- All changes MUST be documented in `implementation.md` using append-only logs.
- Do NOT modify `proposal.md`, `plan.md`, or `design.md` during implementation.
- Only `/stride-feedback` may alter planning or design files mid-sprint.
- Never generate new sections or remove template sections in implementation.md.
- Code changes must follow project rules defined in `.stride/project.md`.
- If a task is unclear, stop and request clarification before proceeding.

---

**Steps**

1. **Validate Sprint Readiness**  
   - Confirm existence of:  
     - `proposal.md`  
     - `plan.md`  
     - `implementation.md`  
     - `design.md` (if required for this sprint)  
   - Ensure `/stride-present` has been completed and user has explicitly approved implementation.

2. **Load Strides from plan.md**  
   - Parse the list of Strides defined in `## Strides (Sub-Tasks)` section.  
   - Ensure each Stride contains measurable tasks.  
   - If tasks are missing, incomplete, or ambiguous → stop and request `/stride-feedback`.

3. **Execute Strides Sequentially**  
   For each Stride:  
   - Read the Stride description and its tasks.  
   - Perform the work one task at a time.  
   - After each task, write a new append-only entry in `implementation.md` using the template:

     ```markdown
     ## [Timestamp] Stride: [Stride Name]
     ### Decisions
     - [Decision]: [Reasoning]

     ### Notes
     - [Observations, clarifications, blockers]

     ### Changes Made
     - file/path: summary of change
     ```

4. **Respect Task Boundaries**  
   - Each task must produce one or more log entries.  
   - Do NOT merge multiple Strides or tasks into a single entry.  
   - Do NOT generate large code dumps—summaries only.

5. **Validate Work Against Project Context**  
   - Continuously verify compliance with `.stride/project.md` rules:  
     - Coding conventions  
     - Architectural constraints  
     - Testing expectations  
     - Security and reliability rules  
   - If implementation requires context beyond the plan → pause and request `/stride-feedback`.

6. **Track Blockers if Encountered**  
   - If a task cannot proceed due to ambiguity, missing context, or conflict:  
     - Add a log entry: “**Blocker Encountered**”  
     - Describe issue factually  
     - Stop and request clarification

7. **Complete All Strides Before Finishing**  
   - Ensure every Stride and every task has a corresponding log.  
   - Confirm no pending tasks remain.  
   - At the end of the final Stride, write a log entry:  
     *“All Strides completed successfully.”*

8. **Prompt Next Steps**  
   After finishing all tasks, instruct the user to run:  
   - `/stride-review sprint-[NAME]`  
   to begin validation.

---

**When to Trigger**  
Trigger when user says:  
- “Start implementation”  
- “Begin coding”  
- “Execute the sprint”  
- “Work through the Strides”  
- “Proceed with tasks”  
- “Implement the plan”  

---

**When NOT to Trigger**
- When plan is incomplete or not approved (use `/stride-present` first)  
- When user wants to modify tasks or strategy (use `/stride-feedback`)  
- When sprint is already completed  
- When doing review (use `/stride-review`)  
- When project is not initialized (`/stride-init` required)

---

**Reference**
- `.stride/project.md` — authoritative project contract  
- `.stride/sprints/sprint-[NAME]/plan.md` — tasks & Strides  
- `.stride/sprints/sprint-[NAME]/design.md` — architectural intentions  
- `.stride/templates/implementation.md` — logging template  
- Stride Instructions — implementation semantics & restrictions

<!-- STRIDE:END -->

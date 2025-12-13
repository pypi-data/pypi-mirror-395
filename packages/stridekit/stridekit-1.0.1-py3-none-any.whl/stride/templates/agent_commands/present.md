---
description: Present the sprint plan, Strides, and design for user approval before implementation.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If `$ARGUMENTS` (sprint name) is not provided:

1. **Auto-Detection**:
   - Scan `.stride/sprints/` for sprint folders
   - Filter for PLANNED state: has `plan.md` and `design.md` but NO `implementation.md`
   
2. **Selection Logic**:
   - If exactly ONE planned sprint found → use it automatically
   - If MULTIPLE planned sprints found → ask:
     ```
     Multiple planned sprints available:
     1. sprint-auth (Authentication system)
     2. sprint-search (Search functionality)
     
     Which sprint should I present? (Enter number or name)
     ```
   - If ZERO planned sprints found → stop and suggest:
     ```
     No planned sprints found. Use `/stride-plan [description]` to create one first.
     ```

3. **Validate Selection**:
   - Confirm sprint exists
   - Confirm sprint has `plan.md` and `design.md`
   - If incomplete → stop and suggest: "Re-run `/stride-plan sprint-[name]` to complete planning"

4. **Proceed** with resolved sprint name

---

**Guardrails**
- `/stride-present` is a **read-only** command. It must never modify sprint files.
- Only summarize and present existing content from `proposal.md`, `plan.md`, and `design.md`.
- Never begin implementation or generate code during this command.
- Approval must be explicit; do not assume the user wants to proceed.
- If the sprint files are missing or incomplete, stop and request correction before presenting.

---

**Steps**

1. **Locate Sprint Directory**  
   - Resolve the sprint via the argument (e.g., `sprint-auth`, `sprint-api`, etc.).  
   - Validate existence of:  
     - `proposal.md`  
     - `plan.md`  
     - `design.md` (if required by planning phase)  

2. **Verify Planning Completeness**  
   - Ensure `proposal.md` contains **Why**, **What**, acceptance criteria.  
   - Ensure `plan.md` contains **Strides**, **Tasks**, **Approach**, **Risks**, and **Validation Plan**.  
   - Ensure `design.md` exists if project context or plan indicated architectural impact.  
   - If any file is incomplete or missing, return a corrective instruction for the user or agent.

3. **Summarize the Sprint**  
   Present a concise but complete summary of:  
   - Purpose (from proposal)  
   - Scope and acceptance criteria  
   - Defined Strides (with outcomes)  
   - Architectural decisions (from design.md)  
   - Risks and expected challenges  
   - Validation strategy  

4. **Present Strides Sequentially**  
   - Display Stride-by-Stride:  
     - Stride name  
     - Intended outcome  
     - Task list  
   - DO NOT modify the tasks.  
   - DO NOT reinterpret or reorder Strides.

5. **Request Explicit User Approval**  
   After presenting:  
   - Ask: **“Approve to proceed with implementation?”**  
   - Wait for a clear affirmative response.  
   - Only `/stride-implement` or `/stride-feedback` may follow approval.

6. **Handle Feedback or Clarification Requests**  
   - If user requests changes → Do NOT modify files in this command.  
   - Instead, instruct to run `/stride-feedback` for plan/design updates.

---

**When to Trigger**  
The command MUST trigger when the user says:  
- “Show me the sprint”  
- “Present the plan”  
- “Walk me through the strategy”  
- “Explain the Strides”  
- “Let me review the plan before coding”  

---

**When NOT to Trigger**
- During implementation (`/stride-implement`)  
- After sprint completion (`/stride-complete`)  
- When no sprint folder exists  
- When plan is incomplete  
- When user wants changes (use `/stride-feedback`)  

---

**Reference**
- `.stride/project.md` — context for validating planning alignment.
- `.stride/sprints/sprint-[NAME]/proposal.md` — sprint goals & acceptance criteria.
- `.stride/sprints/sprint-[NAME]/plan.md` — Strides, tasks, approach, risks.
- `.stride/sprints/sprint-[NAME]/design.md` — architecture, data flow, API contracts.
- Stride Instructions — for lifecycle sequencing and approval rules.

<!-- STRIDE:END -->

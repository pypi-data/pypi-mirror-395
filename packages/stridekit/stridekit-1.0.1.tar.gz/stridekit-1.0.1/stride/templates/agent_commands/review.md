---
description: Validate sprint output against plan, design, and project rules. This is a read-only review phase.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If `$ARGUMENTS` (sprint name) is not provided:

1. **Auto-Detection**:
   - Scan `.stride/sprints/` for sprint folders
   - Filter for READY_FOR_REVIEW state: has `implementation.md` with all tasks complete, NO `retrospective.md`
   - Check `plan.md` for total Strides count
   - Check `implementation.md` for completed Stride logs
   - Consider ready if: `completed_strides == total_strides`
   
2. **Selection Logic**:
   - If exactly ONE sprint ready for review found → use it automatically
   - If MULTIPLE sprints ready for review found → ask:
     ```
     Multiple sprints ready for review:
     1. sprint-auth (Authentication system) - All 5 Strides complete
     2. sprint-search (Search functionality) - All 4 Strides complete
     
     Which sprint should I review? (Enter number or name)
     ```
   - If ZERO sprints ready → stop and suggest:
     ```
     No sprints ready for review. Continue implementation with `/stride-implement [sprint-name]`
     ```

3. **Validate Selection**:
   - Confirm sprint exists
   - Confirm all required files present (proposal, plan, design, implementation)
   - Confirm implementation appears complete
   - If incomplete → inform user of completion status and suggest continuing implementation

4. **Proceed** with resolved sprint name

---

**Guardrails**
- `/stride-review` is a **strictly read-only** command. No sprint files may be modified.
- Never update `plan.md`, `design.md`, or `implementation.md` during review.
- Findings must be reported, not corrected. Corrections happen only via `/stride-feedback` or `/stride-implement` (if approved).
- All evaluations must reference `.stride/project.md` rules, acceptance criteria, and sprint definitions.
- Never generate new tasks or Strides; only verify existing ones.

---

**Steps**

1. **Verify Sprint Readiness**
   - Ensure required files exist:  
     - `proposal.md`  
     - `plan.md`  
     - `design.md` (if required)  
     - `implementation.md`  
   - Ensure sprint is NOT in Planning or Presentation phase.  
   - Implementation must be complete before review begins.

2. **Load All Sprint Documents**
   - Read and analyze:  
     - Goals & acceptance criteria from `proposal.md`  
     - Strides & tasks from `plan.md`  
     - Architectural constraints from `design.md`  
     - Execution logs from `implementation.md`  
     - Global rules from `.stride/project.md`

3. **Check Proposal Alignment**
   - Confirm all acceptance criteria listed in `proposal.md` were addressed.
   - Identify any criteria that:  
     - were partially met  
     - were unmet  
     - were contradicted by implementation

4. **Check Plan & Stride Completion**
   - Confirm every Stride in `plan.md` has:  
     - Full task completion  
     - At least one implementation log entry  
     - No skipped or out-of-order Strides  
   - Identify:  
     - Missing tasks  
     - Tasks without logs  
     - Logs referencing tasks that do not exist  

5. **Validate Design Integrity**
   - Ensure implementation aligns with:  
     - Architecture  
     - APIs  
     - Data structures  
     - Security rules  
     - Cross-cutting constraints  
   - Highlight mismatches or deviations requiring resolution.

6. **Review Implementation Logs**
   - Ensure logs follow required template sections:  
     - Decisions  
     - Notes  
     - Changes Made  
   - Ensure logs are append-only, chronological, and free of speculative content.
   - Identify:  
     - Missing logs  
     - Logs with unclear work summaries  
     - Incomplete or incorrect formatting

7. **Check Against Project-Level Rules**
   Validate adherence to `.stride/project.md`:  
   - Coding conventions  
   - Testing strategy  
   - Architecture rules  
   - Security & compliance requirements  
   - Constraints & domain logic  
   Flag any violations.

8. **Generate a Discrepancy Report**
   Provide a structured report:

   ```markdown
   # Review Report: sprint-[NAME]

   ## Summary
   - Overall assessment: [Pass / Needs Fixes]

   ## Proposal Alignment
   - [✓/✗] Acceptance criteria met / unmet

   ## Stride Completion
   - [✓/✗] All Strides completed correctly
   - Missing tasks: [...]
   - Missing logs: [...]

   ## Design Compliance
   - [✓/✗] Implementation matches architectural expectations
   - Issues: [...]

   ## Project Rule Compliance
   - [✓/✗] Coding standards followed
   - [✓/✗] Testing & quality gates satisfied
   - Issues: [...]

   ## Required Fixes
   - [List of fixes needed before completion]
```

9. **Ask for Next Action**

   * If issues exist:
     **“Corrections required. Use `/stride-feedback sprint-[NAME]` to apply changes.”**
   * If clean:
     **“Review passed. You may now run `/stride-complete sprint-[NAME]`.”**

---

**When to Trigger**
This command should run when user says:

* “Review the sprint…”
* “Evaluate the work…”
* “Validate everything before completion…”
* “Check if the sprint is ready…”
* “Perform a full review…”
* “Run the Stride review phase…”

---

**When NOT to Trigger**

* During planning (use `/stride-plan`)
* Before approval (use `/stride-present`)
* When applying changes (use `/stride-feedback`)
* When starting implementation (use `/stride-implement`)
* After completion (invalid)
* When project is not initialized (`/stride-init` required)

---

**Reference**

* `.stride/project.md` — global rules & constraints
* `proposal.md` — sprint intent & acceptance criteria
* `plan.md` — Strides & task definitions
* `design.md` — architectural blueprint
* `implementation.md` — execution log
* Stride Instructions — lifecycle & template boundaries
* `stride validate <sprint>` (CLI) — external validation tool

<!-- STRIDE:END -->



---
description: Finalize sprint with retrospective and update project context based on learnings.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If `$ARGUMENTS` (sprint name) is not provided:

1. **Auto-Detection**:
   - Scan `.stride/sprints/` for sprint folders
   - Filter for REVIEWED state: has `implementation.md` with all tasks complete, `/stride-review` was run successfully, NO `retrospective.md`
   - To detect reviewed status, check for recent review validation (all acceptance criteria met)
   
2. **Selection Logic**:
   - If exactly ONE reviewed sprint found → use it automatically
   - If MULTIPLE reviewed sprints found → ask:
     ```
     Multiple reviewed sprints ready for completion:
     1. sprint-auth (Authentication system) - Review passed
     2. sprint-search (Search functionality) - Review passed
     
     Which sprint should I complete? (Enter number or name)
     ```
   - If ZERO reviewed sprints found → stop and suggest:
     ```
     No reviewed sprints found. Use `/stride-review [sprint-name]` to review a sprint first.
     ```

3. **Validate Selection**:
   - Confirm sprint exists
   - Confirm `/stride-review` was completed successfully (no open issues)
   - Confirm all Strides are checked off in `plan.md`
   - If issues remain → stop and suggest: "Resolve review issues with `/stride-feedback` first"

4. **Proceed** with resolved sprint name

---

**Guardrails**
- `/stride-complete` may ONLY be run after ALL Strides in `plan.md` are checked off.
- Must generate `retrospective.md` using `.stride/templates/retrospective.md`.
- Must review `.stride/project.md` and update if sprint learnings affect project-wide understanding.
- Must not add new implementation work.
- Must not modify previous logs in `implementation.md`.

---

**Steps**

1. **Verify Sprint Completion**
   - All tasks in `plan.md` are checked: `- [x]`
   - `implementation.md` has logs for all Strides
   - `/stride-review` has been run successfully
   - All acceptance criteria from `proposal.md` are satisfied

2. **Analyze Sprint Learnings**
   Review `implementation.md` for insights that affect:
   - Domain knowledge (new entities, rules, relationships)
   - Technical constraints (library issues, version requirements)
   - Architecture patterns (established or avoided)
   - Performance characteristics (measured benchmarks)
   - Security considerations (vulnerabilities, patterns)
   - Risk assumptions (validated or invalidated)

3. **Update `.stride/project.md` (Conditional)**
   
   If sprint revealed project-level insights:
   
   **When to update which section:**
   - **Section 1-2**: Rarely (only if project purpose/scope fundamentally changed)
   - **Section 3**: Performance, reliability, security learnings
   - **Section 7**: New domain entities, business rules, edge cases discovered
   - **Section 8**: New constraints discovered (technical, business, operational)
   - **Section 9**: Changes to external dependencies, rate limits, auth mechanisms
   - **Section 11**: Risk validations, new risks identified, assumption updates
   
   **How to update:**
   - Read current section content in `.stride/project.md`
   - Append new learnings (never delete existing content)
   - Use traceability format: `- [Description] (sprint-[NAME]): [Details]`
   - Be clear, factual, and actionable
   
   **Example update to Section 7:**
   ```
   - **User-Session Relationship** (sprint-auth-refactor): Users may have multiple concurrent sessions; session tokens expire after 24h of inactivity.
   ```

4. **Generate `retrospective.md`**
   
   Use template from `.stride/templates/retrospective.md`:
   
   - **What Worked**: Specific Strides, decisions, tools that succeeded
   - **What Didn't**: Blockers, failures, bottlenecks with references
   - **Lessons Learned**: Actionable insights for future sprints
   - **Recommendations**: Process or technical improvements
   - **Project Context Updates**: Document all project.md changes made
     - List each section updated
     - Explain what was added and why
     - Reference specific Strides or implementation decisions

5. **Provide Completion Summary**
   
   Display in chat:
   - Sprint name and status (COMPLETED)
   - Strides completed (count)
   - Files generated
   - project.md sections updated (if any)
   - Key learnings summary (2-3 sentences)

---

**When to Trigger**

Trigger when user says:
- "Complete the sprint"
- "Finalize this"
- "Wrap up"
- "Generate retrospective"
- "Mark as done"
- "Finish the sprint"

---

**When NOT to Trigger**

- Tasks still incomplete → use `/stride-implement`
- Need to add work → use `/stride-feedback`
- Need validation → use `/stride-review`
- Starting new sprint → use `/stride-plan`

---

**Reference**

- `.stride/project.md` — project-wide context
- `.stride/templates/retrospective.md` — retrospective format
- `.stride/sprints/sprint-[NAME]/implementation.md` — learning source
- Stride Instructions — phase rules

<!-- STRIDE:END -->

---
description: Provide deep conversational project status with progress, blockers, and recommendations.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Guardrails**
- `/stride-status` is **read-only** - never modifies files.
- Provides conversational analysis, not tabular output.
- Must parse implementation.md for accurate progress calculation.
- Must identify blockers from implementation logs.
- Must generate actionable recommendations based on project state.
- Output must be prose format, not structured data or tables.

---

**Steps**

1. **Validate Project Context**  
   - Check if `.stride/project.md` exists.  
   - If missing → stop and suggest: "Run `/stride-init` to initialize the project first."  
   - If present → proceed to analyze sprints.

2. **Scan Sprint Directory**  
   - Read `.stride/sprints/` directory for all sprint folders.  
   - Get list of sprint IDs (folder names).  
   - If no sprints exist → inform user: "No sprints found. Use `/stride-derive` for ideas or `/stride-plan` to create a sprint."

3. **Analyze Each Sprint**  
   For each sprint folder:
   
   **a) Determine Lifecycle Phase**:
   - Check file existence to determine status:
     - Has `retrospective.md` → COMPLETED
     - Has `implementation.md` → ACTIVE
     - Has `plan.md` → PROPOSED
     - Only `proposal.md` → PROPOSED
   
   **b) For ACTIVE Sprints, Calculate Progress**:
   - **Parse `plan.md`**:
     - Find section: `## Strides (Sub-Tasks)` or `## Strides`
     - Count numbered Stride items (e.g., "1. **Stride 1:**", "2. **Stride 2:**")
     - Store as `total_strides`
   
   - **Parse `implementation.md`**:
     - Find all log entries with pattern: `## [Timestamp] Stride: [Name]`
     - Extract unique Stride names from logs
     - Count unique Strides that have been logged
     - Store as `completed_strides`
   
   - **Calculate Completion**:
     ```
     completion_percentage = (completed_strides / total_strides) × 100
     ```
   
   - **Extract Current Stride**:
     - Find the most recent log entry in implementation.md
     - Extract the Stride name from that entry
   
   **c) Identify Blockers**:
   - Scan `implementation.md` for blocker keywords:
     - "blocker"
     - "blocked"
     - "cannot proceed"
     - "waiting for"
     - "needs clarification"
     - "dependency missing"
     - "requires [something] before"
   
   - When found, extract:
     - Which Stride the blocker is in
     - Description of the blocker (surrounding context)
     - When it was logged (timestamp)
   
   **d) Check Staleness**:
   - Get last modification time of sprint folder
   - Calculate: `days_since_update = (today - last_modified).days`
   - If `days_since_update > 7` → mark as STALE

4. **Calculate Project Health**  
   
   Determine overall project health status:
   
   ```
   IF any active sprint has blockers:
       health = "Blocked 🚫"
   ELSE IF stale_sprint_count > 2:
       health = "At Risk ⚠️"
   ELSE IF active_sprint_count == 0 AND proposed_sprint_count > 5:
       health = "At Risk ⚠️" (too much planning, not enough execution)
   ELSE:
       health = "Healthy ✅"
   ```
   
   Also calculate:
   - Total sprints by status (proposed, active, review, completed)
   - Average completion percentage across active sprints
   - Number of blocked sprints
   - Number of stale sprints

5. **Generate Recommendations**  
   
   Based on analysis, create actionable recommendations:
   
   **Rule 1: Blocked Sprints**
   ```
   FOR each sprint with blockers:
       ADD "Resolve blocker in {sprint_id}: {blocker_description}"
       ADD suggested action (e.g., "Use /stride-feedback to adjust" or "Request missing resource")
   ```
   
   **Rule 2: High-Completion Sprints**
   ```
   FOR each active sprint where completion > 90%:
       ADD "Run `/stride-review {sprint_id}` - sprint is 90%+ complete"
   ```
   
   **Rule 3: Stale Sprints**
   ```
   FOR each stale sprint (> 7 days):
       ADD "{sprint_id} has no updates in {days} days - consider `/stride-feedback` or `/stride-complete`"
   ```
   
   **Rule 4: No Active Work**
   ```
   IF active_sprint_count == 0 AND proposed_sprint_count > 0:
       ADD "No active sprints. Consider starting: {list first 3 proposed sprint names}"
   ```
   
   **Rule 5: Capacity Planning**
   ```
   IF active_sprint_count > 3:
       ADD "High number of active sprints ({count}). Consider focusing on fewer sprints for better velocity."
   ```

6. **Format Conversational Output**  
   
   Structure the response as natural prose:
   
   ```
   Project Health: {status} {emoji}
   
   Active Sprints ({count}):
   
   {sprint_id} is {completion}% complete
   - Currently on Stride {current}/{total}: "{stride_name}"
   - {blocker_status: "No blockers" or "⚠️ Blocker: {description}"}
   - Next: {suggested_action}
   
   [Repeat for each active sprint]
   
   Proposed Sprints ({count}):
   {comma-separated list of sprint names}
   
   Completed Recently:
   - {sprint_name} ({days} days ago)
   - {sprint_name} ({days} days ago)
   - {sprint_name} ({days} days ago)
   
   Recommendations:
   1. {recommendation_1}
   2. {recommendation_2}
   3. {recommendation_3}
   ```
   
   **Formatting Rules**:
   - Use emojis: ✅ (healthy), ⚠️ (warning), 🚫 (blocked)
   - Write in complete sentences, not bullet points for sprint descriptions
   - Be specific about percentages and Stride names
   - Highlight blockers prominently
   - Keep recommendations actionable and specific

7. **Present to User**  
   - Output the formatted conversational status
   - Use natural language throughout
   - Be encouraging and constructive
   - End with a question if appropriate (e.g., "Would you like details on any specific sprint?")

---

**When to Trigger**  

The command MUST trigger when the user says:
- "How's the project going?"
- "What's the status?"
- "Show me project health"
- "Any blockers?"
- "What needs attention?"
- "Which sprint should I focus on?"
- "Give me an update"
- "Project status"

---

**When NOT to Trigger**

- When user is focused on implementation work (don't distract)
- When creating new sprints (use `/stride-plan`)
- For quick file checks (not needed)
- During `/stride-implement` phase (stay focused on current work)

---

**Output Example**

```
Project Health: Healthy ✅

Active Sprints (2):

sprint-auth is 85% complete
- Currently on Stride 3 of 4: "Add JWT validation middleware"
- No blockers, progressing well
- Next: Complete validation logic, then ready for /stride-review

sprint-ui-polish is 40% complete
- Currently on Stride 2 of 5: "Implement responsive layout system"
- ⚠️ Blocker: Missing design specifications for mobile breakpoints
- Next: Request design specs from team or use /stride-feedback to adjust approach

Proposed Sprints (3):
sprint-api-docs, sprint-error-handling, sprint-performance

Completed Recently:
- sprint-database-setup (2 days ago)
- sprint-user-model (5 days ago)
- sprint-init-config (7 days ago)

Recommendations:
1. Focus on resolving blocker in sprint-ui-polish (request mobile design specs)
2. sprint-auth will be ready for /stride-review in the next session
3. Plan to start one of the proposed sprints after auth completes

Would you like me to dive deeper into any specific sprint?
```

---

**Rules**

- MUST be read-only (no file modifications)
- MUST parse `plan.md` for total Strides count
- MUST parse `implementation.md` for completed Strides and blockers
- MUST calculate accurate completion percentages
- MUST identify all blockers using keyword search
- MUST generate specific, actionable recommendations
- Output MUST be conversational prose (not tables or structured data)
- MUST include emojis for clarity (✅ ⚠️ 🚫)
- MUST be encouraging and constructive in tone

---

**Reference**

- `.stride/project.md` — project context (verify exists)
- `.stride/sprints/` — all sprint folders to analyze
- `plan.md` — total Strides count for progress calculation
- `implementation.md` — completed Strides logs and blocker identification
- Stride Instructions — for understanding sprint lifecycle phases

<!-- STRIDE:END -->

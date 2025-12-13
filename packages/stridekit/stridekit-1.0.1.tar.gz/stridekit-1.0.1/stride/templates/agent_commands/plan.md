---
description: Create a comprehensive sprint plan with proposal, plan, and design documents.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If `$ARGUMENTS` is not provided or is unclear:

1. **Check for Natural Language Description**:
   - If user provided a feature description (e.g., "add user authentication with JWT"), extract the core concept
   - Derive a short, relevant sprint name (4-12 chars) from the description
   - Examples:
     - "add user authentication with JWT" → `sprint-auth-jwt`
     - "implement search functionality" → `sprint-search`
     - "refactor database layer" → `sprint-db-refactor`

2. **If No Description Provided**:
   - Ask: "What feature or capability should we plan for this sprint?"
   - Wait for user response with feature description
   - Derive sprint name from response

3. **Generate Sprint Name**:
   - Format: `sprint-[shortname]` where shortname is 4-12 chars
   - Use lowercase, hyphens for spaces
   - Make it domain-relevant and memorable
   - Ensure uniqueness by checking `.stride/sprints/` directory

4. **Confirm with User**:
   - Present: "Planning sprint-[name] for [feature description]. Proceed?"
   - Wait for confirmation
   - If user wants different name, adjust accordingly

5. **Validate**:
   - Ensure sprint name doesn't already exist in `.stride/sprints/`
   - If exists, suggest: `sprint-[name]-v2` or ask for alternative

---

**Guardrails**
- Must have `.stride/project.md` before creating any sprint
- Sprint name must be 4-12 chars, lowercase, hyphen-separated
- Must create all three files: proposal.md, plan.md, design.md
- Must use templates from `.stride/templates/`
- Must follow project constraints from `.stride/project.md`

---

**Steps**

1. **Validate Project Context**
   - Verify `.stride/project.md` exists
   - If missing, stop and instruct: "Run `/stride-init` first"
   - Read all 11 sections to understand project scope and constraints

2. **Resolve Sprint Name** (use Argument Resolution above)

3. **Create Sprint Directory**
   - Create `.stride/sprints/sprint-[name]/`
   - Ensure uniqueness

4. **Generate proposal.md**
   - Use template from `.stride/templates/proposal.md`
   - Fill in:
     - **What**: Feature/capability description
     - **Why**: Business value, problem solved
     - **Acceptance Criteria**: Measurable success conditions
   - Align with Section 1-2 of project.md (purpose and scope)

5. **Generate plan.md**
   - Use template from `.stride/templates/plan.md`
   - Define:
     - **Strides**: Sequential sub-tasks (3-7 strides typical)
     - **Tasks**: Atomic, outcome-driven actions per stride
     - **Approach**: Technical strategy
     - **Risks**: Potential blockers
     - **Validation Plan**: How to verify success
   - Follow Section 6 conventions and Section 8 constraints

6. **Generate design.md**
   - Use template from `.stride/templates/design.md`
   - Include:
     - **Architecture**: Component structure
     - **Data Flow**: How data moves through system
     - **API Contracts**: Interfaces and signatures
     - **Security**: Auth, validation, encryption needs
   - Stay high-level (no implementation details)
   - Align with Section 4 (architecture) and Section 8.1 (technical constraints)

7. **Validate Planning Completeness**
   - All three files created
   - No placeholder or TODO markers
   - Strides are sequential and atomic
   - Design aligns with project.md architecture

8. **Guide Next Steps**
   - Inform user: "Sprint planned successfully!"
   - Suggest: "Run `/stride-present sprint-[name]` to review before implementation"

---

**When to Trigger**

Trigger when user says:
- "Plan a sprint for..."
- "Create a sprint to..."
- "Let's plan [feature]"
- "I want to build..."
- "/stride-plan [description]"

---

**When NOT to Trigger**

- When `.stride/project.md` doesn't exist (use `/stride-init`)
- When user wants to see potential sprints (use `/stride-derive`)
- During active implementation (use `/stride-feedback` for changes)
- When sprint already exists (suggest different name or version)

---

**Reference**

- `.stride/project.md` — authoritative project context
- `.stride/templates/` — proposal, plan, design templates
- Stride Instructions — sprint naming and structure conventions

<!-- STRIDE:END -->

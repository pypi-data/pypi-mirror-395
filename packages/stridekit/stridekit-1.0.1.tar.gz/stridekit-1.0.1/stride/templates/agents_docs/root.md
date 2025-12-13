<!-- STRIDE:START -->
# Stride Instructions

These instructions are for AI coding assistants working in this project.

**🛑 STOP & READ:** Before starting any task, you MUST read the full guidelines in:
👉 `.stride/AGENTS.md`

**When to consult the full guidelines:**
- **Starting a new feature?** → You need to run `/stride-plan`
- **Writing code?** → You need to update `implementation.md` via `/stride-implement`
- **Finished a task?** → You need to run `/stride-review`
- **Unsure of the process?** → The workflow is strictly defined in `.stride/AGENTS.md`

**Core Workflow:**

1. **🗣️ Talk (Discussion)**
   - Understand the goal.
   - Ask clarifying questions.
   - *Do not write code yet.*

2. **📅 Plan (Design)**
   - Run `/stride-plan` to generate sprint docs.
   - Create `proposal.md`, `plan.md`, and `design.md`.
   - Define tasks, architecture, and risks.

3. **✅ Confirm (Approval)**
   - Present the plan using `/stride-present`.
   - Wait for explicit user approval ("Proceed").
   - *No implementation until approved.*

4. **🔨 Implement (Execution)**
   - Run `/stride-implement` to log progress.
   - Execute tasks from `plan.md`.
   - Update `implementation.md` with decisions/notes.

5. **🏁 Complete (Retrospective)**
   - Run `/stride-review` for final check.
   - Run `/stride-complete` to archive and reflect.

**Quick Commands:**
- `/stride-init` - Initialize project context
- `/stride-derive` - Discover sprint ideas (AI-powered brainstorming) 🆕
- `/stride-lite` - Quick fixes without sprint files (< 50 lines) 🆕
- `/stride-status` - Get project status with blockers & recommendations 🆕
- `/stride-plan` - Create a new sprint
- `/stride-present` - Show sprint plan
- `/stride-implement` - Log implementation details
- `/stride-feedback` - Adjust mid-sprint
- `/stride-review` - Submit for review
- `/stride-complete` - Finalize sprint

**💡 Tips:**
- Not sure what to work on next? Use `/stride-derive` to get AI-generated sprint proposals!
- Small fix (< 50 lines)? Use `/stride-lite` for faster execution without creating sprint files!
- Want a project update? Use `/stride-status` for progress, blockers, and recommendations!
- Building a feature? Use `/stride-plan` for full sprint workflow!

<!-- STRIDE:END -->

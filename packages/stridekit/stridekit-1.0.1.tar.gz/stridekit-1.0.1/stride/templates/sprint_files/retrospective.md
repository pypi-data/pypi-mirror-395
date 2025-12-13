# Retrospective: [Sprint Name]

## What Worked
[Identify the areas of the sprint that were successful.  
List specific Strides, decisions, processes, or tools that contributed positively.]

Examples:
- Stride 1 delivered the expected outcome ahead of time due to…
- Architectural decisions in design.md reduced complexity by…
- Collaboration, communication, or feedback loops that improved efficiency
- Testing or validation approaches that ensured stability

---

## What Didn't
[Identify the pain points, issues, bottlenecks, or failures.  
Reference specific Strides, tasks, or design decisions that underperformed.]

Examples:
- Unexpected blockers in Stride 2 due to dependency mismatch
- Incomplete assumptions in the proposal that caused rework
- Time overruns due to unexpected technical debt
- Gaps in design.md that caused ambiguity during implementation

---

## Lessons Learned
[Extract insights from successes and failures.  
These must be actionable and future-facing.]

Examples:
- “Ensure API schemas are validated before planning begins.”
- “Break down complex Strides into more atomic units.”
- “Clarify domain rules earlier in the planning phase.”
- “Improve upfront requirements validation.”

---

## Recommendations
[State improvements to be applied in future sprints, processes, and Stride usage.  
These recommendations may influence project.md, future sprint planning, or team workflows.]

Examples:
- Adopt a more rigorous review step during `/stride-present`.
- Mandate a design.md file for any sprint involving external APIs.
- Introduce automated testing earlier in implementation.
- Refactor legacy modules to reduce future sprint overhead.

---

## Project Context Updates
[Document changes to `.stride/project.md` based on sprint learnings.  
Only complete this section if the sprint revealed new information that affects project-wide understanding.]

### Changes to project.md
- **Section [Number & Name]**: [What was updated and why]

Examples:
- **Section 7 (Domain Knowledge)**: Added new entity relationship between User and Session discovered during authentication implementation.
- **Section 8.1 (Technical Constraints)**: Updated library restriction—removed XYZ package due to security vulnerability found in sprint.
- **Section 11 (Risks & Assumptions)**: Validated assumption about API rate limits; updated with actual measured values.


---
description: Initialize or validate the Stride project context.
---

$ARGUMENTS
<!-- STRIDE:START -->

**Argument Resolution**

If project context is missing or incomplete:

1. **Auto-Detection First**:
   - Scan repository for existing documentation (README.md, package.json, pyproject.toml, etc.)
   - Analyze directory structure for tech stack clues
   - Detect dependencies and frameworks from config files
   - Infer domain from code patterns and naming
   - Extract project purpose from existing docs

2. **Targeted Questions Only** (for missing critical info):
   - Ask ONLY specific, narrow questions about undetectable information
   - Never ask: "Tell me about your project" (too broad)
   - Good examples:
     - "What is the primary business purpose? (e.g., e-commerce platform, data analytics tool)"
     - "What's the target deployment environment? (cloud/on-premise/hybrid)"
     - "Any specific compliance requirements? (GDPR, HIPAA, SOC2)"
   
3. **Question Priority** (ask in order, skip if detectable):
   - **High Priority**: Project purpose, primary tech stack (if not detected)
   - **Medium Priority**: Target users, deployment constraints
   - **Low Priority**: Nice-to-haves that can be updated later
   
4. **Never Prompt For**:
   - Information clearly present in README or docs
   - Tech stack visible in dependencies
   - Architecture patterns evident in code structure
   - Standard conventions for detected frameworks

5. **Accept Minimal Input**:
   - If user provides brief answers, infer reasonable defaults
   - Don't repeatedly ask for more detail
   - Generate sensible project.md with available information
   - Note what can be refined later

6. **Proceed** to create `.stride/project.md` with gathered + detected information

---

**Guardrails**
- Follow `.stride/project.md` template exactly—no added/removed sections.
- Do not generate sprint files during init.
- Ask only targeted questions when the repo lacks enough context.
- Never overwrite an existing valid `.stride/project.md` without explicit confirmation.
- Keep initialization strictly focused on establishing project-level understanding (not sprint planning).

**Steps**
1. Check for `.stride/project.md`.  
   - If present, validate structure (all 11 sections).  
   - If valid, stop and inform the user that initialization is already complete.

2. If `.stride/project.md` is missing or incomplete:  
   - Create `.stride/` directory if it does not exist.  
   - Load the project template from `.stride/templates/project.md` or reconstruct the required 11-section template from Stride Instructions.

3. Populate each section using:  
   - Repository analysis (directory structure, code patterns, tech stack)  
   - Existing documentation (README, architecture docs, configs)  
   - Dependency inspection (package.json, pyproject, go.mod, etc.)  
   - Domain inference (only when low-risk and safe)  

4. For any missing details that cannot be inferred:  
   - Ask the user targeted clarifying questions.  
   - Never ask broad or open-ended questions.  
   - Insert no placeholders or partial sections.

5. Generate `.stride/project.md`:  
   - Write all 11 sections with complete, meaningful content.  
   - Preserve headings exactly as defined in the template.  
   - Ensure no section is left empty or templated.

6. Validate internally:  
   - All sections populated  
   - No TODO markers  
   - Markdown is structurally correct  
   - Content aligns with repository reality  
   - Technical stack matches detected environment

7. Announce successful initialization:  
   - Summarize extracted project context  
   - Confirm `.stride/project.md` is now authoritative  
   - Suggest next steps:
     - Use `/stride-derive` to discover sprint ideas (recommended for new projects or when prioritizing work)
     - Use `/stride-plan <sprint-name>` if you already know what sprint to create

**Reference**
- `.stride/templates/project.md` — authoritative template for initialization.
- `.stride/project.md` — global project contract required before any sprint.
- Stride Instructions — for lifecycle rules, section semantics, and validation logic.
- Repository scanning tools (`ls`, project configs, dependency files) for context extraction.

<!-- STRIDE:END -->

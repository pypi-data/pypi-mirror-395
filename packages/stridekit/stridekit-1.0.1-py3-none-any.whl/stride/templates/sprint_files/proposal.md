# Proposal: [Sprint Name or Feature Name]

## Why
[Explain the underlying motivation in depth.  
Describe the user problem, technical gap, business opportunity, or system constraint that triggers this sprint.]

Examples:
- Current workflow causes friction for end-users because…
- Architecture lacks modularity, creating maintenance overhead…
- New business requirements demand support for…
- Performance bottlenecks degrade user experience beyond acceptable thresholds…
- Security or compliance requirements mandate improvements because…

State the **negative impact** of not solving this issue and the **positive impact** expected from the sprint.

## What
[Describe the exact scope of the sprint in a detailed but high-level format.  
Explain what the sprint WILL deliver and what it WILL NOT deliver.  
Define the functional outcomes, expected behaviors, and boundaries.]

### In Scope
- [Feature or capability that will be developed]
- [APIs/endpoints/modules that will be added or extended]
- [UI/UX flow changes]
- [Refactors that modify system behavior]
- [Dependencies or integrations to be introduced]

### Out of Scope
- [Anything explicitly not included]
- [Deferred capabilities]
- [Future improvements that will require another sprint]

## Acceptance Criteria
Each acceptance criterion MUST be:
- Measurable  
- Testable  
- Unambiguous  
- Mapped to a Stride later in the sprint

Examples:

### Functional Criteria
- [ ] When the user performs X, the system MUST respond by Y within Z ms  
- [ ] Feature MUST persist its state across application restarts  
- [ ] API MUST return proper error codes for invalid requests  
- [ ] Behavior MUST match rules defined in `.stride/project.md`

### Reliability Criteria
- [ ] System MUST handle at least N concurrent operations successfully  
- [ ] Error handling MUST follow project-defined fallback strategy

### Security Criteria
- [ ] Only authorized roles can invoke new functionality  
- [ ] Sensitive data MUST never appear in logs

### UX Criteria (If applicable)
- [ ] Flow MUST complete within N steps  
- [ ] Error states MUST be clearly communicated

## Success Definition
A sprint is considered **successful** when:
- All acceptance criteria are satisfied  
- All Strides in `plan.md` are complete  
- Code passes all automated tests  
- Documentation is up-to-date  
- No violations of `.stride/project.md` patterns, architecture, or security rules  
- Validation via `stride validate <sprint>` passes without warnings

## Impact
[List the impact areas this sprint will touch.]

Examples:
- Affected modules:  
  - `/src/modules/auth/`  
  - `/api/user/`  
  - `/infra/logging/`

- Affected teams:
  - Frontend  
  - Backend  
  - DevOps  
  - QA  

- Affected systems:
  - CI/CD pipeline  
  - Analytics stack  
  - External APIs  

Define whether the sprint introduces:
- Breaking changes  
- Backward-compatible enhancements  
- Migration requirements  

If **breaking changes** exist, explicitly state:

> **BREAKING:** This sprint alters existing behavior in…

## Dependencies
[List dependencies that could affect delivery.]

Types:
- Technical (libraries, frameworks, APIs, infrastructure)
- Organizational (waiting for another team’s output)
- Architectural (pending design decisions)
- Open questions that must be answered before implementation

## Risks & Assumptions
### Risks
[List risks that may affect execution.]

Examples:
- Legacy components may block integration  
- Performance thresholds might not be achievable  
- Upstream API limits may be restrictive  

### Assumptions
[List assumptions that the sprint relies on.]

Examples:
- User roles and permissions model is stable  
- Versioning scheme remains unchanged  
- Required infrastructure is available  

## Milestone Alignment
[Link this sprint to a longer-term roadmap item or product milestone, if applicable.]

Example:
- This sprint completes Phase 1 of the Authentication Revamp
- This sprint finalizes the data model required for upcoming analytics module

# ADR-016: Dashboard Implementation Timeline (S7-S9 vs S13)

**Status**: Accepted  
**Decision Date**: 2026-04-22  
**Context**: Clarify conflicting dashboard timeline (MVP section says S15 end date, but implementation starts S12)  
**Owner**: Product + Architecture

---

## Problem Statement

Dashboard implementation timeline is ambiguous in project planning:

- **PLAN-REALISATION.md** says: Dashboard MVP implemented in **S12** (Phase 3)
- **BACKLOG.md** says: Dashboard MVP is part of MVP scope ending **S15**
- **BLOCKERS.md** initially listed this as priority inconsistency

**Question**: When should dashboard development start? S7-S9 or S12?

---

## Solution

### Dashboard Timeline (FINAL DECISION)

```
Phase 0 (S1-S3):   Discovery + Architecture ← Dashboard sketched but not built
Phase 1 (S4-S6):   Read implementation ← Dashboard NOT required yet
Phase 2 (S7-S11):  Plan + Approve implementation ← Dashboard design finalized
Phase 3 (S10-S12): Execute + Dashboard MVP ← Dashboard BUILD starts in S12
                                             ← Dashboard COMPLETE by S12 (end of Phase 3)

MVP Validation (S13-S15): Testing + measurement ← Dashboard already live, used for testing

V1 (S16-S20): Post-MVP improvements ← Dashboard enhanced with metrics, custom fields
```

### Rationale

1. **Dashboard is NOT blocking MVP**
   - MVP can complete diagnostic/approval cycle without visual dashboard
   - Teams cards provide approval interface

2. **Dashboard improves MVP validation**
   - Implementing dashboard in S12 allows S13-S15 to test with working UI
   - Better incident context visible in dashboard accelerates diagnostics

3. **"MVP" refers to scope, not timeline**
   - MVP scope includes dashboard (must-have feature)
   - MVP scope deadline is S15
   - Dashboard implementation can be S12 because it's not dependency-blocking

4. **Parallel execution possible**
   - Execute phase (E0-E4) can run without dashboard
   - Dashboard built in parallel (S12) after Approve phase matures (S10-S11)

---

## Detailed Timeline

### Phase 3: Execute + Dashboard (S10-S12)

```
Week 10-11 (Phase 3a): 
  - [ ] Finalize Execute phase (E0, E1, E2, E3)
  - [ ] Dashboard design locked (UX review with team)
  - [ ] Data schema finalized (schema.sql, schema_dai.sql)

Week 12 (Phase 3b):
  - [ ] Dashboard MVP build
    - [ ] FastAPI setup + authentication
    - [ ] HTMX incident list page
    - [ ] Incident detail view with diagnostic context
    - [ ] Approval status display
    - [ ] Audit log viewer
  - [ ] Integration with SQLite (read incidents_ado, releases_dai)
  - [ ] Testing: smoke tests on dashboard pages
  - [ ] Documentation: dashboard user guide
```

### Phase 4: MVP Validation (S13-S15)

```
Week 13-14:
  - Dashboard populated with real incident data
  - Team uses dashboard to review diagnostics
  - User feedback collected

Week 15:
  - Dashboard bug fixes
  - Performance optimization
  - MVP validation complete
```

---

## Implementation Checklist (S12)

### Code

- [ ] FastAPI app.py with 5+ endpoints
- [ ] HTML templates (Jinja2) for list/detail pages
- [ ] HTMX endpoints for dynamic updates
- [ ] SQLite queries for incidents, releases, audit_log
- [ ] Authentication middleware (Azure AD)

### Data Integration

- [ ] List incidents_ado with pagination
- [ ] Display related releases_dai for context
- [ ] Show approval status (pending/approved/rejected)
- [ ] Display audit trail

### Features

- [ ] **Incident list**: Sortable by date, pipeline, status
- [ ] **Incident detail**: Full context (logs, custom fields, diagnostics)
- [ ] **Diagnostic display**: Root cause, recommended action, risk level
- [ ] **Approval history**: Who approved, when, outcome
- [ ] **Audit log**: All actions with timestamp + actor

### Testing

- [ ] Unit tests for FastAPI endpoints (using TestClient)
- [ ] Integration tests with SQLite mock data
- [ ] HTMX interaction tests
- [ ] Authentication tests (Azure AD token validation)
- [ ] Performance tests (list page < 2 sec with 100 incidents)

### Documentation

- [ ] Dashboard user guide (how to view incidents, approve actions)
- [ ] Developer guide (how to add new pages)
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Database schema documentation

---

## Why NOT Earlier? (Why not S7-S9)

**Dashboard is NOT required until Approve phase matures**:

- S4-S9: Focused on Read, Plan, Approve logic
- Dashboard would sit idle without functional diagnostic data
- Prioritizing core RPAE cycle first, UI second

**Resources**:

- S7-S9 should focus on Plan + Approve complexity
- Dashboard development can't run in parallel (single developer team)
- Better to deliver working logic + simple UI than complex UI + broken logic

---

## Why NOT Later? (Why not S13)

**Dashboard needed for MVP validation**:

- S13-S15 must test with live incident data
- Dashboard accelerates diagnostic review vs command-line tools
- Demonstrates "full cycle" to stakeholders
- Better user experience for MTTR measurement

---

## Scope Changes (S12 Release)

### Included in S12 Dashboard

✅ Incident list (searchable, sortable)  
✅ Incident detail with diagnostic context  
✅ Approval status display  
✅ Audit log viewer  
✅ Authentication  
✅ Read-only mode (no manual edits)

### NOT Included (S13+)

❌ Metrics/MTTR graphs (S16 in V1)  
❌ Custom fields display (pending ADO-CUSTOM-FIELDS-ISAGRI.md)  
❌ Cross-pipeline dependencies visualization (ADR-015: not MVP)  
❌ Export functionality (S20)  
❌ Webhook status / health checks (S20)

---

## Dependencies

| Dependency | Status | Owner | ETA |
|-----------|--------|-------|-----|
| Schema.sql finalized | ✅ Done | Architecture | S6 |
| Schema_dai.sql finalized | ✅ Done | Architecture | S6 |
| Approve phase complete | 🟡 In progress | DevOps | S11 |
| Azure AD setup | 🟡 In progress | Security | S3 |
| MCP integration | ✅ Done | OpenCode | S3 |

**Critical path**: Approve phase must be stable by S12 for dashboard integration.

---

## Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| Dashboard delay blocks MVP | Low | Dashboard is enhancement, not blocker |
| Dashboard too complex | Medium | Limit features to MVP scope (list, detail, logs) |
| Database schema incomplete | Low | Schema reviewed in S6 |
| Authentication integration fails | Medium | Test Azure AD in S3, early integration |

---

## Success Criteria

- [ ] Dashboard deployed to staging by EOW S12
- [ ] All dashboard features working in S13
- [ ] Team can view incidents from dashboard
- [ ] Performance: list loads in < 2 sec, detail in < 1 sec
- [ ] No breaking changes to API between S12-S15
- [ ] User feedback incorporated into V1 (S16)

---

## References

- [PLAN-REALISATION.md — Phase 3 timeline](../artifacts/07-PLAN-REALISATION.md)
- [BACKLOG.md — MVP scope](../artifacts/09-BACKLOG.md)
- [ADR-010: FastAPI + HTMX decision](ADR-010-fastapi-htmx.md)
- [ADR-005: Dashboard MVP mandatory](ADR-005-dashboard-mvp.md)
- [TECH-STACK.md — Dashboard tech choices](../artifacts/TECH-STACK.md)

---

## Decision Log

**2026-04-22**: ADR-016 created  
- Resolved conflicting timeline interpretations
- Confirmed S12 as dashboard build week
- Confirmed S13-S15 for validation with live dashboard
- Scope bounded to MVP features only

---

**Approved by**: Product Lead + Architecture Lead  
**Next review**: EOW S12 (progress check)

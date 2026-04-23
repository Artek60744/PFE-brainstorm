# Approval Levels & Risk Classification

**Document Version**: 1.0  
**Last Updated**: 2026-04-22  
**Status**: Operational Guide  
**Owner**: DevOps + Product team

---

## Overview

This document defines the **three-tier approval framework** for OpenClaw actions, based on risk level and business impact.

### Resolution of BLOCKER Q7

**Q7**: What are "Niveau 1 auto-approuvé", "Niveau 2", "Niveau 3" criteria?  
**Answer**: See Tiers 1-3 below with specific risk classifiers

---

## Part 1: Risk Classification Framework

### Risk Factors

Every proposed action is scored on:

| Factor | Weight | Low Risk | Medium Risk | High Risk |
|--------|--------|----------|-------------|-----------|
| **Scope** | 40% | Single service | Multiple services | Critical infrastructure |
| **Impact** | 30% | Non-production | Staging | Production |
| **Reversibility** | 20% | Easily reversed | Manual rollback needed | Data loss possible |
| **Blast Radius** | 10% | <10 users | 10-100 users | >100 users |

### Risk Score Calculation

```
Risk Score = (Scope × 0.4) + (Impact × 0.3) + (Reversibility × 0.2) + (BlastRadius × 0.1)

Where each factor is 0-100:
  0-33 = Low Risk
  34-66 = Medium Risk
  67-100 = High Risk
```

---

## Part 2: Approval Tier 1 (Auto-Approved)

### Criteria

**Condition**: Risk Score < 34  
**Approval**: NONE REQUIRED (automatic)  
**Examples**:

- ✅ Restart single staging service (non-prod)
- ✅ Re-run failed test job (logs only, no data change)
- ✅ Restart build agent (no production impact)
- ✅ Clear local cache (easily recoverable)

### Implementation

```python
def classify_action_tier(action: dict) -> int:
    """Classify action into tier 1/2/3 based on risk."""
    
    risk_score = calculate_risk_score(action)
    
    if risk_score < 34:
        return 1  # Auto-approve, no human needed
    elif risk_score < 67:
        return 2  # Manual approval needed
    else:
        return 3  # Double-approval required

def calculate_risk_score(action: dict) -> int:
    """Calculate numeric risk score."""
    
    # Scope: 0-100
    if "prod" in action.get("environment", "").lower():
        scope_score = 100
    elif "staging" in action.get("environment", "").lower():
        scope_score = 50
    else:
        scope_score = 10
    
    # Impact: 0-100
    if action.get("type") == "deployment":
        impact_score = 80
    elif action.get("type") == "restart":
        impact_score = 30
    else:
        impact_score = 10
    
    # Reversibility: 0-100 (inverse: easy = low, hard = high)
    if action.get("has_rollback"):
        reversibility_score = 10
    else:
        reversibility_score = 70
    
    # Blast radius: 0-100
    affected_users = action.get("affected_users", 0)
    if affected_users > 100:
        blast_score = 100
    elif affected_users > 10:
        blast_score = 50
    else:
        blast_score = 10
    
    risk = (
        (scope_score * 0.4) +
        (impact_score * 0.3) +
        (reversibility_score * 0.2) +
        (blast_score * 0.1)
    )
    
    return int(risk)
```

### Audit Trail (Tier 1)

Even though Tier 1 is auto-approved, **log the action**:

```sql
INSERT INTO audit_log (action, tier, risk_score, approver, timestamp)
VALUES ('restart_service', 1, 25, 'SYSTEM_AUTO', NOW());
```

---

## Part 3: Approval Tier 2 (Manual Single Approval)

### Criteria

**Condition**: 34 ≤ Risk Score < 67  
**Approval**: ONE DevOps engineer  
**Timeout**: 30 minutes (escalate if no response)  
**Examples**:

- ✅ Restart production database (with rollback plan)
- ✅ Update configuration (reversible)
- ✅ Scale up staging environment
- ✅ Rotate non-critical credentials

### Approval Workflow

```
1. Diagnosis generated (Risk Score = 45)
2. OpenClaw classifies as TIER 2
3. Send Teams card to #openclaw-diagnostics
4. On-call engineer clicks "Approve"
5. Execute action (logged with approver name)
6. If no approval in 30 min → escalate to team lead
```

### Implementation

```python
async def send_approval_request_tier2(diagnosis: dict, approver_email: str):
    """Send Tier 2 approval request to single engineer."""
    
    risk_score = diagnosis['risk_score']
    
    if not (34 <= risk_score < 67):
        raise ValueError("Action not Tier 2")
    
    # Send Teams card
    await send_diagnostic_to_teams({
        **diagnosis,
        "tier": 2,
        "approvers_needed": 1,
        "timeout_minutes": 30
    })
    
    # Set expiration
    diagnosis['expires_at'] = datetime.now() + timedelta(minutes=30)
    
    # Log approval request
    audit.log("APPROVAL_REQUESTED_TIER2", {
        "diagnosis_id": diagnosis['id'],
        "risk_score": risk_score,
        "approver": approver_email,
        "expires_at": diagnosis['expires_at']
    })

@app.post("/approve_tier2")
async def approve_tier2(
    diagnosis_id: str,
    approver = Depends(require_permission("approve_l2"))
):
    """Approve Tier 2 action."""
    
    diagnosis = get_diagnosis(diagnosis_id)
    
    if diagnosis['tier'] != 2:
        raise HTTPException(status_code=400, detail="Not a Tier 2 action")
    
    if datetime.now() > diagnosis['expires_at']:
        raise HTTPException(status_code=410, detail="Approval window expired")
    
    # Execute action
    result = await execute_action(diagnosis)
    
    # Log approval
    audit.log("APPROVAL_GRANTED_TIER2", {
        "diagnosis_id": diagnosis_id,
        "approver": approver["email"],
        "result": result,
        "timestamp": datetime.now()
    })
    
    return {"status": "approved_and_executed", "result": result}
```

### Escalation on Timeout

```python
async def check_approval_timeouts():
    """Scheduled task: escalate Tier 2 approvals after 30 min."""
    
    pending_approvals = get_pending_approvals(tier=2, older_than_minutes=30)
    
    for approval in pending_approvals:
        # Notify team lead
        await notify_team_lead(
            f"Tier 2 approval pending for {approval['diagnosis_id']} "
            f"since {approval['created_at']}"
        )
        
        audit.log("APPROVAL_ESCALATED_TIER2", {
            "diagnosis_id": approval['diagnosis_id'],
            "reason": "timeout_30min",
            "escalated_to": "team_lead"
        })
```

---

## Part 4: Approval Tier 3 (Double Approval)

### Criteria

**Condition**: Risk Score ≥ 67  
**Approval**: TWO approvers (one DevOps lead required)  
**Timeout**: 15 minutes per approver  
**Examples**:

- 🚨 Production database failover
- 🚨 Rolling restart of all web servers
- 🚨 Credential rotation (all systems)
- 🚨 Data migration or backup restore

### Approval Workflow

```
1. Diagnosis generated (Risk Score = 75)
2. OpenClaw classifies as TIER 3
3. Send Teams card requesting 2 approvals
4. First approver clicks "Approve"
5. System waits for second approver (can be same person for L1)
6. Both approvers logged
7. Execute action with full audit trail
```

### Implementation

```python
async def send_approval_request_tier3(
    diagnosis: dict,
    approver1: str,
    approver2: str
):
    """Send Tier 3 approval request requiring TWO approvals."""
    
    risk_score = diagnosis['risk_score']
    
    if risk_score < 67:
        raise ValueError("Action not Tier 3")
    
    # Send Teams card with 2 approvers listed
    await send_diagnostic_to_teams({
        **diagnosis,
        "tier": 3,
        "approvers_needed": 2,
        "timeout_minutes_per_approver": 15,
        "approver1": approver1,
        "approver2": approver2
    })
    
    # Store approval state
    diagnosis['approvals'] = {
        "approver1": None,
        "approver2": None
    }
    diagnosis['expires_at'] = datetime.now() + timedelta(minutes=30)  # Total 30 min
    
    audit.log("APPROVAL_REQUESTED_TIER3", {
        "diagnosis_id": diagnosis['id'],
        "risk_score": risk_score,
        "approvers": [approver1, approver2],
        "expires_at": diagnosis['expires_at']
    })

@app.post("/approve_tier3")
async def approve_tier3(
    diagnosis_id: str,
    approver = Depends(require_permission("approve_l3"))
):
    """Approve Tier 3 action (one of two required)."""
    
    diagnosis = get_diagnosis(diagnosis_id)
    
    if diagnosis['tier'] != 3:
        raise HTTPException(status_code=400, detail="Not a Tier 3 action")
    
    if datetime.now() > diagnosis['expires_at']:
        raise HTTPException(status_code=410, detail="Approval window expired")
    
    # Record this approver
    if diagnosis['approvals']['approver1'] is None:
        diagnosis['approvals']['approver1'] = approver['email']
        missing = "approver2"
    elif diagnosis['approvals']['approver2'] is None:
        diagnosis['approvals']['approver2'] = approver['email']
        missing = None
    else:
        raise HTTPException(status_code=400, detail="Both approvers already recorded")
    
    audit.log("APPROVAL_PARTIAL_TIER3", {
        "diagnosis_id": diagnosis_id,
        "approver": approver['email'],
        "approvals_received": 2 if missing is None else 1
    })
    
    if missing is None:
        # Both approvals received, execute
        result = await execute_action(diagnosis)
        
        audit.log("APPROVAL_COMPLETE_TIER3", {
            "diagnosis_id": diagnosis_id,
            "approver1": diagnosis['approvals']['approver1'],
            "approver2": diagnosis['approvals']['approver2'],
            "result": result,
            "timestamp": datetime.now()
        })
        
        return {"status": "approved_by_two_and_executed", "result": result}
    else:
        return {
            "status": "awaiting_second_approval",
            "first_approver": diagnosis['approvals']['approver1'],
            "needed": missing
        }
```

---

## Part 5: Dashboard Risk Display

### Teams Card Risk Indicator

```json
{
  "type": "Container",
  "body": [
    {
      "type": "ColumnSet",
      "columns": [
        {
          "width": "stretch",
          "items": [
            {
              "type": "TextBlock",
              "text": "Risk Level",
              "weight": "bolder"
            },
            {
              "type": "TextBlock",
              "text": "${riskLevel}",  // "Tier 1 (Auto)", "Tier 2", "Tier 3 (High)"
              "color": "${riskColor}",  // "good", "warning", "attention"
              "size": "large"
            }
          ]
        },
        {
          "width": "auto",
          "items": [
            {
              "type": "TextBlock",
              "text": "Score: ${riskScore}/100",
              "size": "small"
            }
          ]
        }
      ]
    }
  ]
}
```

### Dashboard Table

```html
<table>
  <tr>
    <th>Diagnosis ID</th>
    <th>Risk Score</th>
    <th>Tier</th>
    <th>Approvers</th>
    <th>Status</th>
  </tr>
  <tr>
    <td>DIAG-2026-001</td>
    <td>25 (Low)</td>
    <td>1 (Auto)</td>
    <td>SYSTEM</td>
    <td>Executed ✅</td>
  </tr>
  <tr>
    <td>DIAG-2026-002</td>
    <td>45 (Medium)</td>
    <td>2 (Manual)</td>
    <td>john.doe@isagri</td>
    <td>Pending ⏳</td>
  </tr>
  <tr>
    <td>DIAG-2026-003</td>
    <td>80 (High)</td>
    <td>3 (Double)</td>
    <td>jane.smith, alice.wilson</td>
    <td>Approved 1/2 ⏳</td>
  </tr>
</table>
```

---

## Part 6: Testing Approval Tiers

### Unit Tests

```python
import pytest

def test_tier1_auto_approved():
    """Tier 1 action should auto-execute without approval."""
    action = {"type": "restart", "environment": "dev", "has_rollback": True}
    assert classify_action_tier(action) == 1
    # Should execute immediately without Teams notification

def test_tier2_requires_approval():
    """Tier 2 action should wait for one approval."""
    action = {"type": "restart", "environment": "staging", "has_rollback": True}
    assert classify_action_tier(action) == 2
    # Should send Teams card, wait for response

def test_tier3_requires_double_approval():
    """Tier 3 action should wait for two approvals."""
    action = {"type": "failover", "environment": "prod", "has_rollback": False}
    assert classify_action_tier(action) == 3
    # Should send Teams card, wait for 2 responses

def test_approval_timeout_tier2():
    """Tier 2 approval should timeout after 30 min."""
    diagnosis = {"tier": 2, "created_at": datetime.now() - timedelta(minutes=31)}
    with pytest.raises(HTTPException) as exc:
        approve_tier2("diag-123")
    assert exc.value.status_code == 410
```

---

## Part 7: Compliance & Audit

### Required Audit Fields

For all approvals (Tier 2 & 3):

```sql
INSERT INTO audit_log 
  (action, diagnosis_id, approver_email, approver_team, tier, risk_score, decision, timestamp)
VALUES 
  ('approval_granted', 'DIAG-001', 'john@isagri', 'DevOps', 2, 45, 'APPROVED', NOW());
```

### Compliance Report

```python
def generate_approval_compliance_report(date_range):
    """Generate monthly compliance report."""
    
    approvals = audit.query(
        "approval_granted",
        date_range=date_range
    )
    
    return {
        "total_approvals": len(approvals),
        "tier1_auto": sum(1 for a in approvals if a['tier'] == 1),
        "tier2_approved": sum(1 for a in approvals if a['tier'] == 2 and a['decision'] == 'APPROVED'),
        "tier2_rejected": sum(1 for a in approvals if a['tier'] == 2 and a['decision'] == 'REJECTED'),
        "tier3_approved": sum(1 for a in approvals if a['tier'] == 3 and a['decision'] == 'APPROVED'),
        "avg_approval_time": average_approval_time(approvals),
        "compliance": "100%" if all_approvals_logged(approvals) else "FAILED"
    }
```

---

## Operational Checklist

- [ ] Risk classification framework understood by team
- [ ] Tier 1 actions tested (auto-execution)
- [ ] Tier 2 approval flow tested (single approver, 30 min timeout)
- [ ] Tier 3 approval flow tested (double approver, escalation)
- [ ] Risk scoring algorithm implemented
- [ ] Teams cards display risk level correctly
- [ ] Audit logging capturing all approvals
- [ ] Compliance reports generated monthly
- [ ] Team trained on risk classification
- [ ] Tier decisions documented in playbook

---

## References

- [ADR-012: Trust Boundary](../decisions/ADR-012-trust-boundary.md)
- [BLOCKERS.md — Q7 Resolution](../BLOCKERS.md)
- [09-BACKLOG.md — Approval Epic A5](../artifacts/09-BACKLOG.md)

---

**Status**: Ready for implementation  
**Blocker Resolved**: Q7 ✅  
**Owner**: Product + DevOps  
**Timeline**: S4-S6 (Approve phase)

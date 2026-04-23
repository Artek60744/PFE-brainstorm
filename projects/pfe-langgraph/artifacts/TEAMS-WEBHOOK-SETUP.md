# Teams Webhook Setup Guide

**Document Version**: 1.0  
**Last Updated**: 2026-04-22  
**Status**: Implementation Guide  
**Owner**: DevOps + OpenClaw Bot Owner

---

## Overview

This document provides **step-by-step instructions** to configure Microsoft Teams webhooks for OpenClaw incident notifications and approvals.

### Resolution of BLOCKER Q6

**Q6**: How to set up Teams webhook for approval workflow?  
**Answer**: See Part 2 below (webhook creation + card setup)

---

## Part 1: Teams Channel Setup

### Create Dedicated Channel

**Channel Name**: `OPENCLAW-DIAGNOSTICS`  
**Privacy**: Private (DevOps team only)  
**Description**: "Real-time OpenClaw incident diagnostics and approvals"

**Steps**:

1. Open Microsoft Teams
2. Click `+ Create` → `Create a team`
3. Choose `From scratch` → `Private`
4. Name: `OPENCLAW-DIAGNOSTICS`
5. Add members: DevOps team (+ OpenClaw bot if applicable)

### Channel Settings

```
Channel name: OPENCLAW-DIAGNOSTICS
Privacy: Private
Members: 
  - DevOps team leads
  - On-call engineers
  - OpenClaw monitoring account (if applicable)

Message retention: 90 days (Teams default)
Notifications: Enable for all team members
```

---

## Part 2: Incoming Webhook Configuration

### Step 1: Add Webhook Connector

1. Open channel `OPENCLAW-DIAGNOSTICS`
2. Click `⋯` (More options) → `Connectors`
3. Search for `Incoming Webhook`
4. Click `Configure`

### Step 2: Create Webhook URL

1. **Name**: `OpenClaw Diagnostics`
2. **Image**: (Optional) Upload OpenClaw logo if available
3. Click `Create`
4. **Copy the Webhook URL** — this is the `TEAMS_WEBHOOK_URL` for OpenClaw

```
Example webhook URL (NEVER commit to git):
https://outlook.webhook.office.com/webhookb2/xxxxx@xxxxx/IncomingWebhook/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3: Store Webhook Securely

**CRITICAL**: Never commit webhook URL to Git

**Option A: AWS Secrets Manager (Recommended for production)**

```bash
# Store webhook URL in AWS Secrets Manager
aws secretsmanager create-secret \
  --name openclaw/teams-webhook-diagnostics \
  --secret-string "https://outlook.webhook.office.com/webhookb2/..."
```

**Option B: Environment Variable (.env.production)**

```bash
# .env.production (not in git, managed by ops)
TEAMS_WEBHOOK_URL="https://outlook.webhook.office.com/webhookb2/..."
```

**Option C: OpenCode MCP Server Configuration**

If using OpenCode MCP integration for Teams:

```yaml
# openclaw/config/teams-config.yaml
teams:
  webhook_url: "${TEAMS_WEBHOOK_URL}"  # Injected at runtime
  channel: "OPENCLAW-DIAGNOSTICS"
  message_templates:
    - diagnostics_card
    - approval_card
```

---

## Part 3: Message Templates

### Template 1: Diagnostic Card

**File**: `artifacts/dashboard/templates/teams_diagnostic_card.json`

```json
{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "Container",
      "style": "emphasis",
      "body": [
        {
          "type": "TextBlock",
          "text": "🔴 Pipeline Failure — Diagnostic Ready",
          "size": "large",
          "weight": "bolder"
        }
      ]
    },
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
                  "text": "Pipeline",
                  "weight": "bolder",
                  "size": "small"
                },
                {
                  "type": "TextBlock",
                  "text": "${pipelineName}",
                  "size": "medium"
                }
              ]
            },
            {
              "width": "auto",
              "items": [
                {
                  "type": "TextBlock",
                  "text": "Build #",
                  "weight": "bolder",
                  "size": "small"
                },
                {
                  "type": "TextBlock",
                  "text": "${buildNumber}",
                  "size": "medium"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "Container",
      "separator": true,
      "body": [
        {
          "type": "TextBlock",
          "text": "🔍 Root Cause Analysis",
          "weight": "bolder"
        },
        {
          "type": "TextBlock",
          "text": "${rootCause}",
          "wrap": true
        }
      ]
    },
    {
      "type": "Container",
      "body": [
        {
          "type": "TextBlock",
          "text": "✅ Recommended Action",
          "weight": "bolder"
        },
        {
          "type": "TextBlock",
          "text": "${recommendedAction}",
          "wrap": true
        }
      ]
    },
    {
      "type": "Container",
      "body": [
        {
          "type": "TextBlock",
          "text": "Approval Required",
          "weight": "bolder",
          "color": "warning"
        },
        {
          "type": "TextBlock",
          "text": "This action expires in 30 minutes if not approved",
          "size": "small"
        }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "✅ Approve & Execute",
      "url": "https://openclaw.isagri.internal/approve?diagId=${diagnosisId}&token=${approvalToken}",
      "style": "positive"
    },
    {
      "type": "Action.OpenUrl",
      "title": "❌ Reject",
      "url": "https://openclaw.isagri.internal/reject?diagId=${diagnosisId}&token=${approvalToken}",
      "style": "destructive"
    },
    {
      "type": "Action.OpenUrl",
      "title": "📋 View Full Details",
      "url": "https://dev.azure.com/isagri/_build/results?buildId=${buildNumber}"
    }
  ]
}
```

### Template 2: Approval Response Card

Sent when user clicks "Approve" or "Reject":

```json
{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "Approval Recorded",
      "size": "large",
      "weight": "bolder",
      "color": "good"
    },
    {
      "type": "TextBlock",
      "text": "Decision: ${decision}",
      "wrap": true
    },
    {
      "type": "TextBlock",
      "text": "Approved by: ${approverName}",
      "size": "small"
    },
    {
      "type": "TextBlock",
      "text": "Timestamp: ${approvalTime}",
      "size": "small"
    }
  ]
}
```

---

## Part 4: Python Integration (FastAPI)

### Send Diagnostic Message

```python
import json
import requests
from datetime import datetime, timedelta

async def send_diagnostic_to_teams(diagnosis: dict) -> bool:
    """
    Send diagnostic card to Teams channel via webhook.
    
    Args:
        diagnosis: Diagnostic result with rootCause, recommendedAction, etc.
        
    Returns:
        True if message sent successfully
    """
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    
    if not webhook_url:
        logger.error("TEAMS_WEBHOOK_URL not configured")
        return False
    
    # Prepare card data
    card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
            {
                "type": "TextBlock",
                "text": "🔴 Pipeline Failure — Diagnostic Ready",
                "size": "large",
                "weight": "bolder"
            },
            {
                "type": "TextBlock",
                "text": f"Pipeline: {diagnosis['pipeline_name']}",
                "wrap": true
            },
            {
                "type": "TextBlock",
                "text": f"Build #{diagnosis['build_id']}",
                "wrap": true
            },
            {
                "type": "TextBlock",
                "text": "🔍 Root Cause",
                "weight": "bolder"
            },
            {
                "type": "TextBlock",
                "text": diagnosis['root_cause'],
                "wrap": true
            },
            {
                "type": "TextBlock",
                "text": "✅ Recommended Action",
                "weight": "bolder"
            },
            {
                "type": "TextBlock",
                "text": diagnosis['recommended_action'],
                "wrap": true
            }
        ],
        "actions": [
            {
                "type": "Action.OpenUrl",
                "title": "✅ Approve & Execute",
                "url": f"https://openclaw.isagri.internal/approve?diagId={diagnosis['id']}"
            },
            {
                "type": "Action.OpenUrl",
                "title": "❌ Reject",
                "url": f"https://openclaw.isagri.internal/reject?diagId={diagnosis['id']}"
            }
        ]
    }
    
    # Send to Teams
    try:
        response = requests.post(
            webhook_url,
            json={"@type": "MessageCard", "body": [card]},
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"Diagnostic sent to Teams: {diagnosis['id']}")
            return True
        else:
            logger.error(f"Teams webhook failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Teams webhook error: {e}")
        return False
```

### Receive Approval Callback

```python
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

@app.get("/approve")
async def approve_action(diagId: str, token: str) -> dict:
    """
    Handle approval callback from Teams.
    
    Args:
        diagId: Diagnosis ID from Teams card
        token: Approval token (for validation)
        
    Returns:
        Approval confirmation
    """
    # Validate token
    if not validate_approval_token(token, diagId):
        raise HTTPException(status_code=401, detail="Invalid approval token")
    
    # Check expiration (30 min)
    diagnosis = get_diagnosis(diagId)
    if datetime.now() > diagnosis['expires_at']:
        raise HTTPException(status_code=410, detail="Approval expired")
    
    # Record approval in audit trail
    audit.log("APPROVAL_GRANTED", {
        "diagnosis_id": diagId,
        "approver": get_current_user(),
        "timestamp": datetime.now()
    })
    
    # Execute action
    action_result = await execute_approved_action(diagnosis)
    
    return {
        "status": "approved",
        "action_result": action_result,
        "timestamp": datetime.now()
    }

@app.get("/reject")
async def reject_action(diagId: str, token: str, reason: str = None) -> dict:
    """Handle rejection callback from Teams."""
    if not validate_approval_token(token, diagId):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    audit.log("APPROVAL_REJECTED", {
        "diagnosis_id": diagId,
        "rejector": get_current_user(),
        "reason": reason,
        "timestamp": datetime.now()
    })
    
    return {
        "status": "rejected",
        "timestamp": datetime.now()
    }
```

---

## Part 5: Testing the Webhook

### Manual Test

```bash
# Test webhook with simple message
curl -X POST "${TEAMS_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "OpenClaw Webhook Test - Connection Successful ✅",
    "themeColor": "0078D4"
  }'

# Expected response: 200 OK (body is "1")
```

### Automated Test

```python
import requests

def test_teams_webhook():
    """Verify Teams webhook is accessible."""
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    
    test_payload = {
        "text": "OpenClaw Test Message",
        "themeColor": "0078D4"
    }
    
    response = requests.post(webhook_url, json=test_payload, timeout=5)
    
    assert response.status_code == 200, f"Webhook returned {response.status_code}"
    assert response.text == "1", "Teams returned unexpected response"
    
    print("✅ Teams webhook test passed")
```

---

## Part 6: Monitoring & Troubleshooting

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Invalid webhook URL | 404 error | Regenerate webhook in Teams connector |
| Expired webhook | 401 error | Regenerate webhook |
| Malformed card JSON | Message fails to send | Validate JSON schema |
| Timeout (>10s) | No message received | Check network connectivity |
| Wrong channel | Message goes elsewhere | Verify webhook URL scoped to channel |

### Health Check Script

```python
async def check_teams_health():
    """Monitor Teams webhook health."""
    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    
    try:
        response = await asyncio.wait_for(
            requests.post(webhook_url, json={"text": "Health check"}),
            timeout=5
        )
        
        if response.status_code == 200:
            logger.info("✅ Teams webhook healthy")
            return True
        else:
            logger.warning(f"⚠️ Teams webhook returned {response.status_code}")
            return False
            
    except asyncio.TimeoutError:
        logger.error("❌ Teams webhook timeout")
        return False
    except Exception as e:
        logger.error(f"❌ Teams webhook error: {e}")
        return False
```

---

## Part 7: Security Best Practices

- ✅ Store webhook URL in AWS Secrets Manager (not in code)
- ✅ Rotate webhook URL every 90 days
- ✅ Restrict channel access to DevOps team only
- ✅ Log all approval decisions for audit trail
- ✅ Implement token validation (prevent approval spoofing)
- ✅ Set approval expiration (30 min max)
- ✅ Monitor webhook usage for anomalies

---

## Deployment Checklist

- [ ] Teams channel `OPENCLAW-DIAGNOSTICS` created
- [ ] Incoming webhook configured and URL copied
- [ ] Webhook URL stored in AWS Secrets Manager
- [ ] FastAPI endpoints `/approve` and `/reject` implemented
- [ ] Diagnostic card template tested
- [ ] Webhook health check passing
- [ ] Manual test message sent and received
- [ ] Audit logging configured
- [ ] Security review completed
- [ ] Documentation updated with webhook URL (in SECRET manager, not repo)

---

## References

- [Microsoft Teams Webhook Integration](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using)
- [Adaptive Cards Documentation](https://adaptivecards.io/)
- [OpenClaw MCP Teams Integration](https://opencode.ai/docs/mcp/teams)
- [BLOCKERS.md — Q6 Resolution](../BLOCKERS.md)

---

**Status**: Ready for implementation  
**Blocker Resolved**: Q6 ✅  
**Owner**: DevOps team  
**Timeline**: S1-S3 (MVP setup phase)

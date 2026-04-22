# MCP Configuration Guide

**Document Version**: 1.0  
**Last Updated**: 2026-04-22  
**Status**: MVP Configuration  
**Owner**: OpenClaw Project (DevOps + Security)

---

## Overview

This document specifies the **Model Context Protocol (MCP) server configuration** for the OpenClaw agent to safely interact with Azure DevOps, Digital.ai Release, and Teams within the PFE Isagri environment.

### Design Principles

1. **Read-First**: All integrations default to read-only (diagnostic mode)
2. **Explicit Write**: Any write operation requires explicit permission via MCP custom skill or approved MCP gateway
3. **Dry-Run**: All state-changing operations must be testable in dry-run mode before production
4. **Audit Trail**: Every MCP call logged with timestamp, user context, and outcome
5. **Heartbeat**: Periodic health checks ensure connectivity and permissions remain valid

---

## Part 1: Core MCP Servers

### 1.1 Azure DevOps MCP Server

**Purpose**: Read-only access to pipelines, work items, logs, and PRs  
**Status**: Required for MVP  
**Security Level**: Read-only by default

#### Configuration

```yaml
name: "azure-devops-read"
type: "mcp-server"
host: "dev.azure.com"
organization: "isagri"  # or company Isagri uses
protocol: "https"
version: "7.0"
authentication:
  type: "PAT"  # Personal Access Token
  token_env: "ADO_PAT"
  scopes:
    - "vso.code_read"       # Read code/PRs
    - "vso.build_read"      # Read pipelines
    - "vso.work_read"       # Read work items
    - "vso.release_read"    # Read releases
permissions:
  read: 
    - "pipelines"
    - "logs"
    - "workitems"
    - "pullrequests"
    - "builds"
  write: []  # Disabled for MVP
  execute: []
timeout_seconds: 30
retry_policy:
  max_attempts: 3
  backoff_ms: 1000
heartbeat:
  interval_seconds: 300
  endpoint: "/status"
  healthcheck: "true"
```

#### Environment Setup

```bash
# In production deployment (.env.production or secrets manager)
export ADO_PAT="<Personal Access Token with vso.code_read, vso.build_read, vso.work_read>"
export ADO_ORGANIZATION="isagri"
export ADO_PROJECT_ID="<project_guid>"

# Verify connectivity
curl -H "Authorization: Basic $(echo -n \":${ADO_PAT}\" | base64)" \
  https://dev.azure.com/isagri/_apis/build/definitions?api-version=7.0
```

#### Supported Operations (MVP)

| Operation | Endpoint | Permission | Status |
|-----------|----------|-----------|--------|
| List pipelines | `/build/definitions` | read | ✅ Implemented |
| Get pipeline details | `/build/definitions/{id}` | read | ✅ Implemented |
| Get build logs | `/build/builds/{id}/logs` | read | ✅ Implemented |
| List work items | `/work/workitems` | read | ✅ Implemented |
| Get work item | `/work/workitems/{id}` | read | ✅ Implemented |
| List pull requests | `/git/pullrequests` | read | ✅ Implemented |
| Add work item comment | `/wit/workitems/{id}/comments` | write | ⏸️ Draft mode only (P3) |

---

### 1.2 Digital.ai Release MCP Server

**Purpose**: Read diagnostic data from Digital.ai Release; NO execute capability in MVP  
**Status**: Required for MVP (read-only)  
**Security Level**: Read-only + Custom skill for diagnostics

#### Configuration

```yaml
name: "dai-release-read"
type: "mcp-server"
host: "<dai.isagri.internal or cloud instance>"
protocol: "https"
version: "latest"
authentication:
  type: "API_KEY"
  key_env: "DAI_API_KEY"
  scopes:
    - "releases:read"
    - "templates:read"
    - "tasks:read"
permissions:
  read:
    - "releases"
    - "templates"
    - "phases"
    - "tasks"
    - "deployments"
  write: []  # Disabled for MVP
  execute: []
timeout_seconds: 45
retry_policy:
  max_attempts: 2
  backoff_ms: 2000
heartbeat:
  interval_seconds: 600
  endpoint: "/api/v1/system/status"
  healthcheck: "true"
custom_skill:
  name: "ai-release-diagnostic-skill"
  language: "python"
  path: "skills/dai_diagnostic.py"
  purpose: "Analyze release status and suggest actions (read-only)"
```

#### Environment Setup

```bash
export DAI_URL="https://dai.isagri.internal"
export DAI_API_KEY="<api_key_with_releases_read_permission>"
export DAI_HEARTBEAT_ENABLED="true"

# Verify connectivity
curl -H "Authorization: Bearer ${DAI_API_KEY}" \
  ${DAI_URL}/api/v1/releases?state=ACTIVE&limit=10
```

#### Custom Skill: `ai_release_diagnostic.py`

```python
"""
Digital.ai Release Diagnostic Skill (Read-Only)

Analyzes release status and suggests actions without executing.
All execution requires explicit human approval and separate MCP write call.
"""

from datetime import datetime, timedelta

def diagnose_release(release_id: str, dai_client) -> dict:
    """
    Diagnose a release for blockers, delays, and failure patterns.
    
    Args:
        release_id: Digital.ai release ID
        dai_client: Authenticated DAI MCP client
        
    Returns:
        dict with diagnosis: {
            "status": "ACTIVE|BLOCKED|FAILED",
            "blockers": [...],
            "failing_tasks": [...],
            "recommendations": [...]
        }
    """
    release = dai_client.releases.get(release_id)
    
    diagnosis = {
        "release_id": release_id,
        "title": release.get("title"),
        "status": release.get("status"),
        "start_date": release.get("startDate"),
        "due_date": release.get("dueDate"),
        "blockers": [],
        "failing_tasks": [],
        "recommendations": []
    }
    
    # Identify blockers
    for phase in release.get("phases", []):
        for task in phase.get("tasks", []):
            if task.get("status") == "FAILED":
                diagnosis["failing_tasks"].append({
                    "phase": phase.get("title"),
                    "task": task.get("title"),
                    "error": task.get("errorMessage")
                })
            elif task.get("status") == "PENDING" and is_blocked(task):
                diagnosis["blockers"].append({
                    "phase": phase.get("title"),
                    "task": task.get("title"),
                    "reason": get_blocker_reason(task)
                })
    
    # Generate recommendations
    diagnosis["recommendations"] = generate_recommendations(diagnosis)
    
    return diagnosis

def is_blocked(task: dict) -> bool:
    """Check if task is blocked on dependencies."""
    return task.get("precondition") and not task.get("precondition_met", False)

def get_blocker_reason(task: dict) -> str:
    """Extract blocker reason from task metadata."""
    return task.get("blockMessage", "Unknown blocker")

def generate_recommendations(diagnosis: dict) -> list:
    """Generate actionable recommendations based on diagnosis."""
    recs = []
    
    if diagnosis.get("failing_tasks"):
        recs.append({
            "action": "retry_failed_phase",
            "description": "Retry the failed phase after fixing the issue",
            "risk": "MEDIUM"
        })
    
    if len(diagnosis.get("blockers", [])) > 2:
        recs.append({
            "action": "escalate_to_devops",
            "description": "Multiple blockers detected - escalate to DevOps team",
            "risk": "HIGH"
        })
    
    return recs
```

#### Supported Operations (MVP)

| Operation | Endpoint | Permission | Status |
|-----------|----------|-----------|--------|
| List releases | `/api/v1/releases` | read | ✅ Implemented |
| Get release details | `/api/v1/releases/{id}` | read | ✅ Implemented |
| Get release phases | `/api/v1/releases/{id}/phases` | read | ✅ Implemented |
| Get task status | `/api/v1/releases/{id}/tasks/{taskId}` | read | ✅ Implemented |
| Run diagnostic skill | Custom skill (read-only) | read | ✅ Implemented |
| Start release | `/api/v1/releases/{id}/start` | write | ❌ Not in MVP |
| Complete task | `/api/v1/releases/{id}/tasks/{taskId}/complete` | write | ❌ Not in MVP |

---

### 1.3 Microsoft Teams MCP Server

**Purpose**: Send notifications, receive approvals via interactive cards  
**Status**: Required for MVP  
**Security Level**: Write-only to dedicated channel, no read of message history

#### Configuration

```yaml
name: "teams-notifications"
type: "mcp-server"
host: "teams.microsoft.com"
protocol: "webhook"
version: "1.0"
authentication:
  type: "WEBHOOK_URL"
  webhook_env: "TEAMS_WEBHOOK_URL"
  # Webhook scoped to single channel (OPENCLAW-DIAGNOSTICS)
permissions:
  read: []  # No read for MVP
  write:
    - "messages"
    - "interactive_cards"
  execute: []
timeout_seconds: 10
heartbeat:
  interval_seconds: 3600
  endpoint: "ping"  # Webhook doesn't support health checks
  healthcheck: "false"
message_templates:
  - name: "diagnosis_card"
    path: "templates/teams_diagnosis_card.json"
  - name: "approval_card"
    path: "templates/teams_approval_card.json"
```

#### Environment Setup

```bash
# Teams Webhook URL (channel-scoped, never commit to git)
export TEAMS_WEBHOOK_URL="https://outlook.webhook.office.com/webhookb2/..."

# Verify connectivity (Teams will return 200 OK)
curl -X POST ${TEAMS_WEBHOOK_URL} \
  -H "Content-Type: application/json" \
  -d '{"text":"OpenClaw connectivity test"}'
```

#### Teams Channel Setup

**Channel Name**: `OPENCLAW-DIAGNOSTICS`  
**Purpose**: Real-time pipeline diagnostics and approval requests  
**Members**: DevOps team + OpenClaw bot  
**Retention**: 90 days (Teams default)

**Approval Workflow**:
1. Bot sends **Adaptive Card** with diagnosis + action plan
2. Card includes two buttons: **Approve** / **Reject**
3. User clicks button → webhook sends callback to OpenClaw
4. OpenClaw validates approval source (DevOps team member)
5. Action logged in audit trail

#### Adaptive Card Templates

**File**: `templates/teams_diagnosis_card.json`

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
          "type": "ColumnSet",
          "columns": [
            {
              "width": "stretch",
              "items": [
                {
                  "type": "TextBlock",
                  "text": "🔴 Pipeline Failure Detected",
                  "size": "large",
                  "weight": "bolder"
                }
              ]
            },
            {
              "width": "auto",
              "items": [
                {
                  "type": "TextBlock",
                  "text": "${timestamp}",
                  "size": "small",
                  "color": "warning"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "Container",
      "body": [
        {
          "type": "TextBlock",
          "text": "Pipeline: ${pipelineName}",
          "weight": "bolder",
          "size": "medium"
        },
        {
          "type": "TextBlock",
          "text": "Build #${buildNumber} failed",
          "size": "default"
        }
      ]
    },
    {
      "type": "Container",
      "body": [
        {
          "type": "TextBlock",
          "text": "Root Cause Analysis",
          "weight": "bolder"
        },
        {
          "type": "TextBlock",
          "text": "${rootCause}",
          "wrap": true,
          "size": "default"
        }
      ]
    },
    {
      "type": "Container",
      "body": [
        {
          "type": "TextBlock",
          "text": "Recommended Action",
          "weight": "bolder"
        },
        {
          "type": "TextBlock",
          "text": "${recommendedAction}",
          "wrap": true,
          "size": "default"
        }
      ]
    },
    {
      "type": "Container",
      "body": [
        {
          "type": "TextBlock",
          "text": "Approval Required (Expires in 30 min)",
          "weight": "bolder",
          "color": "warning"
        }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "✅ Approve",
      "url": "https://openclaw.internal/approve?id=${diagnosisId}&token=${approvalToken}"
    },
    {
      "type": "Action.OpenUrl",
      "title": "❌ Reject",
      "url": "https://openclaw.internal/reject?id=${diagnosisId}&token=${approvalToken}"
    },
    {
      "type": "Action.OpenUrl",
      "title": "📋 View Details",
      "url": "https://dev.azure.com/isagri/_build/results?buildId=${buildNumber}"
    }
  ]
}
```

---

## Part 2: Authentication & Authorization

### 2.1 Service Principal (Azure DevOps + Teams)

**Name**: `OpenClaw-ServicePrincipal`  
**Scope**: Isagri Azure AD tenant  
**Permissions**:
- **Azure DevOps**: Read work items, read builds, read releases, add comments (P3)
- **Teams**: Send messages to `OPENCLAW-DIAGNOSTICS` channel only

**Setup**:

```bash
# Register app in Azure AD
az ad app create \
  --display-name "OpenClaw-PFE" \
  --sign-in-audience AzureADMyOrg

APP_ID=$(az ad app list --filter "displayName eq 'OpenClaw-PFE'" --query '[0].id' -o tsv)

# Create service principal
az ad sp create --id ${APP_ID}

# Grant Azure DevOps permissions (via Azure DevOps admin)
# - Organization: isagri
# - Scope: vso.code_read, vso.build_read, vso.work_read, vso.release_read

# Grant Teams permissions (via Teams admin)
# - Channel: OPENCLAW-DIAGNOSTICS
# - Permission: Send messages, create cards
```

### 2.2 API Keys & Tokens

| Service | Auth Method | Storage | Rotation |
|---------|------------|---------|----------|
| Azure DevOps | PAT | AWS Secrets Manager | 90 days |
| Digital.ai Release | API Key | AWS Secrets Manager | 90 days |
| Teams | Webhook URL | AWS Secrets Manager | Manual (if leaked) |

---

## Part 3: Dry-Run Mode Configuration

**Purpose**: All state-changing operations tested in dry-run before production  
**Activation**: Environment variable `OPENCLAW_DRY_RUN=true`  
**Behavior**:

```python
# Example: Dry-run for "add comment to work item"
if os.getenv("OPENCLAW_DRY_RUN") == "true":
    # Log action instead of executing
    logger.info(f"[DRY-RUN] Would add comment to WI {wi_id}: {comment_text}")
    audit.log("DRY_RUN_ACTION", {"action": "add_comment", "wi_id": wi_id})
    return {"status": "ok_dry_run", "action_id": None}
else:
    # Execute for real
    result = ado_client.workitems.add_comment(wi_id, comment_text)
    audit.log("EXECUTED_ACTION", {"action": "add_comment", "result": result})
    return result
```

---

## Part 4: Security & Validation (Q1-Q6 BLOCKERS Resolution)

### Q1: ✅ MCP Server URLs Documented

**Resolution**: This document specifies all URLs:
- Azure DevOps: `https://dev.azure.com/isagri`
- Digital.ai: `https://dai.isagri.internal` (or cloud URL)
- Teams: `https://outlook.webhook.office.com/webhookb2/...`

### Q2: ✅ Credentials & Token Management Defined

**Resolution**: Stored in AWS Secrets Manager:
- `openclaw/ado-pat`
- `openclaw/dai-api-key`
- `openclaw/teams-webhook-url`

### Q3: ✅ Dry-Run Mode Documented

**Resolution**: Section 3 above + implementation template provided

### Q4: ✅ Audit Trail Approach Specified

**Resolution**: All MCP calls logged with:
- Timestamp, caller, operation, parameters, outcome
- Storage: SQLite (MVP) → PostgreSQL (V2)

### Q5: ✅ LDAP/SSO Configuration Path Identified

**Resolution**: Uses Azure AD service principal (no LDAP for MVP)  
See Section 2.1 for setup.

### Q6: ✅ Teams Webhook Setup Documented

**Resolution**: Section 1.3 + channel setup + Adaptive Card templates included.

---

## Part 5: Checklist for MVP Deployment

- [ ] Azure DevOps PAT created with scopes: `vso.code_read`, `vso.build_read`, `vso.work_read`
- [ ] Digital.ai Release API key created with `releases:read` permission
- [ ] Teams webhook URL generated for `OPENCLAW-DIAGNOSTICS` channel
- [ ] AWS Secrets Manager configured with 3 secrets
- [ ] OpenClaw environment variables set (dev, staging, prod)
- [ ] MCP health checks passing (ADO, DAI, Teams)
- [ ] Dry-run mode tested in staging (log-only, no changes)
- [ ] Approval flow tested (diagnosis → Teams card → approve/reject)
- [ ] Audit trail verified in SQLite
- [ ] Security review completed by InfoSec team
- [ ] Production deployment approved by Isagri DevOps lead

---

## Part 6: Troubleshooting

### Connectivity Issues

```bash
# Test Azure DevOps
curl -v -H "Authorization: Basic $(echo -n :${ADO_PAT} | base64)" \
  https://dev.azure.com/isagri/_apis/projects

# Test Digital.ai
curl -v -H "Authorization: Bearer ${DAI_API_KEY}" \
  https://dai.isagri.internal/api/v1/system/status

# Test Teams webhook
curl -X POST ${TEAMS_WEBHOOK_URL} \
  -d '{"text":"Test message"}' \
  -H "Content-Type: application/json"
```

### Permission Errors

- **ADO**: Verify PAT scopes in Organization Settings → Personal access tokens
- **DAI**: Verify API key in Digital.ai → API → Management
- **Teams**: Verify webhook URL points to correct channel; regenerate if needed

---

## References

- [ADR-009: Diagnostic System Architecture](../decisions/ADR-009-systeme-diagnostic.md)
- [Azure DevOps REST API](https://docs.microsoft.com/en-us/rest/api/azure/devops)
- [Digital.ai Release API](https://docs.digital.ai/release/latest/reference/rest-api.html)
- [Microsoft Teams Webhook Integration](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using)
- [BLOCKERS.md](../BLOCKERS.md) — Q1-Q6 answered by this document

---

**Status**: Ready for MVP deployment  
**Last Reviewed**: 2026-04-22  
**Next Review**: After first production run

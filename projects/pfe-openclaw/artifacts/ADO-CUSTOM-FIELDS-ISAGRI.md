# Azure DevOps Custom Fields — Isagri Configuration

**Document Version**: 1.0  
**Last Updated**: 2026-04-22  
**Status**: Configuration Guide  
**Owner**: DevOps + Security team

---

## Overview

This document specifies the **custom work item fields** used by Isagri in Azure DevOps that OpenClaw must understand and interact with.

### Design Principle

- OpenClaw treats custom fields **as read-only metadata** in MVP
- Custom fields used only for **context enrichment**, not workflow control
- Future versions (V2) can implement custom field mutations

---

## Part 1: Isagri Custom Fields Inventory

### Known Custom Fields (to be verified with Isagri)

| Field Name | Internal ID | Type | Purpose | MVP Usage | Notes |
|------------|-------------|------|---------|-----------|-------|
| `Platform` | `custom.platform` | Dropdown | Target platform (API, Web, Mobile, Infra) | Read | Used to categorize incidents |
| `SLA Level` | `custom.sla_level` | Dropdown | SLA tier (P0, P1, P2, P3) | Read | Affects approval timeout |
| `Affected Customers` | `custom.affected_customers` | String (multi) | List of customer IDs | Read | For context in diagnostic |
| `Environment` | `custom.environment` | Dropdown | Prod/Staging/Dev | Read | Determines alert urgency |
| `Cost Center` | `custom.cost_center` | String | Billing code | Read | For audit trail |
| `Security Classification` | `custom.security_class` | Dropdown | Public/Internal/Secret | Read | Determines log retention |

### Unknown Fields (BLOCKERS)

**Status**: ❓ Not yet specified  
**Action Required**: Contact Isagri DevOps team to provide:

```yaml
# Template to request from Isagri
isagri_custom_fields:
  - name: "<Field Display Name>"
    internal_id: "<Field Reference Name>"
    type: "String|Integer|DateTime|Dropdown|Boolean|MultiSelect"
    values: "[for Dropdowns]"
    description: "Purpose of field"
    required_for_incidents: "true|false"
    openclaw_usage: "read|write"
```

---

## Part 2: OpenClaw Field Access

### MCP Azure DevOps Integration

OpenClaw accesses custom fields via **existing ADO MCP server** (integrated in OpenCode):

```python
# Pseudo-code: Reading custom fields
work_item = ado_mcp.workitems.get(
    id=incident_id,
    fields=["custom.platform", "custom.sla_level", "custom.environment"]
)

print(f"Platform: {work_item['fields']['custom.platform']}")
print(f"SLA: {work_item['fields']['custom.sla_level']}")
```

### Field Retrieval in Diagnostic

When OpenClaw generates a diagnostic for an incident:

1. Read base WI fields (title, description, assignee)
2. Read custom fields (platform, SLA, environment)
3. Include custom fields in **diagnostic context card** sent to Teams
4. Store custom fields in **audit trail** (SQLite)

---

## Part 3: Configuration Tasks (Before MVP Deployment)

- [ ] **Contact Isagri DevOps**: Request list of all custom fields in use
- [ ] **Document field definitions**: Create extended inventory with all properties
- [ ] **Test MCP field access**: Verify ADO MCP can read each custom field
- [ ] **Add fields to diagnostic template**: Update Teams Adaptive Card to display relevant custom fields
- [ ] **Verify audit logging**: Ensure custom fields captured in SQLite audit table

---

## Part 4: Schema Update (SQLite)

When custom fields are confirmed, extend audit schema:

```sql
-- Add column to audit table (if not exists)
ALTER TABLE audit_log ADD COLUMN custom_fields TEXT; -- JSON-encoded

-- Example audit entry with custom fields
INSERT INTO audit_log 
  (action, work_item_id, custom_fields, timestamp)
VALUES (
  'diagnostic_created',
  123456,
  '{"platform":"API","sla_level":"P1","environment":"prod"}',
  datetime('now')
);

-- Query: Find all P1 incidents in production
SELECT * FROM audit_log 
WHERE json_extract(custom_fields, '$.sla_level') = 'P1'
AND json_extract(custom_fields, '$.environment') = 'prod';
```

---

## Part 5: Future (V2+)

Once custom field configuration is stable, OpenClaw could:

- ✅ Automatically escalate based on SLA level (custom field)
- ✅ Route incidents by platform (custom field)
- ✅ Generate cost reports by cost center (custom field)
- ✅ Enforce security classification rules (custom field)

---

## References

- [MCP Azure DevOps Integration](https://opencode.ai/docs/mcp) (OpenCode docs)
- [Azure DevOps Custom Fields API](https://docs.microsoft.com/en-us/rest/api/azure/devops/wit/fields)
- [Isagri Work Item Template](../artifacts/00-CONTEXTE-PROJET.md)

---

**Status**: Awaiting Isagri field inventory  
**Blocker**: Q7 (custom fields list)  
**Next Step**: Provide custom field list, then execute configuration tasks

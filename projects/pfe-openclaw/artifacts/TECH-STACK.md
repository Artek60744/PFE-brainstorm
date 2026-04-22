# Tech Stack — Centralized Definition

**Document Version**: 1.0  
**Last Updated**: 2026-04-22  
**Status**: Reference Guide  
**Owner**: Architecture + DevOps team

---

## Overview

This document **centralizes the technology stack** for OpenClaw, eliminating redundant definitions scattered across PROJECT.md, project.yaml, decisions, and artifacts.

### Single Source of Truth

All references to "tech stack" should point to this document.

---

## Core Architecture

```
┌──────────────────────────────────────────────────────┐
│                   OpenClaw Agent                      │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐    │
│  │ Read   │→ │ Plan   │→ │Approve │→ │Execute │    │
│  │(MCP)   │  │(LLM)   │  │(Teams) │  │(Draft) │    │
│  └────────┘  └────────┘  └────────┘  └────────┘    │
└──────────────────────────────────────────────────────┘
       ↓            ↓            ↓            ↓
   Azure DevOps  Digital.ai    Teams       Audit
   (via MCP)     (via MCP)    (webhook)    (SQLite)
```

---

## Part 1: Component Stack

### 1.1 Agent Framework

| Component | Technology | Version | Purpose | Notes |
|-----------|-----------|---------|---------|-------|
| **Agent Runtime** | OpenClaw | Latest | Read-Plan-Approve-Execute orchestration | Open-source, persistent memory |
| **Integration Protocol** | MCP (Model Context Protocol) | 1.0+ | Safe system integrations | Integrated in OpenCode |
| **Language** | Python | 3.10+ | Dashboard + diagnostic logic | FastAPI web framework |

**References**:
- ADR-001: OpenClaw as framework
- ADR-002: MCP as protocol

### 1.2 External Integrations (via MCP)

#### Azure DevOps

| Layer | Technology | Provider | Use Case |
|-------|-----------|----------|----------|
| **Read** | ADO REST API 7.0 | Microsoft | Pipelines, build logs, work items |
| **MCP Server** | azure-devops (OpenCode) | Integrated | Safe read/write access |
| **Auth** | PAT (Personal Access Token) | Azure AD | Service identity |

**ADR**: ADR-002, ADR-009

#### Digital.ai Release

| Layer | Technology | Provider | Use Case |
|-------|-----------|----------|----------|
| **Read** | DAI REST API | Digital.ai | Release status, task info |
| **MCP Server** | dai-release (OpenCode) | Integrated | Read-only diagnostics |
| **Auth** | API Key | Digital.ai | Service identity |

**ADR**: ADR-014 (polling 30s)

#### Teams Notifications

| Layer | Technology | Provider | Use Case |
|-------|-----------|----------|----------|
| **Write** | Teams Webhook | Microsoft | Send diagnostic cards |
| **Format** | Adaptive Cards | Microsoft | Interactive approval UI |
| **Auth** | Webhook URL | Teams | Channel-scoped |

**Stored in**: AWS Secrets Manager, never in git

**ADR**: ADR-004 (Teams only, no Slack)

### 1.3 Dashboard Backend

| Component | Technology | Version | Purpose | Notes |
|-----------|-----------|---------|---------|-------|
| **Web Framework** | FastAPI | 0.100+ | REST API + Async | Lightweight, modern |
| **Authentication** | Azure AD + OIDC | Microsoft | SSO via corporate credentials | Replaces local LDAP |
| **CORS** | fastapi-cors | Latest | Cross-origin requests | Configurable by environment |
| **Templates** | Jinja2 | 3.0+ | Server-side rendering | HTMX integration |
| **JavaScript Framework** | HTMX | 1.9+ | Dynamic UX without full reload | Minimal bundle size |
| **HTTP Server** | Uvicorn | 0.23+ | ASGI application server | Async-native |

**ADR**: ADR-010 (FastAPI + HTMX)

### 1.4 Data Storage

#### Primary Database (MVP)

| Component | Technology | Version | Purpose | Timeline |
|-----------|-----------|---------|---------|----------|
| **Database** | SQLite | 3.40+ | Incident archive + audit | S1-S15 (MVP) |
| **Schema** | schema.sql + schema_dai.sql | Version-controlled | ADO + DAI incidents | SQL files in repo |
| **File Location** | `artifacts/dashboard/openclaw.db` | Single file | Local deployment | Moved to PostgreSQL in V2 |

**ADR**: ADR-003 (SQLite for POC)

#### Future Database (V2+)

| Component | Technology | Version | Purpose | Timeline |
|-----------|-----------|---------|---------|----------|
| **Database** | PostgreSQL | 14+ | Production-grade analytics | S16+ (Post-MVP) |
| **Schema** | Enhanced with JSONB | Version-controlled | Better indexing, scalability | See DATABASE-MIGRATION-PLAN.md |
| **Replication** | Streaming replication | High availability | Hot standby | Post-PFE |

**Plan**: DATABASE-MIGRATION-PLAN.md

### 1.5 Audit Trail

| Component | Technology | Purpose | Storage |
|-----------|-----------|---------|---------|
| **Action Logging** | SQLite audit_log table | Compliance + debugging | Local DB (MVP) |
| **Fields** | (action, actor, timestamp, outcome) | Immutable trail | JSON for custom fields |
| **Retention** | 90 days rolling | GDPR/compliance | Archived to S3 (V2) |
| **Querying** | SQL + Python | Analytics + reporting | Monthly reports |

### 1.6 Infrastructure

| Component | Environment | Technology | Notes |
|-----------|-------------|-----------|-------|
| **Dev** | Laptop / Local | Docker Compose | SQLite in-memory for tests |
| **Staging** | Isagri staging | Docker + K8s | SQLite mounted volume |
| **Production** | Isagri production | Docker + K8s | PostgreSQL + HA setup (V2) |
| **Secrets** | All environments | AWS Secrets Manager | PAT, API keys, webhook URLs |
| **CI/CD** | Azure Pipelines | OpenCode agents | Build, test, deploy |
| **Monitoring** | Production | Application Insights | Logs, metrics, health checks |

---

## Part 2: Development Stack

### 2.1 Languages & Frameworks

```python
# Core dependencies (requirements.txt)
fastapi==0.100.0              # Web framework
uvicorn==0.23.0               # ASGI server
aiohttp==3.8.0                # Async HTTP client
msal==1.24.0                  # Azure AD auth
pydantic==2.0.0               # Data validation
python-dotenv==1.0.0          # Environment config
sqlite3                       # Built-in (MVP)
psycopg2-binary==2.9.0        # PostgreSQL (V2)
```

### 2.2 Templating

```html
<!-- Frontend: HTMX + Jinja2 -->
<div hx-get="/api/incidents" hx-trigger="load">
  Loading...
</div>
```

### 2.3 Testing

| Tool | Purpose | Framework |
|------|---------|-----------|
| pytest | Unit tests | Python test runner |
| pytest-asyncio | Async tests | FastAPI endpoints |
| mock / unittest.mock | Mocking MCP services | Built-in Python |
| testclient | Integration tests | FastAPI test client |

### 2.4 Documentation

| Tool | Format | Purpose |
|------|--------|---------|
| Markdown | .md files | Technical documentation |
| Docstrings | Python | Code documentation |
| ADR | Architecture Decision Records | Design rationale |

---

## Part 3: Deployment Artifacts

### 3.1 Containerization

```dockerfile
# Dockerfile (MVP)
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY dashboard/ .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3.2 Orchestration

```yaml
# docker-compose.yml (local dev)
version: '3'
services:
  openclaw_dashboard:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AZURE_AD_CLIENT_ID=${AZURE_AD_CLIENT_ID}
      - DATABASE_URL=sqlite:///./openclaw.db
    volumes:
      - ./artifacts/dashboard:/app
```

### 3.3 Kubernetes (Future)

```yaml
# deployment.yaml (production V2)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: openclaw-dashboard
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: dashboard
        image: isagri/openclaw-dashboard:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: openclaw-secrets
              key: postgres-url
```

---

## Part 4: API Specifications

### 4.1 REST Endpoints

```
GET  /api/incidents             # List recent incidents
GET  /api/incidents/:id         # Get incident details
GET  /api/diagnostics           # List diagnostics (paginated)
POST /api/approve               # Submit approval
POST /api/reject                # Submit rejection
GET  /api/audit-log             # Query audit trail
```

### 4.2 Response Format

```json
{
  "status": "ok|error",
  "data": { ... },
  "timestamp": "2026-04-22T10:00:00Z",
  "error": "null|error message"
}
```

---

## Part 5: Security Specifications

### 5.1 Authentication

| Method | Where | Scope |
|--------|-------|-------|
| Azure AD OIDC | Dashboard + API | User identity |
| PAT | Azure DevOps MCP | Service identity |
| API Key | Digital.ai MCP | Service identity |
| Webhook URL | Teams | Channel-scoped, secret |

**ADR**: ADR-012 (trust boundary)

### 5.2 Encryption

| Data | Transport | Storage |
|------|-----------|---------|
| Tokens | TLS 1.3 | HttpOnly cookies |
| Credentials | TLS 1.3 | AWS Secrets Manager |
| API Keys | TLS 1.3 | Environment variables |
| Audit logs | SQLite | Plaintext (no PII in MVP) |

### 5.3 Access Control

| Role | Approval Level | Dashboard Access |
|------|----------------|------------------|
| DevOps Admin | L1/L2/L3 | Full |
| DevOps Engineer | L1/L2 | Full (read + approve) |
| Viewer | None | Read-only |

---

## Part 6: Performance Targets

### 6.1 Latency SLOs

| Operation | Target | Notes |
|-----------|--------|-------|
| Incident detection | < 2 min | Via heartbeat polling |
| Diagnostic generation | < 5 min | Includes MCP calls |
| Approval notification | < 30 sec | Teams webhook |
| Dashboard page load | < 2 sec | Cached incidents |

### 6.2 Throughput Capacity

| Metric | MVP | V2 (Post-PFE) |
|--------|-----|---------------|
| Incidents/day | 10-20 | 50-100 |
| Concurrent users | 5-10 | 50+ |
| API RPS | 10 | 100+ |

**Scaling strategy**: SQLite → PostgreSQL + horizontal scaling (V2)

---

## Part 7: Dependency Matrix

### Direct Dependencies

```
OpenClaw
  ├── MCP (ADO) ← Azure DevOps REST API
  ├── MCP (DAI) ← Digital.ai REST API
  ├── FastAPI ← Pydantic, Uvicorn
  ├── Azure AD ← MSAL library
  └── SQLite3

Dashboard
  ├── FastAPI
  ├── HTMX
  ├── Jinja2
  └── SQLite3
```

### External Services

```
Isagri Infrastructure
  ├── Azure DevOps (for pipeline data)
  ├── Digital.ai Release (for release data)
  ├── Azure AD (for authentication)
  ├── Microsoft Teams (for approvals)
  └── AWS Secrets Manager (for credentials)
```

---

## Part 8: Version Compatibility Matrix

### Supported Versions

| Component | Minimum | Current | Maximum | EOL |
|-----------|---------|---------|---------|-----|
| Python | 3.9 | 3.10 | 3.11 | 2025-10 |
| FastAPI | 0.95 | 0.100 | Latest | N/A |
| SQLite | 3.35 | 3.40 | Latest | N/A |
| PostgreSQL | 12 | 14 | 16 | 2026-10 |
| Azure AD | v1.0 | v2.0 | Latest | N/A |

---

## Part 9: Cost Estimate (Annual)

| Component | MVP | V2 | Notes |
|-----------|-----|----|----|
| Azure AD | $0 | $0 | Isagri existing |
| Azure DevOps | $0 | $0 | Isagri existing |
| Digital.ai | $0 | $0 | Isagri existing |
| Teams | $0 | $0 | Isagri existing |
| AWS Secrets Manager | ~$600 | ~$600 | For credentials |
| PostgreSQL (V2) | N/A | ~$2,400-7,200 | Managed service |
| **Total** | **~$600** | **~$3,000-7,800** | |

---

## Part 10: Migration Path (MVP → V2)

```
MVP (S1-S15): All SQLite, Python 3.10, FastAPI 0.100
    ↓ (Database migration plan)
V1 (S16-S20): Dual-write SQLite+PostgreSQL, upgrade to 3.11
    ↓ (Performance optimization)
V2 (Post-PFE): PostgreSQL-only, Kubernetes scaling, Python 3.11+
```

---

## Operational Checklist

- [ ] All technologies vetted by security team
- [ ] Licenses verified (open-source compliance)
- [ ] Version constraints documented in requirements.txt
- [ ] Docker image built and tested
- [ ] CI/CD pipeline configured for automated builds
- [ ] Monitoring alerts configured for critical dependencies
- [ ] Vendor lock-in risks identified
- [ ] Backup/recovery procedures documented
- [ ] Cost projections reviewed

---

## References

- **ADR-001**: OpenClaw framework choice
- **ADR-002**: MCP protocol adoption
- **ADR-003**: SQLite for MVP
- **ADR-004**: Teams (not Slack)
- **ADR-010**: FastAPI + HTMX
- **ADR-014**: DAI polling strategy
- **MCP-CONFIGURATION.md**: Server setup details
- **DATABASE-MIGRATION-PLAN.md**: SQLite → PostgreSQL roadmap

---

**Status**: Reference document  
**Maintenance**: Update when tech changes  
**Owner**: Architecture team  
**Last Review**: 2026-04-22

# SSO/LDAP Authentication Configuration

**Document Version**: 1.0  
**Last Updated**: 2026-04-22  
**Status**: Configuration Guide  
**Owner**: Security + Infrastructure team

---

## Overview

This document specifies the **authentication strategy** for OpenClaw dashboard access using Azure AD (Single Sign-On).

### Resolution of BLOCKER Q5

**Q5**: How to configure LDAP/SSO for dashboard access?  
**Answer**: Use Azure AD via OpenCode MCP Microsoft server (already integrated)

---

## Part 1: Authentication Architecture (MVP)

### Choice: Azure AD (via OpenCode MCP)

OpenClaw uses **Azure AD for authentication** (Isagri's identity provider):

- OpenCode MCP already integrates with **Microsoft identity services**
- OpenClaw dashboard runs behind **Azure AD authentication middleware**
- User logs in with **Isagri corporate credentials**
- Dashboard verifies token via Azure AD + role-based access control (RBAC)

### No Local LDAP Required

Isagri's LDAP is **not directly used** — instead:

1. Azure AD is the **source of truth** for Isagri users
2. OpenCode MCP handles **OAuth2/OIDC flows** to Azure AD
3. Dashboard receives **authenticated JWT token**
4. JWT decoded to extract user info + group membership

---

## Part 2: Azure AD Application Setup

### Step 1: Register OpenClaw App in Azure AD

**Portal**: https://portal.azure.com → Azure Active Directory → App registrations

```
Application name: OpenClaw-Dashboard
Supported account types: Single tenant (Isagri only)
Redirect URI: https://openclaw.isagri.internal/auth/callback
```

### Step 2: Configure Credentials

1. Go to **Certificates & secrets**
2. Create new **Client Secret**
   - Name: `openclaw-dashboard-secret`
   - Expiry: 1 year (set renewal reminder)
3. **Copy the secret** → Store in AWS Secrets Manager

```bash
aws secretsmanager create-secret \
  --name openclaw/azure-ad-client-secret \
  --secret-string "xxxxx-generated-secret-xxxxx"
```

### Step 3: Grant API Permissions

In **API permissions**, add:

```
Microsoft Graph
├── Directory.Read.All (Application)  # Read user/group info
├── User.Read (Delegated)             # Read current user
└── User.Read.All (Application)       # Read all users

Azure DevOps
├── vso.work_read (Delegated)         # Read work items (optional, redundant with MCP)
```

---

## Part 3: RBAC — Roles & Permissions

### OpenClaw Dashboard Roles

| Role | Members | Permissions | Dashboard Access |
|------|---------|-------------|------------------|
| **DevOps Admin** | Team leads | Full access, approve all levels | ✅ Full |
| **DevOps Engineer** | On-call engineers | Create diagnostics, approve L1/L2 | ✅ Full (read + approve) |
| **Viewer** | Managers, leads (optional) | Read-only, no approval | ✅ View only |
| **Excluded** | Developers, other teams | None | ❌ Denied |

### Azure AD Groups

Create in Azure AD:

```
Group: openclaw-dashboardusers
  ├── openclaw-devops-admin (App Owner, Team Leads)
  ├── openclaw-devops-engineers (On-Call Rotation)
  └── openclaw-viewers (Managers)
```

### Membership Management

**Add users to groups**:

```bash
# Via Azure Portal
1. Azure AD → Groups → openclaw-dashboardusers
2. Members → Add members → Select users
3. Assign roles via FastAPI middleware (see Part 4)
```

---

## Part 4: Dashboard Authentication Middleware (FastAPI)

### Installation

```bash
# Add to requirements.txt
fastapi-aad-auth>=1.0.0
aiohttp
msal
```

### Configuration

```python
# dashboard/auth.py
from fastapi_aad_auth import AADAuth
from fastapi import FastAPI, Depends, HTTPException
import os

app = FastAPI()

# Azure AD configuration
aad_auth = AADAuth(
    client_id=os.getenv("AZURE_AD_CLIENT_ID"),
    client_secret=os.getenv("AZURE_AD_CLIENT_SECRET"),
    tenant_id=os.getenv("AZURE_AD_TENANT_ID"),
    authority="https://login.microsoftonline.com",
    scopes=["https://graph.microsoft.com/.default"]
)

# Role mapping
ROLE_PERMISSIONS = {
    "openclaw-devops-admin": ["read", "approve_l1", "approve_l2", "approve_l3"],
    "openclaw-devops-engineers": ["read", "approve_l1", "approve_l2"],
    "openclaw-viewers": ["read"]
}

async def get_current_user(token: str = Depends(aad_auth.get_token)):
    """Extract user from JWT token."""
    try:
        user_info = aad_auth.decode_token(token)
        return {
            "user_id": user_info["oid"],
            "email": user_info["upn"],
            "name": user_info["name"],
            "groups": user_info.get("groups", [])
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

async def require_permission(permission: str):
    """Check if user has required permission."""
    async def _check(current_user = Depends(get_current_user)):
        user_groups = current_user["groups"]
        
        for group in user_groups:
            if permission in ROLE_PERMISSIONS.get(group, []):
                return current_user
        
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return _check

# Protected routes
@app.get("/dashboard")
async def dashboard(current_user = Depends(get_current_user)):
    """Dashboard accessible to authenticated users only."""
    return {"message": f"Welcome {current_user['name']}"}

@app.post("/approve")
async def approve_action(
    diagnosis_id: str,
    current_user = Depends(require_permission("approve_l1"))
):
    """Approval action requires specific permission."""
    # ... approval logic
    return {"status": "approved", "approver": current_user["email"]}
```

### Environment Variables

```bash
# .env (development)
AZURE_AD_CLIENT_ID="<application-id>"
AZURE_AD_CLIENT_SECRET="<from-azure-portal>"
AZURE_AD_TENANT_ID="<isagri-tenant-id>"
AZURE_AD_AUTHORITY="https://login.microsoftonline.com"

# Or use AWS Secrets Manager in production
aws secretsmanager create-secret \
  --name openclaw/azure-ad-config \
  --secret-string '{
    "client_id": "...",
    "client_secret": "...",
    "tenant_id": "..."
  }'
```

---

## Part 5: Login Flow

### User Login Process

```
1. User visits https://openclaw.isagri.internal/
2. Middleware detects no valid token
3. Redirects to Azure AD login
   → https://login.microsoftonline.com/common/oauth2/v2.0/authorize?...
4. User enters Isagri credentials
5. Azure AD redirects back to:
   → https://openclaw.isagri.internal/auth/callback?code=...
6. Backend exchanges code for JWT token
7. Token stored in secure cookie (HttpOnly, Secure flags)
8. User redirected to dashboard
9. Token automatically included in subsequent requests
```

### Implementation

```python
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode

@app.get("/login")
async def login():
    """Initiate Azure AD login."""
    auth_url = aad_auth.get_authorization_url(
        scopes=["https://graph.microsoft.com/.default"],
        redirect_uri="https://openclaw.isagri.internal/auth/callback"
    )
    return RedirectResponse(url=auth_url)

@app.get("/auth/callback")
async def auth_callback(code: str):
    """Handle Azure AD callback."""
    try:
        token = await aad_auth.get_token_from_code(code)
        
        # Store token in secure cookie
        response = RedirectResponse(url="/dashboard")
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,  # HTTPS only
            samesite="Strict"
        )
        return response
        
    except Exception as e:
        logger.error(f"Auth callback failed: {e}")
        raise HTTPException(status_code=400, detail="Authentication failed")

@app.get("/logout")
async def logout():
    """Clear authentication."""
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
```

---

## Part 6: Testing Authentication

### Manual Test

```bash
# Test login flow
1. Navigate to: https://openclaw.isagri.internal/login
2. Enter Isagri credentials
3. Should redirect to dashboard after successful auth
4. Verify user info displayed (name, email, groups)
```

### Automated Test

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_login_redirect(client):
    """Test login initiates Azure AD redirect."""
    response = client.get("/login")
    assert response.status_code == 307
    assert "login.microsoftonline.com" in response.headers["location"]

def test_unauthorized_access(client):
    """Test unauthenticated access denied."""
    response = client.get("/dashboard")
    assert response.status_code == 307  # Redirect to login
    assert "/login" in response.headers["location"]

def test_authenticated_access(client, mock_jwt_token):
    """Test authenticated dashboard access."""
    response = client.get(
        "/dashboard",
        cookies={"access_token": mock_jwt_token}
    )
    assert response.status_code == 200
    assert "Welcome" in response.text

def test_permission_denied(client, viewer_token):
    """Test insufficient permissions."""
    response = client.post(
        "/approve",
        json={"diagnosis_id": "123"},
        cookies={"access_token": viewer_token}
    )
    assert response.status_code == 403
```

---

## Part 7: Security Hardening

### Token Security

- ✅ Tokens stored in **HttpOnly cookies** (not localStorage)
- ✅ **Secure flag** set (HTTPS only)
- ✅ **SameSite=Strict** prevents CSRF
- ✅ Token expiry: **1 hour** (short-lived)
- ✅ Refresh token rotation: **7 days**

### Session Management

```python
# Maximum session duration: 8 hours
MAX_SESSION_DURATION = 8 * 3600

@app.middleware("http")
async def enforce_session_timeout(request, call_next):
    """Enforce max session duration."""
    token = request.cookies.get("access_token")
    
    if token:
        user = get_current_user(token)
        issued_at = user.get("iat", 0)
        
        if time.time() - issued_at > MAX_SESSION_DURATION:
            response = RedirectResponse(url="/login")
            response.delete_cookie("access_token")
            return response
    
    return await call_next(request)
```

### Audit Logging

```python
@app.middleware("http")
async def log_access(request, call_next):
    """Log all authenticated access."""
    token = request.cookies.get("access_token")
    user = get_current_user(token) if token else None
    
    response = await call_next(request)
    
    audit.log("API_ACCESS", {
        "user": user.get("email") if user else "anonymous",
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "timestamp": datetime.now()
    })
    
    return response
```

---

## Part 8: Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "Invalid client_id" | Wrong Azure AD client ID | Verify in Azure Portal |
| "Redirect URI mismatch" | URI doesn't match registered | Update in Azure Portal |
| "User not in group" | User not added to Azure AD group | Add to openclaw-dashboardusers group |
| "Token expired" | Session > 1 hour | User must re-login |
| CORS errors | Frontend on different origin | Configure CORS middleware |

---

## Deployment Checklist

- [ ] Azure AD application registered
- [ ] Client secret created and stored in Secrets Manager
- [ ] API permissions granted (Microsoft Graph)
- [ ] Azure AD groups created (admin, engineers, viewers)
- [ ] Users added to groups
- [ ] FastAPI middleware implemented
- [ ] Login/logout endpoints working
- [ ] RBAC tested with different roles
- [ ] Session timeout configured
- [ ] HTTPS enforced
- [ ] Audit logging enabled
- [ ] Security review completed

---

## References

- [Azure AD Authentication with FastAPI](https://github.com/starlite-api/starlite/blob/main/docs/advanced/security.md)
- [Microsoft Identity Platform](https://docs.microsoft.com/en-us/azure/active-directory/develop/)
- [Azure AD Groups and Roles](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/groups-overview)
- [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)

---

**Status**: Ready for implementation  
**Blocker Resolved**: Q5 ✅  
**Owner**: Security + DevOps team  
**Timeline**: S1-S3 (MVP setup phase)

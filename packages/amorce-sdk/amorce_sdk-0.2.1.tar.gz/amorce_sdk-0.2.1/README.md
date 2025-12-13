# Amorce Python SDK

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)

**The Standard for Secure AI Agent Transactions**

Protect your AI Agent's API with cryptographic verification. The Amorce SDK handles Ed25519 signatures, zero-trust identity, and transaction validation—so you can focus on building.

---

## 🚀 Quick Start

### Installation

```bash
pip install amorce-sdk
```

### Identity Setup

Every AI Agent needs an identity (Ed25519 keypair):

```python
from amorce import IdentityManager

# Generate a new identity (ephemeral for dev/testing)
identity = IdentityManager.generate_ephemeral()

print(f"Agent ID: {identity.agent_id}")
print(f"Public Key:\\n{identity.public_key_pem}")
```

**📝 For Production:** Save your identity securely

```python
# Save for reuse
with open("my_agent_key.pem", "w") as f:
    f.write(identity.private_key_pem)

# Load next time
from amorce import LocalFileProvider
identity = IdentityManager(LocalFileProvider("my_agent_key.pem"))
```

---

## 🛡️ For Builders: Protect Your API

**Are you building an AI Agent?** Use the SDK to verify incoming requests on your server.

### Why This Matters

- ✅ **Cryptographic proof** of sender identity (Ed25519 signatures)
- ✅ **Zero-trust by default** - every request is verified
- ✅ **Intent whitelisting** - only allow specific actions  
- ✅ **Automatic key revocation** - invalid agents rejected instantly
- ✅ **No maintenance burden** - public keys auto-fetched from Trust Directory

### How to Verify Requests

```python
from amorce import verify_request, AmorceSecurityError
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/v1/webhook', methods=['POST'])
def handle_incoming():
    try:
        # ✅ AUTOMATIC VERIFICATION
        # SDK fetches public key from Trust Directory and verifies signature
        verified = verify_request(
            headers=request.headers,
            body=request.get_data(),
            allowed_intents=['book_table', 'check_availability', 'cancel']
        )
        
        print(f"✅ Verified request from: {verified.agent_id}")
        print(f"Intent: {verified.payload['payload']['intent']}")
        
        # Your business logic here - 100% sure it's legitimate
        if verified.payload['payload']['intent'] == 'book_table':
            return {"status": "confirmed", "table": "A5", "time": "19:00"}
        
    except AmorceSecurityError as e:
        # Invalid signature, unknown agent, or unauthorized intent
        print(f"❌ Rejected: {e}")
        return {"error": "Unauthorized"}, 401
```

**That's it!** Your API is now protected by cryptographic verification.

### Advanced: Manual Public Key (Offline/Testing)

For testing or private networks, you can skip the Trust Directory lookup:

```python
# Provide public key directly (no network call)
verified = verify_request(
    headers=request.headers,
    body=request.get_data(),
    public_key="-----BEGIN PUBLIC KEY-----\\n...\\n-----END PUBLIC KEY-----"
)
```

---

## 📋 Register Your Agent (Optional)

Want to list your service in the Amorce Network? Generate your manifest:

```python
identity = IdentityManager.generate_ephemeral()

# 🖨️  Generate manifest JSON
manifest = identity.to_manifest_json(
    name="My Restaurant Bot",
    endpoint="https://my-api.example.com/api/v1/webhook",
    capabilities=["book_table", "check_availability", "cancel_reservation"],
    description="Fine dining reservations with real-time availability"
)

# Save it
with open("agent-manifest.json", "w") as f:
    f.write(manifest)

print("✅ Manifest created! Submit it to the Trust Directory to get listed.")
```

**What you get:**
- 🌐 Discoverable by other agents in the network
- 🔐 Your public key automatically distributed
- 📊 Trust score based on transaction history

---

## 📤 Sending Transactions (For Clients/Testing)

Need to call another agent? The SDK makes it simple:

```python
from amorce import AmorceClient, IdentityManager

# Setup identity
identity = IdentityManager.generate_ephemeral()

# Initialize client (zero-config - uses production mainnet)
client = AmorceClient(identity=identity)

# Send a transaction
response = client.transact(
    service_contract={"service_id": "srv_restaurant_123"},
    payload={
        "intent": "book_table",
        "params": {"date": "2025-12-01", "guests": 4, "time": "19:00"}
    }
)

if response.get("status") == "success":
    print(f"✅ Booking confirmed: {response['data']}")
```

### Custom Endpoints (Development/Testing)

```python
client = AmorceClient(
    identity=identity,
    directory_url="http://localhost:8080",
    orchestrator_url="http://localhost:8081"
)
```

---

## ⚡ Async Support (NEW in v0.2.0)

For high-performance applications:

```python
from amorce import AsyncAmorceClient

async with AsyncAmorceClient(identity=identity) as client:
    response = await client.transact(
        service_contract={"service_id": "srv_restaurant_123"},
        payload={"intent": "book_table", "params": {...}}
    )
```

**Features:**
- HTTP/2 multiplexing
- Exponential backoff + jitter
- Auto-generated idempotency keys
- 3x faster for concurrent requests

---

## 🤝 Human-in-the-Loop (HITL) Support

Enable human oversight for critical agent decisions with built-in approval workflows.

### When to Use HITL

- **High-value transactions** - Booking reservations, making purchases
- **Data sharing** - Before sending personal information to third parties
- **Irreversible actions** - Cancellations, deletions, confirmations
- **Regulatory compliance** - Finance, healthcare, legal industries

### Basic HITL Workflow

```python
from amorce import AmorceClient, IdentityManager

identity = IdentityManager.generate_ephemeral()
client = AmorceClient(identity=identity)

# 1. Agent negotiates with service
response = client.transact(
    service_contract={"service_id": "srv_restaurant_123"},
    payload={"intent": "book_table", "guests": 4, "date": "2025-12-05"}
)

# 2. Request human approval before finalizing
approval_id = client.request_approval(
    transaction_id=response['transaction_id'],
    summary=f"Book table for 4 guests at {response['restaurant']['name']}",
    details=response['result'],
    timeout_seconds=300  # 5 minute timeout
)

print(f"Awaiting approval: {approval_id}")

# 3. Human reviews and approves (via SMS, email, app, etc.)
# ... your notification logic here ...

# 4. Check approval status
status = client.check_approval(approval_id)
if status['status'] == 'approved':
    # 5. Finalize the transaction
    final_response = client.transact(
        service_contract={"service_id": "srv_restaurant_123"},
        payload={"intent": "confirm_booking", "booking_id": response['booking_id']}
    )
    print("✅ Booking confirmed!")
```

### Submitting Approval Decisions

Your application collects human input and submits the decision:

```python
# Human approved via your UI/SMS/voice interface
client.submit_approval(
    approval_id=approval_id,
    decision="approve",  # or "reject"
    approved_by="user@example.com",
    comments="Looks good for the business lunch"
)
```

### LLM-Interpreted Approvals

Use AI to interpret natural language responses:

```python
import google.generativeai as genai

# Human responds: "yes sounds perfect"
human_response = "yes sounds perfect"

# LLM interprets the intent
interpretation = genai.GenerativeModel('gemini-pro').generate_content(
    f'Is this approving or rejecting? "{human_response}" Answer: APPROVE or REJECT'
).text

decision = "approve" if "APPROVE" in interpretation.upper() else "reject"

client.submit_approval(
    approval_id=approval_id,
    decision=decision,
    approved_by="user@example.com",
    comments=f"Original response: {human_response}"
)
```

### Channel-Agnostic Notifications

HITL is **protocol-level** - you choose how to notify humans:

- **SMS** (Twilio): "Sarah wants to book Le Petit Bistro for 4. Reply YES/NO"
- **Email**: Send approval link with one-click approve/reject
- **Voice** (Vapi.ai): "Your assistant needs approval. Say approve or decline"
- **Push notification**: Mobile app notification
- **Slack/Teams**: Bot message with buttons

**Example with Twilio:**
```python
from twilio.rest import Client

# Create approval
approval_id = client.request_approval(...)

# Send SMS
twilio = Client(account_sid, auth_token)
twilio.messages.create(
    to="+1234567890",
    from_="+0987654321",
    body=f"Sarah needs approval: Book table for 4 at Le Petit Bistro tomorrow 7pm. Reply YES or NO"
)

# Poll for response or use webhook
# When you receive "YES", submit approval
client.submit_approval(approval_id, decision="approve", approved_by="sms:+1234567890")
```

### Advanced: Approval Timeouts

Approvals automatically expire after the timeout period:

```python
approval_id = client.request_approval(
    transaction_id=tx_id,
    summary="High-value purchase: $5,000",
    timeout_seconds=600  # 10 minutes
)

# Later...
status = client.check_approval(approval_id)
if status['status'] == 'expired':
    print("⏱️ Approval request timed out - transaction cancelled")
```

### Best Practices

1. **Clear summaries** - Make approval requests easy to understand
2. **Appropriate timeouts** - Balance urgency vs. convenience
3. **Audit trail** - All approvals are logged with timestamps and user IDs
4. **Fallback handling** - Handle expired/rejected approvals gracefully
5. **Security** - Verify human identity before submitting approvals


## 🔒 Security Architecture

```
┌─────────────┐                  ┌──────────────────┐                  ┌─────────────┐
│   Client    │                  │  Orchestrator    │                  │   Service   │
│   Agent     │                  │  (Amorce)        │                  │   Provider  │
└─────────────┘                  └──────────────────┘                  └─────────────┘
       │                                  │                                    │
       │ 1. Sign request                  │                                    │
       │    (Ed25519)                     │                                    │
       ├─────────────────────────────────>│                                    │
       │                                  │ 2. Verify signature                │
       │                                  │    (fetch public key from          │
       │                                  │     Trust Directory)               │
       │                                  ├───────────────────────────────────>│
       │                                  │ 3. Forward verified request        │
       │                                  │    (with sender identity)          │
       │                                  │                                    │
       │                                  │ 4. Service verifies again          │
       │                                  │    (optional double-check)         │
       │                                  │<───────────────────────────────────│
       │<─────────────────────────────────│ 5. Return signed response          │
       │                                  │                                    │
```

**Zero-Trust Principles:**
1. Every request is signed by sender
2. Every signature is verified before processing
3. Public keys are immutable (tied to agent_id)
4. Revoked agents are immediately rejected

---

## 📚 API Reference

### `IdentityManager`

**Factory Methods:**
- `generate_ephemeral()` - Create new Ed25519 identity (in-memory)
- `IdentityManager(provider)` - Load from file/env/secret manager

**Properties:**
- `agent_id` - SHA-256 hash of public key (deterministic)
- `public_key_pem` - Public key in PEM format
- `private_key_pem` - Private key in PEM format (⚠️ handle carefully)

**Methods:**
- `sign_data(bytes)` - Sign raw bytes, return base64 signature
- `to_manifest_json(...)` - Generate agent manifest for registration
- `verify_signature(public_key, data, signature)` - Static verification method

### `verify_request()`

**For Builders** - Verify incoming signed requests

```python
verify_request(
    headers: Dict[str, str],
    body: bytes,
    allowed_intents: Optional[List[str]] = None,
    public_key: Optional[str] = None,
    directory_url: str = "https://directory.amorce.io"
) -> VerifiedRequest
```

**Returns:** `VerifiedRequest` with `.agent_id`, `.payload`, `.signature`  
**Raises:** `AmorceSecurityError` if verification fails

### `AmorceClient`

**Constructor:**
```python
AmorceClient(
    identity: IdentityManager,
    directory_url: str = "https://directory.amorce.io",    # Zero-config!
    orchestrator_url: str = "https://orchestrator.amorce.io",
    agent_id: Optional[str] = None,
    api_key: Optional[str] = None
)
```

**Methods:**
- `discover(service_type)` - Find services in Trust Directory
- `transact(service_contract, payload, priority)` - Execute transaction
- `request_approval(transaction_id, summary, details, timeout_seconds)` - Create HITL approval request
- `check_approval(approval_id)` - Get approval status
- `submit_approval(approval_id, decision, approved_by, comments)` - Submit approval decision

### Exceptions

- `AmorceError` - Base exception
- `AmorceConfigError` - Invalid configuration
- `AmorceNetworkError` - Network/connection errors
- `AmorceAPIError` - API errors (4xx, 5xx)
- `AmorceSecurityError` - Signature/verification failures ⚠️
- `AmorceValidationError` - Data validation errors

---

## 🛠️ Development

```bash
# Clone and install
git clone https://github.com/trebortGolin/amorce_py_sdk.git
cd amorce_py_sdk
pip install -e ".[dev]"

# Run tests
pytest --cov=amorce

# Type checking
mypy amorce/
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🔗 Related Projects

- [amorce-js-sdk](https://github.com/trebortGolin/amorce-js-sdk) - JavaScript/TypeScript SDK
- [amorce-trust-directory](https://github.com/trebortGolin/amorce-trust-directory) - Trust Directory service
- [amorce-console](https://github.com/trebortGolin/amorce-console) - Management console

---

## 📝 Changelog

### v0.2.1 (2025-11-30) 🆕
* **[NEW - FOR BUILDERS]** `verify_request()` - Verify incoming signed requests
* **[NEW]** `to_manifest_json()` - Generate agent manifest for registration
* **[ENHANCEMENT]** Zero-config defaults (production mainnet URLs)
* **[DOCS]** Restructured README for Builders-first messaging

### v0.2.0 (2025-11-30)
* **[FEATURE]** `AsyncAmorceClient` with HTTP/2 support
* **[FEATURE]** Exponential backoff + jitter retry logic
* **[FEATURE]** Auto-generated idempotency keys
* **[FEATURE]** Structured `AmorceResponse` model
* **[BREAKING]** Requires `httpx` and `tenacity` dependencies

### v0.1.7
* Initial stable release
* Ed25519 signature support
* Trust Directory integration
* Sync `AmorceClient`

---

**Built with ❤️ for the Agent Economy**
---

## 🔌 MCP Integration - Production Ready ✅

**Use Model Context Protocol tools through Amorce with cryptographic security and human oversight.**

The Amorce SDK provides production-ready integration with [Model Context Protocol](https://modelcontextprotocol.io) servers, adding Ed25519 signatures and human-in-the-loop approvals to all tool calls.

### 🚀 Quick Start

```python
from amorce import IdentityManager, MCPToolClient

# 1. Create your agent identity
identity = IdentityManager.generate_ephemeral()

# 2. Connect to MCP wrapper
mcp = MCPToolClient(identity, wrapper_url="http://localhost:5001")

# 3. Discover available tools
tools = mcp.list_tools()
for tool in tools:
    hitl = "🔒" if tool.requires_approval else "✓"
    print(f"{hitl} {tool.name}: {tool.description}")

# 4. Call tools (read operations)
result = mcp.call_tool('filesystem', 'read_file', {'path': '/tmp/data.txt'})
print(result)

# 5. Call tools requiring approval (write operations)
try:
    mcp.call_tool('filesystem', 'write_file', {
        'path': '/tmp/output.txt',
        'content': 'Hello from Amorce!'
    })
except ValueError as e:
    print("Approval required!")  
    # Request approval through orchestrator
    approval_id = request_approval(...)  
    result = mcp.call_tool('filesystem', 'write_file', {...}, approval_id=approval_id)
```

### ✅ Production Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Cryptographic Signatures** | ✅ Production | Ed25519 on every request |
| **HITL Approvals** | ✅ Production | Required for write/delete/move |
| **Rate Limiting** | ✅ Production | 20 req/min, configurable |
| **Load Tested** | ✅ Verified | 50 concurrent, 5ms avg response |
| **Error Handling** | ✅ Comprehensive | Timeouts, connection errors, validation |
| **Trust Directory** | ✅ 95% Ready | Public key distribution |

### 📖 Complete Example with HITL

```python
from amorce import IdentityManager, MCPToolClient, AmorceClient

# Setup
identity = IdentityManager.generate_ephemeral()
mcp = MCPToolClient(identity, "http://localhost:5001")
client = AmorceClient(identity, orchestrator_url="http://localhost:8080")

# List tools and check HITL requirements
tools = mcp.list_tools()
write_tool = next(t for t in tools if t.name == 'write_file')
print(f"Write file requires approval: {write_tool.requires_approval}")  # True

# Attempt without approval (will fail)
try:
    result = mcp.call_tool('filesystem', 'write_file', {
        'path': '/tmp/important.txt',
        'content': 'Critical data'
    })
except ValueError as e:
    print(f"Blocked: {e}")  # "Tool requires approval"
    
# Request approval
approval = client.request_approval(
    tool_name='write_file',
    tool_args={'path': '/tmp/important.txt', 'content': 'Critical data'},
    reason='Writing ML model output'
)

# Human reviews and approves (via UI or API)
# ... approval.approve() ...

# Execute with approval
result = mcp.call_tool('filesystem', 'write_file', {
    'path': '/tmp/important.txt',
    'content': 'Critical data'
}, approval_id=approval.id)

print(f"File written successfully: {result}")
```

### 🎯 Tool Categories

| Category | Examples | HITL Required |
|----------|----------|---------------|
| **Read Operations** | read_file, list_directory, search | ❌ No |
| **Write Operations** | write_file, edit_file | ✅ Yes |
| **Destructive Operations** | delete_file, move_file | ✅ Yes |
| **Search/Query** | brave_search, database_query | ❌ No (read-only) |

### 📈 Performance

**Production-Tested Metrics:**
- **Response Time:** 3-9ms average
- **Concurrent:** 50 requests in 40ms
- **Rate Limit:** 20 req/min (enforced)
- **Uptime:** 100% under load testing

### 🔗 Available MCP Servers

Access 80+ production MCP servers through Amorce:

```python
# Filesystem operations
mcp.call_tool('filesystem', 'read_file', {'path': '/data/input.json'})

# Web search
mcp.call_tool('search', 'brave_search', {'query': 'AI agents 2024'})

# Database access (with HITL)
mcp.call_tool('postgres', 'execute_query', {'sql': 'SELECT * FROM users'}, approval_id)

# Git operations (with HITL)
mcp.call_tool('git', 'commit', {'message': 'Update config'}, approval_id)
```

[View all 80+ MCP servers →](https://github.com/modelcontextprotocol/servers)

### 📚 Additional Resources

- **[MCP Wrapper Docs](https://github.com/trebortGolin/amorce/blob/main/docs/MCP_WRAPPER.md)** - Complete integration guide
- **[Console Integration](https://amorce.io/docs/guides/mcp-integration)** - UI for approval management
- **[Test Results](https://github.com/trebortGolin/amorce/blob/main/tests/TEST_RESULTS.md)** - Production readiness evidence

---

# rotagent

A Python library for secure agent-orchestrator communication using JWT-based authentication with RSA keypairs.

## Features

- 🔐 **AgentAuth**: Flask decorator for securing agent endpoints with JWT verification
- 📡 **OrchestratorClient**: Async client for sending signed requests to agents
- 🔑 **KeyManager**: RSA keypair generation and public key loading
- 🛠️ **DevTools**: Development utilities for key setup and token generation

## Installation

```bash
pip install rotagent
```

## Quick Start

### Agent Side (Flask Application)

```python
from flask import Flask, request, jsonify
from rotagent import AgentAuth

app = Flask(__name__)
auth = AgentAuth(keys_dir="./authorized_keys")

@app.route("/agent", methods=["POST"])
@auth.require_auth
def agent_endpoint():
    data = request.get_json()
    # Your agent logic here
    return jsonify({"response": "Hello from agent!"})
```

### Orchestrator Side

```python
import aiohttp
from rotagent import OrchestratorClient

async def call_agent():
    async with aiohttp.ClientSession() as session:
        response = await OrchestratorClient.send_secure_request(
            session=session,
            url="http://agent-url.com",
            payload={"query": "What movies are playing?"},
            issuer_id="my_orchestrator",
            private_key_pem=private_key_pem  # Your RSA private key
        )
        return response
```

### Development Setup

Generate development keys for testing:

```python
from rotagent import DevTools

# Generate keys - saves public key to disk, prints private key for .env
DevTools.setup_persistent_keys(keys_dir="authorized_keys", issuer_id="dev_postman")

# Generate a test token for Postman/curl testing
token, body = DevTools.generate_bearer_token(query="test query")
```

## Environment Variables

- `APP_ENV`: Set to `development` to disable security checks (replay protection, body hash verification)

## Security Features

- **JWT-based authentication** with RS256 signing
- **Replay attack protection** with JTI (JWT ID) tracking
- **Body tampering detection** via SHA256 content hashing
- **Hot-reload** of public keys (no restart needed when adding new orchestrators)

## License

MIT License

import sys, json
from client import JWTHmacSha256AttestationValidator

val = JWTHmacSha256AttestationValidator()

def handle_jsonrpc(line):
    global val
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-jwt-hmac-sha256-token-attestation-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "create_jwt", "description": "Create signed JWT token.", "inputSchema": {"type": "object", "properties": {"payload": {"type": "object"}, "secret": {"type": "string"}}, "required": ["payload", "secret"]}},
                {"name": "verify_jwt", "description": "Verify token signature and exp.", "inputSchema": {"type": "object", "properties": {"token": {"type": "string"}, "secret": {"type": "string"}}, "required": ["token", "secret"]}},
                {"name": "benchmark_jwt_attestation", "description": "Run standard JWT benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "create_jwt":
                tok = val.create_token(args.get("payload", {}), args.get("secret"))
                res = {"token": tok}
            elif tool == "verify_jwt":
                res = val.verify_token(args.get("token"), args.get("secret"))
            elif tool == "benchmark_jwt_attestation":
                res = val.benchmark_jwt_attestation()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()

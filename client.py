import hmac, hashlib, base64, json, time
from typing import Dict, Any

class JWTHmacSha256AttestationValidator:
    @staticmethod
    def _b64url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')

    @classmethod
    def create_token(cls, payload: Dict[str, Any], secret: str) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        h_str = cls._b64url_encode(json.dumps(header).encode('utf-8'))
        p_str = cls._b64url_encode(json.dumps(payload).encode('utf-8'))
        signing_input = f"{h_str}.{p_str}"
        sig = hmac.new(secret.encode('utf-8'), signing_input.encode('utf-8'), hashlib.sha256).digest()
        s_str = cls._b64url_encode(sig)
        return f"{signing_input}.{s_str}"

    @classmethod
    def verify_token(cls, token: str, secret: str) -> Dict[str, Any]:
        parts = token.split('.')
        if len(parts) != 3:
            return {"valid": False, "error": "Invalid format"}
        h_str, p_str, s_str = parts
        signing_input = f"{h_str}.{p_str}"
        expected_sig = cls._b64url_encode(hmac.new(secret.encode('utf-8'), signing_input.encode('utf-8'), hashlib.sha256).digest())
        if not hmac.compare_digest(expected_sig, s_str):
            return {"valid": False, "error": "Signature mismatch"}
        padded = p_str + '=' * (4 - len(p_str) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded.encode('ascii')).decode('utf-8'))
        exp = payload.get("exp")
        if exp and exp < time.time():
            return {"valid": False, "error": "Token expired"}
        return {"valid": True, "payload": payload}

    def benchmark_jwt_attestation(self) -> Dict[str, Any]:
        secret = "agent_sec_2026"
        token = self.create_token({"sub": "agent_worker_42", "role": "executor", "exp": time.time() + 3600}, secret)
        ver = self.verify_token(token, secret)
        return {"token_sample": token[:30] + "...", "verified": ver["valid"], "sub": ver["payload"]["sub"]}

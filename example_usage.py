from client import JWTHmacSha256AttestationValidator

def run_example():
    print("=== GenPark JWT HMAC-SHA256 Validator Example ===")
    validator = JWTHmacSha256AttestationValidator()
    print("Benchmark Result:", validator.benchmark_jwt_attestation())

if __name__ == "__main__":
    run_example()

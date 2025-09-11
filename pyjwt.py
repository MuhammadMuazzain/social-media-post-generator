import jwt
import datetime
import sys

def decode_jwt(token: str, secret: str = None):
    try:
        # Always decode header (just base64 JSON)
        header = jwt.get_unverified_header(token)
        print("===== HEADER =====")
        print(header)

        # Decode payload (without signature check first)
        payload = jwt.decode(token, options={"verify_signature": False})
        print("\n===== PAYLOAD =====")
        print(payload)

        # Check expiry if present
        if "exp" in payload:
            exp_time = datetime.datetime.fromtimestamp(payload["exp"])
            print(f"\n[+] Expiration Time: {exp_time} (UTC)")
            if exp_time < datetime.datetime.utcnow():
                print("[-] Token is EXPIRED ❌")
            else:
                print("[+] Token is still valid ✅")

        if "iat" in payload:
            iat_time = datetime.datetime.fromtimestamp(payload["iat"])
            print(f"[+] Issued At: {iat_time} (UTC)")

        if "nbf" in payload:
            nbf_time = datetime.datetime.fromtimestamp(payload["nbf"])
            print(f"[+] Not Valid Before: {nbf_time} (UTC)")

        # Verify signature if secret provided
        if secret:
            try:
                verified = jwt.decode(token, secret, algorithms=[header.get("alg", "HS256")])
                print("\n[+] Signature verified successfully ✅")
                print("Verified Payload:", verified)
            except jwt.InvalidSignatureError:
                print("\n[-] Invalid Signature ❌")
            except Exception as e:
                print(f"\n[-] Verification failed: {e}")

    except Exception as e:
        print(f"Error decoding JWT: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_jwt.py <JWT_TOKEN> [SECRET]")
        sys.exit(1)

    token = sys.argv[1]
    secret = sys.argv[2] if len(sys.argv) > 2 else None

    decode_jwt(token, secret)

# cython: language_level=3
import json
import base64
import time
import os

_CRYPTO_AVAILABLE = True
try:
    # Do not import cryptography at module import time to keep the package lightweight
    # unless the licensing APIs are actually used. We'll import lazily inside functions.
    import cryptography  # noqa: F401
except Exception:
    _CRYPTO_AVAILABLE = False

# Embedded Public Key (Ed25519)
# This is hardcoded so the public key is available at import time.
# Using a plain Python bytes literal avoids Cython-only syntax so the module
# can be imported in regular Python environments for checks.
PUBLIC_KEY_BYTES = bytes([
    0x79, 0xfa, 0x38, 0x49, 0x75, 0xbe, 0xe8, 0xc1, 0xc3, 0x7c, 0x59, 0x90,
    0x7c, 0xb5, 0x03, 0x00, 0x93, 0x9f, 0xca, 0x39, 0x68, 0x16, 0x79, 0xb1,
    0x5d, 0x4a, 0x61, 0xd4, 0x28, 0x45, 0xc6, 0x5e
])


def get_public_key():
    """Reconstructs the public key object from embedded bytes."""
    if not _CRYPTO_AVAILABLE:
        raise ImportError(
            "The 'cryptography' package is required to use genuity licensing functions. "
            "Install it with 'pip install cryptography' or enable it in your environment."
        )
    from cryptography.hazmat.primitives.asymmetric import ed25519

    return ed25519.Ed25519PublicKey.from_public_bytes(PUBLIC_KEY_BYTES[:32])

def verify_license(license_key: str):
    """
    Verifies the license key.
    Returns the payload dict if valid, raises ValueError if invalid.
    """
    if not license_key or not isinstance(license_key, str):
        raise ValueError("License key must be a non-empty string")
    
    try:
        # Clean the license key - remove any whitespace and ensure it's a string
        license_key = str(license_key).strip()
        if not license_key:
            raise ValueError("License key cannot be empty")
        
        parts = license_key.split(".")

        # Support two common formats:
        # 1) JWT-like: payload.signature (two base64url parts separated by a dot)
        # 2) Single base64-encoded JSON: b64encode(json{"payload": "...", "signature": "..."})
        if len(parts) == 2:
            b64_payload, b64_sig = parts
            # Add padding if needed
            b64_payload += "=" * (-len(b64_payload) % 4)
            b64_sig += "=" * (-len(b64_sig) % 4)
            try:
                payload_bytes = base64.urlsafe_b64decode(b64_payload)
                signature_bytes = base64.urlsafe_b64decode(b64_sig)
            except Exception as e:
                raise ValueError(f"Invalid base64 encoding in license key: {e}")
        else:
            # Try decode whole string as base64 JSON wrapper
            s = license_key.strip()
            s += "=" * (-len(s) % 4)
            try:
                decoded = base64.urlsafe_b64decode(s)
                try:
                    obj = json.loads(decoded.decode("utf-8"))
                except UnicodeDecodeError as e:
                    raise ValueError(f"License key contains invalid UTF-8 data. Please check that you copied the license key correctly: {e}")
                # Expect keys 'payload' and 'signature'
                if not isinstance(obj, dict) or 'payload' not in obj or 'signature' not in obj:
                    raise ValueError("Unsupported single-part license format; expected JSON with 'payload' and 'signature'")
                b64_payload = obj['payload']
                b64_sig = obj['signature']
                b64_payload += "=" * (-len(b64_payload) % 4)
                b64_sig += "=" * (-len(b64_sig) % 4)
                try:
                    payload_bytes = base64.urlsafe_b64decode(b64_payload)
                    signature_bytes = base64.urlsafe_b64decode(b64_sig)
                except Exception as e:
                    raise ValueError(f"Invalid base64 encoding in wrapped license format: {e}")
            except ValueError:
                # Re-raise ValueError as-is
                raise
            except Exception as e:
                raise ValueError(f"Invalid license format. Expected two-part format (payload.signature) or valid base64 JSON wrapper: {e}")
        
        # Verify signature
        try:
            public_key = get_public_key()
            public_key.verify(signature_bytes, payload_bytes)
        except Exception as e:
            raise ValueError(f"License signature verification failed. The license key may be invalid or corrupted: {e}")
        
        # Parse payload
        try:
            payload = json.loads(payload_bytes.decode("utf-8"))
        except UnicodeDecodeError as e:
            raise ValueError(f"License payload contains invalid UTF-8 data: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"License payload is not valid JSON: {e}")
        
        # Check expiry
        if payload.get("exp", 0) < time.time():
            raise ValueError("License expired")
            
        return payload
        
    except ValueError:
        # Re-raise ValueError as-is (already has good error message)
        raise
    except Exception as e:
        raise ValueError(f"License verification failed: {e}")

def activate(license_key: str):
    """
    Verifies the license and stores only a salted hash of the payload for validation caching (for offline mode).
    Call this as genuity.activate('PASTE_LICENSE')
    """
    payload = verify_license(license_key)
    import hashlib
    import json
    salt = 'GENUITY_SALT_v1'  # static salt for example/demo purposes
    payload_hash = hashlib.sha256((json.dumps(payload, sort_keys=True)+salt).encode('utf-8')).hexdigest()
    home = os.path.expanduser("~")
    cache_dir = os.path.join(home, ".genuity")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, "cache")
    expires_at = payload.get("expires_at") or payload.get("exp")
    cache_content = {
        "payload_hash": payload_hash,
        "expires_at": expires_at
    }
    with open(cache_path, "w") as f:
        f.write(json.dumps(cache_content))
    return payload

def check_cache():
    """
    Check if the local activation cache is present and not expired. Returns True if active.
    """
    import json, os, time
    home = os.path.expanduser("~")
    cache_path = os.path.join(home, ".genuity", "cache")
    try:
        with open(cache_path, "r") as f:
            cache = json.load(f)
        if int(cache["expires_at"]) > time.time():
            return True
    except Exception:
        pass
    return False


# Compatibility aliases expected by older imports
activate_license = activate
check_activation = check_cache

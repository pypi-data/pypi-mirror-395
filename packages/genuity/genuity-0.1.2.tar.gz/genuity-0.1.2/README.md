# Genuity: Offline License Activation

## Installation

```bash
pip install genuity
```

## Activation & Usage
After purchasing, you’ll receive a license string:

```
import genuity
genuity.activate('PASTE_LICENSE_STRING')
```

If your system is offline, activation works by validating the license via an embedded public key (NO INTERNET NEEDED).

- License is valid for 7 days, then repeat activation with fresh license.
- No private key is ever shipped or present anywhere but our server.

## Security
- License is cryptographically signed (Ed25519), verified offline.
- Only hardened/compiled Cython modules are shipped. No source code is exposed in the package.

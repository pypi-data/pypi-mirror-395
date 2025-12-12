# E2EE

End-to-end encryption helper built on elliptic-curve Diffie-Hellman (ECDH), PBKDF2 key derivation, and Fernet symmetric encryption. The `E2EE` class coordinates server/client key exchange, mutual authentication, and message confidentiality.

## Features
- ECDH (SECP521R1) key agreement for both a public key and a salt key-pair
- Server-signed public material to prevent tampering (ECDSA with SHA-224)
- PBKDF2-HMAC-SHA256 derivation of a 256-bit Fernet key from the dual shared secrets
- Simple `encrypt`/`decrypt` helpers that emit URL-safe Base64 strings

## Prerequisites
- Python `>=3.9.10`
- `cryptography` library (pulled automatically via `pyproject.toml`)
- DER-encoded ECDSA key pair available on disk:
   - `PRIVATE_KEY` environment variable -> path to the server signing key (PKCS#8 DER)
   - `PUBLIC_KEY` environment variable -> path to the public key distributed to clients (SubjectPublicKeyInfo DER)

These files are used exactly as in the `tests/conftest.py` fixture.

## Key-Exchange Workflow
1. **Server bootstrap**: instantiate `E2EE()` with no arguments. It becomes the authoritative peer, loading its private signing key and generating ephemeral public key/salt pairs.
2. **Publish public material**: the server exposes `server.public_key` and `server.public_salt`. Each property returns the Base32-encoded point alongside a Base32 signature.
3. **Client bootstrap**: instantiate `E2EE(server.public_key, server.public_salt)` on the client. The client verifies the signatures with the server's public signing key (pointed to by `PUBLIC_KEY`), generates its own ephemeral key material, and sets up symmetric encryption.
4. **Mutual exchange**: the client shares its unsigned public key/salt. The server calls `load_peer_public_key(client.public_key, client.public_salt)` to complete ECDH.
5. **Secure channel**: both peers derive the same Fernet key from the combined secrets and can call `encrypt`/`decrypt` to exchange ciphertexts.

The round-trip mirrors `tests/test_e2ee.py` and can be summarized as:

```python
server = E2EE()
client = E2EE(server.public_key, server.public_salt)
server.load_peer_public_key(client.public_key, client.public_salt)

ciphertext = server.encrypt("hello")
plaintext = client.decrypt(ciphertext)
```

## Quickstart Example

1. **Generate signing keys (dev only):**

```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat

priv = ec.generate_private_key(ec.SECP521R1())
pub = priv.public_key()

open("/tmp/ecdsa_private_key.pem", "wb").write(
      priv.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())
)
open("/tmp/ecdsa_public_key.pem", "wb").write(
      pub.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
)
```

2. **Export the paths:**

```bash
export PRIVATE_KEY=/tmp/ecdsa_private_key.pem
export PUBLIC_KEY=/tmp/ecdsa_public_key.pem
```

3. **Exchange messages:**

```python
from e2ee import E2EE

server = E2EE()
client = E2EE(server.public_key, server.public_salt)
server.load_peer_public_key(client.public_key, client.public_salt)

secret_from_server = server.encrypt("SECRET MESSAGE FROM SERVER!")
print(client.decrypt(secret_from_server))

secret_from_client = client.encrypt("SECRET MESSAGE FROM CLIENT!")
print(server.decrypt(secret_from_client))
```

## API Reference

- `E2EE(public_key=None, public_salt=None)`: Creates a server instance when called with no arguments; otherwise acts as a client that immediately verifies and loads the remote public key material.
- `public_key` / `public_salt`: Base32-encoded strings (plus signatures on the server). Client values do **not** include signatures.
- `load_peer_public_key(public_key, public_salt, exchange=True)`: Imports peer material. For clients, the tuple must include `(encoded_key, signature)` pairs; servers expect plain Base32 strings. When `exchange` is true (default) the instance computes shared secrets and arms Fernet encryption.
- `encrypt(message: str) -> str`: Encrypts UTF-8 strings and returns URL-safe Base64 ciphertext, ideal for transport over JSON/HTTP.
- `decrypt(encoded_ciphertext: str) -> str`: Reverses `encrypt` and returns the original plaintext string.

## Running the Test Suite

```bash
pip install -e .[dev]
pytest
```

The unit test in `tests/test_e2ee.py` performs the full server/client dance, so it serves as an executable example as well as a regression check.
# qcrypto

**Version: 0.5.0**

`qcrypto` is a lightweight Python library that provides simple, Pythonic wrappers around post-quantum cryptography (PQC) using the official `liboqs-python` bindings from the Open Quantum Safe project.

The library exposes unified, minimal interfaces for:

* Post-quantum key encapsulation (KEM)
* Post-quantum digital signatures
* A hybrid PQC + AES-GCM authenticated encryption scheme

`qcrypto` is suitable for learning PQC concepts, prototyping, research, and experimentation with quantum-safe primitives.

---

## Features

### Post-Quantum Key Encapsulation (KEM)

* **Kyber** (Kyber512 / Kyber768 / Kyber1024)
* **Classic McEliece** (all parameter sets exposed by liboqs)
* Public/secret key generation
* Encapsulation → shared secret + ciphertext
* Decapsulation → recover the same shared secret

### Digital Signatures

* **Dilithium** (2, 3, 5)
* **Falcon** (Falcon-512, Falcon-1024)
* **SPHINCS+** (SHA2 and SHAKE variants)
* Unified signature interface:

  * `SignatureScheme` for any liboqs signature algorithm
  * Convenience wrappers: `DilithiumSig`, `FalconSig`, `SphincsSig`

### Hybrid PQC + AES-256-GCM Encryption

* Kyber encapsulates a shared secret
* HKDF-SHA256 derives an AES key
* AES-256-GCM encrypts the message
* Compact single-blob ciphertext format:

```
[1 byte]  version  
[1 byte]  algorithm id  
[2 bytes] Kyber ciphertext length  
[N bytes] Kyber ciphertext  
[12 bytes] AES-GCM nonce  
[M bytes] AES-GCM ciphertext+tag
```

High-level API:

```python
from qcrypto import encrypt, decrypt
```

Legacy API retained:

```python
encrypt_for_recipient()
decrypt_from_sender()
```

### Key Serialization

* `save_public_key()`, `save_private_key()`
* `KyberKEM.load_public_key()`, `KyberKEM.load_private_key()`
* Raw or base64 encoding

---

## Installation

Python 3.8+:

```
pip install qcrypto
```

`liboqs-python` installs automatically.

---

## Examples

All examples are located in the `examples/` directory:

* `kyber_example.py`
* `files_example.py`
* `mceliece_example.py`
* `dilithium_example.py`
* `falcon_example.py`
* `sphincs_example.py`
* `signature_scheme_generic_example.py`
* `hybrid_example.py`
* `list_algorithms.py`

Run an example:

```
python examples/kyber_example.py
```

---

## Implementation Notes

* Uses `liboqs-python`, which bundles optimized C implementations of PQC algorithms.
* AES-256-GCM provided by the `cryptography` package.
* Available algorithms depend on how liboqs was compiled on your platform.
* Hybrid encryption uses HKDF-SHA256 and fresh 96-bit GCM nonces.
* Pure Python library using modern `src/` layout.

---

## Changelog

### v0.5.0 — CLI Tooling & Passphrase-Protected Keys

New Features
------------

• Added a full command-line interface (CLI) installed as `qcrypto`, providing:
    - `qcrypto gen-key`   — Generate Kyber keypairs
    - `qcrypto encrypt`   — Encrypt files using hybrid PQC + AES-GCM
    - `qcrypto decrypt`   — Decrypt files back to plaintext

• Added passphrase-based encryption for private keys using PBKDF2-HMAC-SHA256
  and AES-256-GCM. Private keys can now be saved securely:

      qcrypto gen-key --pass
      qcrypto decrypt --key private.key --pass

• CLI now supports interactive passphrase prompting or inline passphrase input.

• Integrated passphrase logic with existing key serialization mechanisms.

Other Improvements
------------------

• Added `files_example.py` demonstrating end-to-end CLI file encryption.

• Internal refactoring of key loading/saving functions to support encrypted
  and unencrypted key formats transparently.

• Updated README with CLI usage examples and passphrase workflows.

---

### v0.4.0 — File Encryption & Streaming AES-GCM

New Features
------------

• Added `encrypt_file()` and `decrypt_file()` for real file encryption workflows.
• Introduced streaming AES-256-GCM, allowing encryption/decryption of large files
  without loading the entire file into memory.
• File ciphertext format matches the existing `encrypt()` API for full compatibility.

Ciphertext Format
-----------------

```
[1 byte]    version
[1 byte]    algorithm id
[2 bytes]   Kyber ciphertext length
[N bytes]   Kyber ciphertext
[12 bytes]  AES-GCM nonce
[M bytes]   AES-GCM ciphertext + 16-byte GCM tag
```

Other Improvements
------------------

• Added round-trip file encryption tests.
• Updated `__init__.py` to expose file encryption helpers.
• Internal refactoring to support chunked I/O while preserving the
  standardized hybrid ciphertext structure.

---

### v0.3.0 — Expanded PQC Support

**New Algorithms**

* Falcon signatures (`FalconSig`)
* SPHINCS+ signatures (`SphincsSig`)
* Classic McEliece KEM (`ClassicMcElieceKEM`)

**Unified Signature Interface**

* Added `SignatureScheme` supporting any liboqs signature algorithm.

**Examples**

* Added Falcon, SPHINCS+, McEliece, and generic signature examples.

**Internal Improvements**

* Restructured signatures/KEMs for easier future expansion.

---

### v0.2.0 — Hybrid API Rewrite, Ciphertext Format, Key Serialization

* Added new high-level hybrid `encrypt()` and `decrypt()`
* Introduced standardized single-blob ciphertext format
* Added key serialization helpers
* Improved decapsulation API
* Legacy API preserved for compatibility

---

## Disclaimer

This library is for educational, experimental, and research use.
It has not undergone formal security review and should not be used in production systems.

---

## License

MIT License.

---

## Resources

* Open Quantum Safe: [https://openquantumsafe.org](https://openquantumsafe.org)
* liboqs-python: [https://github.com/open-quantum-safe/liboqs-python](https://github.com/open-quantum-safe/liboqs-python)

# Device Authentication Security Model

## Overview

This document describes the **cryptographic signature-based authentication** used for device registration, replacing the insecure shared PGP key approach.

## Problem: Shared PGP Key (Old Approach)

### Security Vulnerabilities

❌ **Shared Secret Across All Devices**
- Single PGP public key (`/opt/files/nodecontrol.gpg`) used by ALL devices
- If leaked, allows impersonation of ANY device
- No way to revoke for specific device

❌ **No Device Authenticity Verification**
- Backend cannot verify which device sent the request
- Any device can claim any serial number
- Replay attacks possible

❌ **No Tamper Detection**
- PGP provides confidentiality but not authenticity in this model
- Intercepted payloads can be modified

❌ **Poor Key Distribution**
- Requires pre-distributing shared key to all devices
- Key rotation affects all devices simultaneously

## Solution: RSA Signature-Based Authentication

### Security Model

✅ **Device-Specific Cryptographic Proof**
- Each device signs registration payload with its OWN blockchain private key
- Backend verifies signature using blockchain public key IN the payload
- Proves device possesses the private key matching the public key

✅ **Payload Integrity**
- RSA-PSS signature ensures payload hasn't been tampered with
- Any modification invalidates the signature

✅ **Replay Protection**
- Timestamp and cryptographic nonce included in signed payload
- Backend can reject old/reused requests

✅ **No Shared Secrets**
- Each device has unique keypair
- Compromise of one device doesn't affect others

## How It Works

### Device Side (vmanage-agent)

```python
# 1. Device generates blockchain keypair during initialization
km = KeyManager()
blockchain_private, blockchain_public = km.generate_blockchain_keys()

# 2. Create registration payload
payload = {
    "serial_number": "ABC123",
    "hostname": "device-001",
    "wireguard_controller_public_key": "...",
    "wireguard_tunnel_public_key": "...",
    "blockchain_public_key": blockchain_public,  # ← Public key included
    "public_ip": "203.0.113.1",
    "timestamp": "2025-11-22T10:30:00Z",  # ← Replay protection
    "nonce": "random32bytes..."  # ← Replay protection
}

# 3. Sign payload with blockchain PRIVATE key
payload_json = json.dumps(payload, sort_keys=True)
signature = rsa_sign(payload_json, blockchain_private)

# 4. Send signed payload to backend
jwt_payload = {
    'data': payload,
    'signature': signature_hex
}
send_to_backend(jwt_payload)
```

### Backend Side (platform-api)

```python
# 1. Receive JWT with signed payload
jwt_payload = decode_jwt(request.data['token'])
payload = jwt_payload['data']
signature_hex = jwt_payload['signature']

# 2. Extract blockchain public key from payload itself
blockchain_public_key = payload['blockchain_public_key']

# 3. Verify signature using public key from payload
payload_json = json.dumps(payload, sort_keys=True)
signature = bytes.fromhex(signature_hex)

is_valid = rsa_verify(
    payload_json, 
    signature, 
    blockchain_public_key
)

if not is_valid:
    return Response({'error': 'Invalid signature'}, status=401)

# 4. Check replay protection
timestamp = datetime.fromisoformat(payload['timestamp'])
if datetime.utcnow() - timestamp > timedelta(minutes=5):
    return Response({'error': 'Request expired'}, status=401)

# Check nonce hasn't been used before (store in Redis/DB)
if nonce_already_used(payload['nonce']):
    return Response({'error': 'Replay attack detected'}, status=401)

# 5. Register device with verified public keys
device = Device.objects.create(
    serial_number=payload['serial_number'],
    blockchain_public_key=payload['blockchain_public_key'],
    # ... register other keys
)
```

## Security Properties

### 1. **Authenticity**
- Signature proves device has private key corresponding to public key
- Backend knows request came from device possessing that specific key
- Cannot be forged without private key

### 2. **Integrity**
- Any modification to payload invalidates signature
- Backend detects tampering immediately

### 3. **Non-Repudiation**
- Device cannot deny sending the request
- Cryptographic proof of origin

### 4. **Replay Protection**
- Timestamp ensures requests expire (default: 5 minutes)
- Nonce ensures requests can't be reused
- Backend tracks used nonces in cache (Redis recommended)

### 5. **Forward Secrecy** (for future enhancement)
- Can implement ephemeral key exchange on top of this
- Current model provides strong authentication

## Signature Algorithm

### RSA-PSS (Probabilistic Signature Scheme)

**Why RSA-PSS?**
- Industry standard (PKCS#1 v2.2)
- Provably secure signature scheme
- Built-in randomization prevents signature reuse
- Better security properties than PKCS#1 v1.5

**Parameters:**
```python
signature = private_key.sign(
    payload_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),  # Mask generation
        salt_length=padding.PSS.MAX_LENGTH   # Maximum salt length
    ),
    hashes.SHA256()  # Hash algorithm
)
```

**Verification:**
```python
public_key.verify(
    signature,
    payload_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
```

## Attack Mitigation

### Man-in-the-Middle (MITM)
**Attack:** Intercept and modify registration
**Mitigation:** Signature verification detects any modification

### Replay Attack
**Attack:** Capture and resend valid registration
**Mitigation:** Timestamp + nonce prevent reuse

### Impersonation
**Attack:** Attacker claims to be legitimate device
**Mitigation:** Cannot forge signature without private key

### Key Compromise (Single Device)
**Attack:** One device's private key stolen
**Mitigation:** Only that device compromised, not entire fleet

## Comparison: Old vs. New

| Aspect | Shared PGP Key (Old) | RSA Signature (New) |
|--------|---------------------|---------------------|
| **Authentication** | None (shared secret) | Strong (device-specific) |
| **Confidentiality** | Yes (PGP encryption) | No (not needed for public keys) |
| **Integrity** | Weak | Strong (signature) |
| **Replay Protection** | No | Yes (timestamp + nonce) |
| **Blast Radius** | All devices | Single device |
| **Key Distribution** | Pre-shared | Self-generated |
| **Backend Verification** | Cannot verify origin | Cryptographic proof |

## Implementation Checklist

### vmanage-agent (Device)

- [x] Remove `/opt/files/nodecontrol.gpg` dependency
- [x] Generate blockchain keypair during init
- [x] Sign registration payload with private key
- [x] Include timestamp and nonce in payload
- [x] Send signature alongside data
- [x] Mark `pgp_encrypt_data()` as deprecated

### platform-api (Backend)

- [ ] Create `/api/v1/devices/add/` endpoint
- [ ] Implement signature verification
- [ ] Validate timestamp (max age: 5 minutes)
- [ ] Implement nonce tracking (Redis recommended)
- [ ] Register all three public keys
- [ ] Return success/error response

### Testing

- [ ] Test successful registration
- [ ] Test invalid signature rejection
- [ ] Test expired timestamp rejection
- [ ] Test replay attack detection
- [ ] Test tampered payload rejection

## Backend Implementation Example

```python
# apps/devices/authentication.py

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from django.core.cache import cache
from datetime import datetime, timedelta
import json

def verify_device_registration(jwt_payload):
    """
    Verify device registration request signature.
    
    Returns:
        tuple: (is_valid, error_message, payload)
    """
    try:
        data = jwt_payload['data']
        signature_hex = jwt_payload['signature']
        
        # 1. Check timestamp
        timestamp = datetime.fromisoformat(data['timestamp'])
        age = datetime.utcnow() - timestamp
        if age > timedelta(minutes=5):
            return False, "Request expired (>5 minutes old)", None
        
        # 2. Check nonce (replay protection)
        nonce = data['nonce']
        cache_key = f"device_nonce:{nonce}"
        if cache.get(cache_key):
            return False, "Replay attack detected (nonce reused)", None
        
        # Mark nonce as used (TTL: 10 minutes)
        cache.set(cache_key, True, 600)
        
        # 3. Load public key from payload
        public_key_pem = data['blockchain_public_key']
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )
        
        # 4. Verify signature
        payload_json = json.dumps(data, sort_keys=True)
        payload_bytes = payload_json.encode('utf-8')
        signature = bytes.fromhex(signature_hex)
        
        public_key.verify(
            signature,
            payload_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return True, None, data
        
    except Exception as e:
        return False, f"Signature verification failed: {str(e)}", None
```

## Future Enhancements

### 1. Certificate Authority (CA)
- Backend acts as CA
- Issues signed certificates to devices
- Mutual TLS with client certificates

### 2. Key Rotation Protocol
- Automated key rotation with grace period
- Old and new keys both valid during transition
- Signature with old key, include new public key

### 3. Hardware Security Module (HSM)
- Store private keys in TPM/secure enclave
- Signature operations in hardware
- Cannot extract private key

### 4. Rate Limiting
- Limit registration attempts per serial number
- Prevent brute force attacks

### 5. Audit Logging
- Log all registration attempts
- Track signature failures
- Alert on anomalies

## Migration from Old System

### Phase 1: Preparation (Backend)
1. Implement signature verification endpoint
2. Deploy to staging
3. Test with simulated requests

### Phase 2: Parallel Operation
1. Backend accepts BOTH old (PGP) and new (signature) methods
2. Log which method each device uses
3. Monitor for issues

### Phase 3: Agent Update
1. Deploy new vmanage-agent to devices
2. Devices auto-generate blockchain keys
3. Use signature authentication

### Phase 4: Deprecation
1. After 90 days, log warnings for PGP usage
2. After 120 days, reject PGP requests
3. Remove PGP code

## Security Recommendations

✅ **DO:**
- Use nonce tracking with Redis for high availability
- Set reasonable timestamp window (5 minutes recommended)
- Log all signature verification failures
- Monitor for unusual registration patterns
- Rotate device blockchain keys annually

❌ **DON'T:**
- Accept requests with expired timestamps
- Skip nonce validation (allows replay attacks)
- Store nonces in local memory (use Redis/DB)
- Log private keys or signatures in plain text
- Reuse nonces across requests

## Conclusion

The signature-based authentication provides **strong cryptographic proof** of device identity without relying on shared secrets. This approach:

- **Eliminates shared key vulnerability**
- **Provides per-device authentication**
- **Detects tampering and replay attacks**
- **Scales to millions of devices**
- **Follows industry best practices (RSA-PSS)**

This is a **significant security improvement** over the previous shared PGP key approach.

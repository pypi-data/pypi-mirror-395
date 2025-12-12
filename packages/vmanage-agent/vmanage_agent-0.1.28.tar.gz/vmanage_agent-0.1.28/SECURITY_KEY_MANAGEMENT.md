# vmanage-agent Enhanced Security Architecture

## Overview

The vmanage-agent now implements **three separate cryptographic key types** for maximum security and isolation:

1. **Controller WireGuard Keys** - Management plane (node ↔ controller)
2. **Tunnel WireGuard Keys** - Data plane (node ↔ node via VPP)
3. **Blockchain RSA Keys** - Configuration encryption/decryption

## Security Principles

### Zero Private Key Exposure
- **Private keys NEVER leave the device**
- Only public keys are transmitted to backend
- Private keys stored with strict file permissions (0600)
- Each key type isolated in separate files

### Defense in Depth
- Controller compromise doesn't expose tunnel keys
- Tunnel compromise doesn't expose controller keys
- Blockchain keys protect configuration distribution
- Independent key rotation per type

## Key Storage Layout

```
/etc/vmanage/keys/
├── wireguard-controller-private.key  # Controller connection private key
├── wireguard-controller-public.key   # Controller connection public key
├── wireguard-tunnel-private.key      # Tunnel connection private key
├── wireguard-tunnel-public.key       # Tunnel connection public key
├── blockchain-private.pem            # RSA private key (2048-bit)
├── blockchain-public.pem             # RSA public key (2048-bit)
└── key-metadata.json                 # Creation timestamps & metadata
```

All files have `0600` permissions (owner read/write only).

## Key Usage

### 1. Controller WireGuard Keys

**Purpose**: Management overlay network connection to controller

**Used for**:
- Salt-minion connection to salt-master
- Control plane communications
- Management traffic
- Configuration updates

**Backend Registration**:
```json
POST /api/v1/devices/{id}/keys/
{
  "key_type": "wireguard_controller",
  "public_key": "<controller_public_key>"
}
```

**WireGuard Interface**: Typically `wg-controller0` on host OS (not VPP)

### 2. Tunnel WireGuard Keys

**Purpose**: Data plane underlay for node-to-node connections

**Used for**:
- VPP tunnel interfaces
- OSPF/BGP routing underlay
- Customer traffic tunnels
- Inter-node mesh connectivity

**Backend Registration**:
```json
POST /api/v1/devices/{id}/keys/
{
  "key_type": "wireguard_tunnel",
  "public_key": "<tunnel_public_key>"
}
```

**WireGuard Interface**: Managed by VPP (e.g., `wg0`, `wg1`, etc.)

### 3. Blockchain RSA Keys

**Purpose**: Encrypt/decrypt configuration payloads from blockchain

**Used for**:
- Receiving encrypted tunnel configs
- Receiving encrypted order payloads
- Device-specific configuration distribution
- Secure command delivery

**Backend Registration**:
```json
POST /api/v1/devices/{id}/keys/
{
  "key_type": "blockchain",
  "public_key": "<blockchain_public_key_pem>"
}
```

**Key Size**: RSA 2048-bit (PEM format)

## Agent Workflow

### Initial Device Provisioning

```bash
# 1. Run vmanage-agent with salt master info
sudo vmanage-agent -m salt.example.com -mf <master_fingerprint>

# Agent automatically:
# - Generates all 3 key types
# - Stores private keys locally
# - Sends ONLY public keys to backend (encrypted via PGP)
# - Registers device with backend
```

### What Happens on First Run

1. **System Checks**
   - Verify running as root
   - Check salt-minion service
   - Get system serial number
   - Normalize hostname

2. **Key Generation** (via `KeyManager`)
   ```python
   key_manager = KeyManager()
   all_keys = key_manager.initialize_all_keys()
   # Returns:
   # {
   #   'wg_controller': (private, public),
   #   'wg_tunnel': (private, public),
   #   'blockchain': (private_pem, public_pem)
   # }
   ```

3. **Registration Payload** (PUBLIC KEYS ONLY)
   ```python
   registration_payload = {
       "serial_number": "...",
       "hostname": "...",
       "wireguard_controller_public_key": "...",
       "wireguard_tunnel_public_key": "...",
       "blockchain_public_key": "...",
       "public_ip": "..."
   }
   ```

4. **Encrypted Transmission**
   - Payload encrypted with backend's PGP public key
   - Sent to `/api/v1/devices/add/`
   - Backend stores public keys
   - Backend NEVER sees private keys

## KeyManager API

### Class: `KeyManager`

Located in `vmanage_agent/key_manager.py`

#### Methods

##### `initialize_all_keys(force=False)`
Generate all three key types if they don't exist.

```python
from vmanage_agent.key_manager import KeyManager

km = KeyManager()
keys = km.initialize_all_keys()
# Returns dict with all key pairs
```

##### `generate_wireguard_controller_keys()`
Generate new controller WireGuard keypair.

```python
private_key, public_key = km.generate_wireguard_controller_keys()
```

##### `generate_wireguard_tunnel_keys()`
Generate new tunnel WireGuard keypair.

```python
private_key, public_key = km.generate_wireguard_tunnel_keys()
```

##### `generate_blockchain_keys()`
Generate new RSA keypair for blockchain encryption.

```python
private_pem, public_pem = km.generate_blockchain_keys()
```

##### `get_public_keys_for_registration()`
Get all public keys formatted for backend registration.

```python
public_keys = km.get_public_keys_for_registration()
# Returns:
# {
#   'wireguard_controller_public_key': '...',
#   'wireguard_tunnel_public_key': '...',
#   'blockchain_public_key': '...'
# }
```

##### `rotate_keys(key_type)`
Rotate specific key type.

```python
# Rotate controller keys
new_private, new_public = km.rotate_keys('wg_controller')

# Rotate tunnel keys
new_private, new_public = km.rotate_keys('wg_tunnel')

# Rotate blockchain keys
new_private_pem, new_public_pem = km.rotate_keys('blockchain')
```

##### `get_key_status()`
Get diagnostic information about all keys.

```python
status = km.get_key_status()
# Returns dict with existence and metadata for all keys
```

## Key Rotation

### Automated Rotation (Backend-Initiated)

Backend sends blockchain notification when keys need rotation:

```json
{
  "action": "rotate_keys",
  "key_type": "wg_controller",  // or "wg_tunnel"
  "reason": "expiring_soon"
}
```

Device daemon:
1. Receives encrypted notification
2. Generates new keypair
3. Registers new public key with backend
4. Updates local configuration
5. Old keys invalidated

### Manual Rotation

```python
from vmanage_agent.key_manager import KeyManager

km = KeyManager()

# Rotate controller keys
private, public = km.rotate_keys('wg_controller')

# Register new public key with backend
import requests
requests.post(
    f"{backend_url}/api/v1/devices/{device_id}/keys/",
    json={
        "key_type": "wireguard_controller",
        "public_key": public
    }
)
```

## Security Best Practices

### ✅ DO

- Run vmanage-agent as root (required for key directory permissions)
- Verify `/etc/vmanage/keys/` has `0700` permissions
- Verify all key files have `0600` permissions
- Regularly rotate keys (controller: 90 days, tunnel: 90 days)
- Back up private keys to secure offline storage
- Use separate keys for dev/staging/prod environments

### ❌ DON'T

- Never transmit private keys over network
- Never log private keys (even in debug mode)
- Never store private keys in version control
- Never share private keys between devices
- Never reuse keys across environments
- Never run agent as non-root user

## Troubleshooting

### Keys Not Generated

**Symptom**: `KeyManager` reports keys missing

**Solution**:
```bash
# Check directory exists and has correct permissions
ls -la /etc/vmanage/keys/
# Should show: drwx------ (700)

# If missing, create manually
sudo mkdir -p /etc/vmanage/keys
sudo chmod 700 /etc/vmanage/keys

# Re-run agent
sudo vmanage-agent -m <master> -mf <fingerprint>
```

### Permission Denied Errors

**Symptom**: Cannot write to `/etc/vmanage/keys/`

**Solution**:
```bash
# Verify running as root
id
# Should show uid=0(root)

# Fix directory permissions
sudo chown root:root /etc/vmanage/keys
sudo chmod 700 /etc/vmanage/keys
```

### Key Already Exists Error

**Symptom**: Agent won't regenerate keys

**Solution**:
```python
# Force regeneration in Python
from vmanage_agent.key_manager import KeyManager
km = KeyManager()
km.initialize_all_keys(force=True)
```

Or manually delete old keys:
```bash
sudo rm -rf /etc/vmanage/keys/*
# Re-run agent to generate fresh keys
```

## Migration from Old Agent

### Before (Single Key)

Old agent generated one WireGuard key for everything:
```python
private_key, public_key = generate_wireguard_keys()
# Sent BOTH private and public to backend (INSECURE!)
```

### After (Three Separate Keys)

New agent generates three isolated keys:
```python
key_manager = KeyManager()
keys = key_manager.initialize_all_keys()
# Sends ONLY public keys to backend (SECURE!)
```

### Migration Steps

1. **Stop old agent** (if running as service)
   ```bash
   sudo systemctl stop vmanage-agent
   ```

2. **Backup existing keys** (if you want to preserve controller connection)
   ```bash
   # If old keys exist somewhere
   sudo mkdir -p /etc/vmanage/keys
   sudo cp /old/location/private.key /etc/vmanage/keys/wireguard-controller-private.key
   sudo cp /old/location/public.key /etc/vmanage/keys/wireguard-controller-public.key
   ```

3. **Run new agent**
   ```bash
   sudo vmanage-agent -m <master> -mf <fingerprint>
   # Will generate tunnel and blockchain keys, preserve controller keys if they exist
   ```

4. **Verify all keys exist**
   ```bash
   ls -la /etc/vmanage/keys/
   # Should show 6 key files + metadata
   ```

## Backend Integration

### Expected Backend Changes

The backend `/api/v1/devices/add/` endpoint should be updated to accept three public keys:

```python
# In platform-api: api/customer/v1/devices/views.py

def device_registration(request):
    payload = decrypt_pgp(request.data['token'])
    
    device = Device.objects.create(
        serial_number=payload['serial_number'],
        hostname=payload['hostname'],
        # ... other fields
    )
    
    # Register all three public keys
    if 'wireguard_controller_public_key' in payload:
        device.register_wireguard_public_key(
            public_key=payload['wireguard_controller_public_key'],
            key_type='controller'
        )
    
    if 'wireguard_tunnel_public_key' in payload:
        device.register_wireguard_public_key(
            public_key=payload['wireguard_tunnel_public_key'],
            key_type='tunnel'
        )
    
    if 'blockchain_public_key' in payload:
        device.blockchain_public_key = payload['blockchain_public_key']
        device.save(update_fields=['blockchain_public_key'])
    
    return Response({'success': True})
```

## Testing

### Unit Tests

```python
# tests/test_key_manager.py
import pytest
from vmanage_agent.key_manager import KeyManager
from pathlib import Path

def test_generate_all_keys(tmp_path):
    # Override key directory for testing
    KeyManager.KEY_DIR = tmp_path / "keys"
    
    km = KeyManager()
    keys = km.initialize_all_keys()
    
    assert 'wg_controller' in keys
    assert 'wg_tunnel' in keys
    assert 'blockchain' in keys
    
    # Verify files exist
    assert km.WG_CONTROLLER_PRIVATE_KEY.exists()
    assert km.WG_TUNNEL_PRIVATE_KEY.exists()
    assert km.BLOCKCHAIN_PRIVATE_KEY.exists()

def test_public_keys_no_private_leak():
    km = KeyManager()
    public_keys = km.get_public_keys_for_registration()
    
    # Ensure no private key data in public keys dict
    assert 'private' not in str(public_keys).lower()
    assert len(public_keys) == 3
```

### Integration Test

```bash
# Test full agent workflow
sudo python3 -m vmanage_agent.main -m test.salt.local -mf test123

# Verify keys created
ls -la /etc/vmanage/keys/

# Verify permissions
stat -c "%a" /etc/vmanage/keys/wireguard-controller-private.key
# Should output: 600
```

## Related Documentation

- **Backend**: `/Users/pdang/codes/platform-api/docs/WIREGUARD_KEY_SEPARATION.md`
- **Security**: `/Users/pdang/codes/platform-api/docs/SECURE_KEY_MANAGEMENT.md`
- **Device API**: `/Users/pdang/codes/platform-api/docs/DEVICE_KEY_MANAGEMENT_API.md`

## Support

For issues or questions:
- Check logs: `/var/log/vmanage-agent.log`
- Review key status: `KeyManager().get_key_status()`
- Verify backend received keys: Check Device admin panel

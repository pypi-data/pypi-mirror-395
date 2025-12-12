# vmanage-agent v0.2.0 - Enhanced Security Release

**Release Date:** November 22, 2025

## 🔐 Major Security Enhancement

This release implements **comprehensive cryptographic key separation** for maximum security and compliance with WireGuard best practices.

### Breaking Changes

⚠️ **Device registration payload format has changed**

**Old (v0.1.x):**
```json
{
  "private_key": "...",  // INSECURE - transmitted private key
  "public_key": "..."
}
```

**New (v0.2.0):**
```json
{
  "wireguard_controller_public_key": "...",
  "wireguard_tunnel_public_key": "...",
  "blockchain_public_key": "..."
  // NO PRIVATE KEYS TRANSMITTED
}
```

### New Features

#### 🎯 Three Separate Key Types

1. **Controller WireGuard Keys**
   - Purpose: Management plane (node ↔ controller)
   - Storage: `/etc/vmanage/keys/wireguard-controller-*.key`
   - Rotation: 90 days

2. **Tunnel WireGuard Keys**
   - Purpose: Data plane VPP underlay (node ↔ node)
   - Storage: `/etc/vmanage/keys/wireguard-tunnel-*.key`
   - Rotation: 90 days

3. **Blockchain RSA Keys**
   - Purpose: Configuration encryption/decryption
   - Storage: `/etc/vmanage/keys/blockchain-*.pem`
   - Type: RSA 2048-bit

#### 🛡️ KeyManager Class

New `KeyManager` module (`vmanage_agent/key_manager.py`) provides:
- Automatic key generation on first run
- Secure file permissions (0600)
- Independent key rotation
- Metadata tracking
- Public key export

#### 🔧 CLI Management Tool

New `vmanage-keys` command for operators:

```bash
vmanage-keys status              # Show key status
vmanage-keys init                # Initialize all keys
vmanage-keys rotate <type>       # Rotate specific key
vmanage-keys export              # Export public keys
```

### Security Improvements

✅ **Zero Private Key Exposure**
- Private keys NEVER transmitted to backend
- Only public keys sent during registration
- All private keys stay on device filesystem

✅ **Key Isolation**
- Controller compromise doesn't expose tunnel keys
- Tunnel compromise doesn't expose controller keys
- Each key type has independent lifecycle

✅ **Secure Storage**
- Keys stored in `/etc/vmanage/keys/` with 0700 permissions
- All key files have 0600 permissions (owner read/write only)
- Metadata tracked in secure JSON file

✅ **Defense in Depth**
- Multiple independent cryptographic layers
- Blockchain encryption for config distribution
- Separate keys for control vs. data plane

### Migration Guide

#### Fresh Installations
No action needed - just run the agent:
```bash
sudo vmanage-agent -m <master> -mf <fingerprint>
```

#### Existing Deployments

1. **Backup old keys** (optional - to preserve controller connection):
   ```bash
   sudo mkdir -p /etc/vmanage/keys
   sudo cp /old/path/private.key /etc/vmanage/keys/wireguard-controller-private.key
   sudo cp /old/path/public.key /etc/vmanage/keys/wireguard-controller-public.key
   sudo chmod 600 /etc/vmanage/keys/*
   ```

2. **Update package**:
   ```bash
   sudo pip3 install --upgrade vmanage-agent
   ```

3. **Initialize new keys**:
   ```bash
   sudo vmanage-keys init
   ```

4. **Verify**:
   ```bash
   sudo vmanage-keys status
   ```

### Backend Requirements

⚠️ **Backend must be updated to accept three public keys**

Update `platform-api/api/customer/v1/devices/views.py`:
```python
# Register all three public keys during device add
device.register_wireguard_public_key(
    payload['wireguard_controller_public_key'], 
    key_type='controller'
)
device.register_wireguard_public_key(
    payload['wireguard_tunnel_public_key'],
    key_type='tunnel'
)
device.blockchain_public_key = payload['blockchain_public_key']
```

See `platform-api/docs/WIREGUARD_KEY_SEPARATION.md` for details.

### Files Changed

**New:**
- `vmanage_agent/key_manager.py` - Key management class
- `vmanage_agent/cli_keys.py` - CLI tool
- `SECURITY_KEY_MANAGEMENT.md` - Security documentation
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `QUICK_REFERENCE.md` - Operator quick reference

**Modified:**
- `vmanage_agent/main.py` - Uses KeyManager, sends 3 public keys
- `vmanage_agent/utils.py` - Removed old `generate_wireguard_keys()`
- `pyproject.toml` - Added `vmanage-keys` CLI script
- `README.md` - Added security features overview

**Removed:**
- Old single-key generation logic

### Dependencies

No new dependencies required - using existing:
- `cryptography ^41.0.7` ✓
- `loguru ^0.7.2` ✓
- `pgpy ^0.6.0` ✓

### Testing

Tested on:
- Ubuntu 20.04 LTS
- Ubuntu 22.04 LTS
- Debian 11

### Documentation

Comprehensive documentation added:
- **SECURITY_KEY_MANAGEMENT.md** - Complete security architecture
- **IMPLEMENTATION_SUMMARY.md** - Technical implementation details
- **QUICK_REFERENCE.md** - Operator quick reference
- **README.md** - Updated with security overview

### Known Issues

None at release time.

### Upgrade Notes

1. **Backward Compatibility:** v0.2.0 can read legacy keys if migrated properly
2. **Backend Update Required:** Backend MUST support three-key registration
3. **Permission Requirements:** Must run as root for key directory access

### Contributors

- Phan Dang <phan.dang@usdatanetworks.com>

---

## Version History

### v0.2.0 (2025-11-22) - Enhanced Security Release
- ✨ Three separate key types (controller, tunnel, blockchain)
- 🔐 Zero private key transmission
- 🛡️ KeyManager class for key lifecycle
- 🔧 vmanage-keys CLI tool
- 📚 Comprehensive security documentation

### v0.1.28 (Previous)
- Single WireGuard key generation
- Basic device registration

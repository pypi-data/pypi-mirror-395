# vmanage-agent Quick Reference

## Installation

```bash
sudo pip3 install https://usdn-repo-bucket.s3.amazonaws.com/vmanage-agent/vmanage_agent-latest.tar.gz
```

## First Run (Device Provisioning)

```bash
sudo vmanage-agent -m salt.example.com -mf <master_fingerprint>
```

**What it does:**
- Generates 3 cryptographic key pairs
- Stores private keys in `/etc/vmanage/keys/` (secure)
- Sends ONLY public keys to backend
- Joins salt-master

## Key Management Commands

### Check Key Status
```bash
sudo vmanage-keys status
```

### Initialize Keys (if missing)
```bash
sudo vmanage-keys init
```

### Rotate Specific Key
```bash
# Rotate controller key
sudo vmanage-keys rotate wg_controller

# Rotate tunnel key
sudo vmanage-keys rotate wg_tunnel

# Rotate blockchain key
sudo vmanage-keys rotate blockchain
```

### Export Public Keys
```bash
# Human-readable format
sudo vmanage-keys export

# JSON format
sudo vmanage-keys export --format json
```

## Key Types

| Key Type | Purpose | Location | Rotation Period |
|----------|---------|----------|----------------|
| **Controller WG** | Management overlay | `/etc/vmanage/keys/wireguard-controller-*.key` | 90 days |
| **Tunnel WG** | Data plane VPP | `/etc/vmanage/keys/wireguard-tunnel-*.key` | 90 days |
| **Blockchain RSA** | Config encryption | `/etc/vmanage/keys/blockchain-*.pem` | Never |

## Troubleshooting

### Keys Missing
```bash
# Reinitialize
sudo vmanage-keys init
```

### Permission Denied
```bash
# Fix permissions
sudo chown -R root:root /etc/vmanage/keys
sudo chmod 700 /etc/vmanage/keys
sudo chmod 600 /etc/vmanage/keys/*
```

### View Logs
```bash
sudo tail -f /var/log/vmanage-agent.log
```

## Security Notes

⚠️ **NEVER share private keys**  
⚠️ **NEVER transmit private keys over network**  
✓ **Always run as root** (for key directory permissions)  
✓ **Backup keys to secure offline storage**  
✓ **Rotate keys every 90 days**

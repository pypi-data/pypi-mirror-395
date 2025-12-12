# vmanage-agent Security Architecture Diagram

## Three-Key Separation Model

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DEVICE NODE                                 │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                    KeyManager                               │   │
│  │                                                             │   │
│  │  /etc/vmanage/keys/                                        │   │
│  │  ├── wireguard-controller-private.key  (0600) ◄──┐        │   │
│  │  ├── wireguard-controller-public.key   (0600)    │        │   │
│  │  ├── wireguard-tunnel-private.key      (0600) ◄──┼──┐     │   │
│  │  ├── wireguard-tunnel-public.key       (0600)    │  │     │   │
│  │  ├── blockchain-private.pem            (0600) ◄──┼──┼──┐  │   │
│  │  ├── blockchain-public.pem             (0600)    │  │  │  │   │
│  │  └── key-metadata.json                 (0600)    │  │  │  │   │
│  │                                                   │  │  │  │   │
│  └───────────────────────────────────────────────────┼──┼──┼──┘   │
│                                                       │  │  │      │
│  ┌────────────────────────────────────────────┐      │  │  │      │
│  │  WireGuard Controller Interface            │      │  │  │      │
│  │  (wg-controller0)                          │      │  │  │      │
│  │  - Management traffic only                 │◄─────┘  │  │      │
│  │  - Salt-minion connection                  │         │  │      │
│  │  - Control plane                           │         │  │      │
│  └────────────────────────────────────────────┘         │  │      │
│                                                          │  │      │
│  ┌────────────────────────────────────────────┐         │  │      │
│  │  VPP WireGuard Tunnel Interfaces           │         │  │      │
│  │  (wg0, wg1, wg2, ...)                      │         │  │      │
│  │  - Data plane traffic                      │◄────────┘  │      │
│  │  - OSPF/BGP underlay                       │            │      │
│  │  - Customer tunnels                        │            │      │
│  └────────────────────────────────────────────┘            │      │
│                                                             │      │
│  ┌────────────────────────────────────────────┐            │      │
│  │  Blockchain Config Receiver                │            │      │
│  │  - Decrypts configuration payloads         │◄───────────┘      │
│  │  - Receives tunnel configs                 │                   │
│  │  - Applies VPP settings                    │                   │
│  └────────────────────────────────────────────┘                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS (TLS)
                              │ PGP-encrypted payload
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        BACKEND (platform-api)                        │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Device Model                                                │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  wireguard_controller_public_key                     │   │   │
│  │  │  wireguard_controller_key_created_at                 │   │   │
│  │  │  wireguard_controller_key_expires_at                 │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  wireguard_tunnel_public_key                         │   │   │
│  │  │  wireguard_tunnel_key_created_at                     │   │   │
│  │  │  wireguard_tunnel_key_expires_at                     │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  blockchain_public_key (RSA PEM)                     │   │   │
│  │  │  blockchain_private_key (ENCRYPTED at rest)          │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ⚠️  NO WIREGUARD PRIVATE KEYS STORED                     │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Controller Model (WireGuardConnection)                     │   │
│  │                                                              │   │
│  │  public_key  ────────► References device.wg_controller_key  │   │
│  │  ❌ private_key (REMOVED for security)                      │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Tunnel Model                                                │   │
│  │                                                              │   │
│  │  local_public_key  ───────► References device.wg_tunnel_key │   │
│  │  remote_public_key ───────► References peer.wg_tunnel_key   │   │
│  │  ❌ local_private_key (Returns None - device-local)         │   │
│  │  ❌ remote_private_key (Returns None - device-local)        │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow: Device Registration

```
┌─────────────┐
│   DEVICE    │
└──────┬──────┘
       │
       │ 1. Generate Keys
       │    KeyManager.initialize_all_keys()
       │
       ▼
┌──────────────────────────────────────┐
│  /etc/vmanage/keys/                  │
│  - controller private/public         │
│  - tunnel private/public             │
│  - blockchain private/public         │
└──────┬───────────────────────────────┘
       │
       │ 2. Extract Public Keys Only
       │
       ▼
┌──────────────────────────────────────┐
│  Registration Payload                │
│  {                                   │
│    "wg_controller_public": "...",    │
│    "wg_tunnel_public": "...",        │
│    "blockchain_public": "..."        │
│  }                                   │
└──────┬───────────────────────────────┘
       │
       │ 3. Encrypt with Backend PGP Key
       │
       ▼
┌──────────────────────────────────────┐
│  PGP Encrypted Payload               │
│  -----BEGIN PGP MESSAGE-----         │
│  ...encrypted data...                │
│  -----END PGP MESSAGE-----           │
└──────┬───────────────────────────────┘
       │
       │ 4. HTTPS POST /api/v1/devices/add/
       │
       ▼
┌─────────────┐
│   BACKEND   │
└──────┬──────┘
       │
       │ 5. Decrypt PGP
       │
       ▼
┌──────────────────────────────────────┐
│  Device.register_wireguard_public_   │
│  key(pub_key, key_type='controller') │
│                                      │
│  Device.register_wireguard_public_   │
│  key(pub_key, key_type='tunnel')     │
│                                      │
│  Device.blockchain_public_key = pub  │
└──────┬───────────────────────────────┘
       │
       │ 6. Store in Database
       │    (PUBLIC KEYS ONLY)
       │
       ▼
┌─────────────┐
│  COMPLETED  │
└─────────────┘
```

## Data Flow: Tunnel Configuration

```
┌─────────────┐
│   BACKEND   │
└──────┬──────┘
       │
       │ 1. Build Tunnel Config
       │
       ▼
┌───────────────────────────────────────┐
│  Tunnel Config                        │
│  {                                    │
│    "tunnel_id": 123,                  │
│    "private_key_path":                │
│      "/etc/vmanage/keys/              │
│       wireguard-tunnel-private.key",  │
│    "peers": [{                        │
│      "public_key": "<peer_wg_pub>",   │
│      "endpoint": "1.2.3.4:51820"      │
│    }]                                 │
│  }                                    │
└───────┬───────────────────────────────┘
        │
        │ 2. Encrypt with Device's Blockchain Public Key
        │
        ▼
┌───────────────────────────────────────┐
│  Encrypted Config                     │
│  (RSA encrypted with device's         │
│   blockchain_public_key)              │
└───────┬───────────────────────────────┘
        │
        │ 3. Post to Blockchain
        │
        ▼
┌─────────────┐
│ BLOCKCHAIN  │
└──────┬──────┘
       │
       │ 4. Device Polls Blockchain
       │
       ▼
┌─────────────┐
│   DEVICE    │
└──────┬──────┘
       │
       │ 5. Decrypt with Blockchain Private Key
       │    (from /etc/vmanage/keys/blockchain-private.pem)
       │
       ▼
┌───────────────────────────────────────┐
│  Decrypted Config                     │
│  {                                    │
│    "tunnel_id": 123,                  │
│    "private_key_path": "...",         │
│    "peers": [...]                     │
│  }                                    │
└───────┬───────────────────────────────┘
        │
        │ 6. Configure WireGuard
        │    wg set wg0 \
        │      private-key /etc/vmanage/keys/wireguard-tunnel-private.key \
        │      peer <pub_key> ...
        │
        ▼
┌─────────────┐
│   VPP/WG    │
│  CONFIGURED │
└─────────────┘
```

## Security Boundaries

```
┌──────────────────────────────────────────────────┐
│  DEVICE TRUST BOUNDARY                           │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │  Private Keys (NEVER leave device)      │    │
│  │  - wg-controller-private.key            │    │
│  │  - wg-tunnel-private.key                │    │
│  │  - blockchain-private.pem               │    │
│  │                                          │    │
│  │  Permissions: 0600 (owner only)         │    │
│  │  Owner: root:root                       │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │  Public Keys (safe to transmit)         │    │
│  │  - Sent to backend during registration  │    │
│  │  - Used by peers for WireGuard config   │    │
│  │  - Stored in backend database           │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  NETWORK TRUST BOUNDARY                          │
│                                                  │
│  ✓ TLS encryption                                │
│  ✓ PGP payload encryption                        │
│  ✓ Only public keys transmitted                  │
│  ✓ Private keys NEVER cross boundary             │
│                                                  │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  BACKEND TRUST BOUNDARY                          │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │  Public Keys (stored)                   │    │
│  │  - wireguard_controller_public_key      │    │
│  │  - wireguard_tunnel_public_key          │    │
│  │  - blockchain_public_key                │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │  Backend Private Keys (encrypted)       │    │
│  │  - blockchain_private_key (for device)  │    │
│  │    ↳ EncryptedTextField (at rest)       │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  ❌ NO WireGuard private keys stored            │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Key Lifecycle

```
CREATION         ACTIVE           ROTATION         EXPIRED
   │               │                  │                │
   ▼               ▼                  ▼                ▼
┌────────┐    ┌────────┐        ┌────────┐      ┌────────┐
│Generate│───►│In Use  │───────►│Rotate  │─────►│Replace │
│Keys    │    │(90 days│        │Warning │      │Old Key │
│        │    │ for WG)│        │(7 days)│      │        │
└────────┘    └────────┘        └────────┘      └────────┘
   │               │                  │                │
   │               │                  │                │
   ▼               ▼                  ▼                ▼
Private    Private Key        Backend          New Key
Keys       Used Daily         Notifies         Generated
Stay On                       Device           Locally
Device                                         │
   │                                           │
   └───────────────────────────────────────────┘
              Public Key Sent to Backend
```

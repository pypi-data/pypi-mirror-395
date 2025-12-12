"""
Key Manager Module for vmanage-agent

Manages three distinct cryptographic key types:
1. Controller WireGuard Keys - For node-to-controller management connection
2. Tunnel WireGuard Keys - For node-to-node VPP underlay connections
3. Blockchain Keys - For RSA encryption/decryption of configuration payloads

Security Principles:
- Private keys NEVER transmitted to backend
- Private keys stored with strict file permissions (0600)
- Each key type isolated in separate files
- Public keys registered with backend via API
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Tuple, Dict, Optional
from loguru import logger as log
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class KeyManager:
    """Manages cryptographic keys for device authentication and encryption"""
    
    # Key storage locations
    KEY_DIR = Path("/etc/vmanage/keys")
    
    # WireGuard Controller Keys (node-to-controller)
    WG_CONTROLLER_PRIVATE_KEY = KEY_DIR / "wireguard-controller-private.key"
    WG_CONTROLLER_PUBLIC_KEY = KEY_DIR / "wireguard-controller-public.key"
    
    # WireGuard Tunnel Keys (node-to-node via VPP)
    WG_TUNNEL_PRIVATE_KEY = KEY_DIR / "wireguard-tunnel-private.key"
    WG_TUNNEL_PUBLIC_KEY = KEY_DIR / "wireguard-tunnel-public.key"
    
    # Blockchain Encryption Keys (RSA)
    BLOCKCHAIN_PRIVATE_KEY = KEY_DIR / "blockchain-private.pem"
    BLOCKCHAIN_PUBLIC_KEY = KEY_DIR / "blockchain-public.pem"
    
    # Metadata file to track key creation timestamps
    KEY_METADATA = KEY_DIR / "key-metadata.json"
    
    def __init__(self):
        """Initialize KeyManager and ensure key directory exists"""
        self._ensure_key_directory()
        
    def _ensure_key_directory(self):
        """Create key directory with secure permissions"""
        self.KEY_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
        log.debug(f"Key directory ensured at {self.KEY_DIR}")
    
    def _set_secure_permissions(self, filepath: Path):
        """Set secure file permissions (owner read/write only)"""
        os.chmod(filepath, 0o600)
        log.debug(f"Set secure permissions (0600) on {filepath}")
    
    def _save_metadata(self, key_type: str, created_at: str):
        """Save key creation metadata"""
        metadata = {}
        if self.KEY_METADATA.exists():
            with open(self.KEY_METADATA, 'r') as f:
                metadata = json.load(f)
        
        metadata[key_type] = {
            'created_at': created_at,
            'filepath': str(getattr(self, f"{key_type.upper()}_PUBLIC_KEY"))
        }
        
        with open(self.KEY_METADATA, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self._set_secure_permissions(self.KEY_METADATA)
    
    # =========================================================================
    # WireGuard Controller Keys
    # =========================================================================
    
    def generate_wireguard_controller_keys(self) -> Tuple[str, str]:
        """
        Generate WireGuard keypair for controller connection.
        
        Returns:
            Tuple[str, str]: (private_key, public_key)
        """
        log.info("Generating WireGuard controller connection keys...")
        
        # Generate private key
        private_key = subprocess.check_output(["wg", "genkey"]).strip().decode('utf-8')
        
        # Generate public key from private key
        public_key_proc = subprocess.Popen(
            ["wg", "pubkey"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        public_key_proc.stdin.write(private_key.encode())
        public_key_proc.stdin.close()
        public_key = public_key_proc.stdout.read().strip().decode('utf-8')
        
        # Save keys to files
        self.WG_CONTROLLER_PRIVATE_KEY.write_text(private_key + '\n')
        self.WG_CONTROLLER_PUBLIC_KEY.write_text(public_key + '\n')
        
        # Set secure permissions
        self._set_secure_permissions(self.WG_CONTROLLER_PRIVATE_KEY)
        self._set_secure_permissions(self.WG_CONTROLLER_PUBLIC_KEY)
        
        # Save metadata
        from datetime import datetime
        self._save_metadata('wg_controller', datetime.utcnow().isoformat())
        
        log.info(f"✓ Controller WireGuard keys saved to {self.KEY_DIR}")
        log.debug(f"Public key: {public_key[:20]}...")
        
        return private_key, public_key
    
    def get_wireguard_controller_keys(self) -> Optional[Tuple[str, str]]:
        """
        Retrieve existing WireGuard controller keys.
        
        Returns:
            Optional[Tuple[str, str]]: (private_key, public_key) or None if not found
        """
        if not self.WG_CONTROLLER_PRIVATE_KEY.exists():
            log.warning("WireGuard controller keys not found")
            return None
        
        private_key = self.WG_CONTROLLER_PRIVATE_KEY.read_text().strip()
        public_key = self.WG_CONTROLLER_PUBLIC_KEY.read_text().strip()
        
        return private_key, public_key
    
    # =========================================================================
    # WireGuard Tunnel Keys
    # =========================================================================
    
    def generate_wireguard_tunnel_keys(self) -> Tuple[str, str]:
        """
        Generate WireGuard keypair for tunnel connections (node-to-node VPP).
        
        Returns:
            Tuple[str, str]: (private_key, public_key)
        """
        log.info("Generating WireGuard tunnel connection keys...")
        
        # Generate private key
        private_key = subprocess.check_output(["wg", "genkey"]).strip().decode('utf-8')
        
        # Generate public key from private key
        public_key_proc = subprocess.Popen(
            ["wg", "pubkey"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        public_key_proc.stdin.write(private_key.encode())
        public_key_proc.stdin.close()
        public_key = public_key_proc.stdout.read().strip().decode('utf-8')
        
        # Save keys to files
        self.WG_TUNNEL_PRIVATE_KEY.write_text(private_key + '\n')
        self.WG_TUNNEL_PUBLIC_KEY.write_text(public_key + '\n')
        
        # Set secure permissions
        self._set_secure_permissions(self.WG_TUNNEL_PRIVATE_KEY)
        self._set_secure_permissions(self.WG_TUNNEL_PUBLIC_KEY)
        
        # Save metadata
        from datetime import datetime
        self._save_metadata('wg_tunnel', datetime.utcnow().isoformat())
        
        log.info(f"✓ Tunnel WireGuard keys saved to {self.KEY_DIR}")
        log.debug(f"Public key: {public_key[:20]}...")
        
        return private_key, public_key
    
    def get_wireguard_tunnel_keys(self) -> Optional[Tuple[str, str]]:
        """
        Retrieve existing WireGuard tunnel keys.
        
        Returns:
            Optional[Tuple[str, str]]: (private_key, public_key) or None if not found
        """
        if not self.WG_TUNNEL_PRIVATE_KEY.exists():
            log.warning("WireGuard tunnel keys not found")
            return None
        
        private_key = self.WG_TUNNEL_PRIVATE_KEY.read_text().strip()
        public_key = self.WG_TUNNEL_PUBLIC_KEY.read_text().strip()
        
        return private_key, public_key
    
    # =========================================================================
    # Blockchain RSA Keys
    # =========================================================================
    
    def generate_blockchain_keys(self) -> Tuple[str, str]:
        """
        Generate RSA keypair for blockchain payload encryption/decryption.
        
        Returns:
            Tuple[str, str]: (private_key_pem, public_key_pem)
        """
        log.info("Generating blockchain RSA keys (2048-bit)...")
        
        # Generate RSA private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Serialize private key to PEM format
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        
        # Serialize public key to PEM format
        public_key_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
        
        # Save keys to files
        self.BLOCKCHAIN_PRIVATE_KEY.write_text(private_key_pem)
        self.BLOCKCHAIN_PUBLIC_KEY.write_text(public_key_pem)
        
        # Set secure permissions
        self._set_secure_permissions(self.BLOCKCHAIN_PRIVATE_KEY)
        self._set_secure_permissions(self.BLOCKCHAIN_PUBLIC_KEY)
        
        # Save metadata
        from datetime import datetime
        self._save_metadata('blockchain', datetime.utcnow().isoformat())
        
        log.info(f"✓ Blockchain RSA keys saved to {self.KEY_DIR}")
        
        return private_key_pem, public_key_pem
    
    def get_blockchain_keys(self) -> Optional[Tuple[str, str]]:
        """
        Retrieve existing blockchain RSA keys.
        
        Returns:
            Optional[Tuple[str, str]]: (private_key_pem, public_key_pem) or None
        """
        if not self.BLOCKCHAIN_PRIVATE_KEY.exists():
            log.warning("Blockchain RSA keys not found")
            return None
        
        private_key_pem = self.BLOCKCHAIN_PRIVATE_KEY.read_text()
        public_key_pem = self.BLOCKCHAIN_PUBLIC_KEY.read_text()
        
        return private_key_pem, public_key_pem
    
    # =========================================================================
    # Unified Key Management
    # =========================================================================
    
    def initialize_all_keys(self, force: bool = False) -> Dict[str, Tuple[str, str]]:
        """
        Initialize all three key types if they don't exist.
        
        Args:
            force: If True, regenerate keys even if they exist
        
        Returns:
            Dict with all public keys for registration
        """
        keys = {}
        
        # WireGuard Controller Keys
        if force or not self.WG_CONTROLLER_PRIVATE_KEY.exists():
            priv, pub = self.generate_wireguard_controller_keys()
            keys['wg_controller'] = (priv, pub)
        else:
            log.info("WireGuard controller keys already exist")
            keys['wg_controller'] = self.get_wireguard_controller_keys()
        
        # WireGuard Tunnel Keys
        if force or not self.WG_TUNNEL_PRIVATE_KEY.exists():
            priv, pub = self.generate_wireguard_tunnel_keys()
            keys['wg_tunnel'] = (priv, pub)
        else:
            log.info("WireGuard tunnel keys already exist")
            keys['wg_tunnel'] = self.get_wireguard_tunnel_keys()
        
        # Blockchain RSA Keys
        if force or not self.BLOCKCHAIN_PRIVATE_KEY.exists():
            priv, pub = self.generate_blockchain_keys()
            keys['blockchain'] = (priv, pub)
        else:
            log.info("Blockchain RSA keys already exist")
            keys['blockchain'] = self.get_blockchain_keys()
        
        return keys
    
    def get_public_keys_for_registration(self) -> Dict[str, str]:
        """
        Get all public keys formatted for backend registration.
        
        Returns:
            Dict with public keys only (never send private keys!)
        """
        keys = self.initialize_all_keys(force=False)
        
        return {
            'wireguard_controller_public_key': keys['wg_controller'][1],
            'wireguard_tunnel_public_key': keys['wg_tunnel'][1],
            'blockchain_public_key': keys['blockchain'][1]
        }
    
    def rotate_keys(self, key_type: str) -> Tuple[str, str]:
        """
        Rotate (regenerate) specific key type.
        
        Args:
            key_type: One of 'wg_controller', 'wg_tunnel', 'blockchain'
        
        Returns:
            Tuple[str, str]: (private_key, public_key)
        """
        log.warning(f"Rotating {key_type} keys...")
        
        if key_type == 'wg_controller':
            return self.generate_wireguard_controller_keys()
        elif key_type == 'wg_tunnel':
            return self.generate_wireguard_tunnel_keys()
        elif key_type == 'blockchain':
            return self.generate_blockchain_keys()
        else:
            raise ValueError(f"Invalid key_type: {key_type}")
    
    def get_key_status(self) -> Dict:
        """
        Get status of all keys for diagnostic purposes.
        
        Returns:
            Dict with key existence and metadata
        """
        status = {
            'wg_controller': {
                'private_key_exists': self.WG_CONTROLLER_PRIVATE_KEY.exists(),
                'public_key_exists': self.WG_CONTROLLER_PUBLIC_KEY.exists(),
                'path': str(self.WG_CONTROLLER_PRIVATE_KEY)
            },
            'wg_tunnel': {
                'private_key_exists': self.WG_TUNNEL_PRIVATE_KEY.exists(),
                'public_key_exists': self.WG_TUNNEL_PUBLIC_KEY.exists(),
                'path': str(self.WG_TUNNEL_PRIVATE_KEY)
            },
            'blockchain': {
                'private_key_exists': self.BLOCKCHAIN_PRIVATE_KEY.exists(),
                'public_key_exists': self.BLOCKCHAIN_PUBLIC_KEY.exists(),
                'path': str(self.BLOCKCHAIN_PRIVATE_KEY)
            }
        }
        
        # Load metadata if available
        if self.KEY_METADATA.exists():
            with open(self.KEY_METADATA, 'r') as f:
                metadata = json.load(f)
                for key_type, info in metadata.items():
                    if key_type in status:
                        status[key_type]['created_at'] = info.get('created_at')
        
        return status

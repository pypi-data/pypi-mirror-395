"""Module: Minion"""

import json
import secrets
import time
import hashlib
from datetime import datetime, timedelta

import jwt
import requests
from .utils import run_command
import textwrap
import os
from pathlib import Path

from loguru import logger as log
from tenacity import (
    retry,
    wait_fixed,
    stop_after_delay,
    retry_if_exception_type,
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

MINION_CONFIG_PATH = "/etc/salt/minion"
SYSTEMD_OVERRIDE_DIR = "/etc/systemd/system/salt-minion.service.d"
SYSTEMD_OVERRIDE_FILE = os.path.join(SYSTEMD_OVERRIDE_DIR, "restart.conf")

MINION_CONFIG_BLOCK = textwrap.dedent("""
    #-- wireguard salt auto-recovery start --
    reconnection_backoff: True
    random_reconnect_delay: True
    tcp_keepalive: True
    tcp_keepalive_idle: 30
    tcp_keepalive_interval: 10
    tcp_keepalive_count: 3
    #-- wireguard salt auto-recovery end --
""")

SYSTEMD_OVERRIDE_CONTENT = textwrap.dedent("""
    [Service]
    Restart=always
    RestartSec=5
"""
    )
class Minion:
    """Class: Minion, required environment and secret key"""

    def __init__(self):
        # self.environment = environment
        self.request_url = self.get_nodecontrol_url()
        self.pub_key = None
        self.priv_key = None
            
    def append_or_replace_block(self, file_path, marker_start, marker_end, block_content):
        """Insert or replace a marked block in a file."""
        path = Path(file_path)
        if not path.exists():
            path.write_text(block_content)
            return

        text = path.read_text()
        if marker_start in text and marker_end in text:
            pre = text.split(marker_start)[0]
            post = text.split(marker_end)[1]
            new_text = pre + block_content + post
        else:
            new_text = text.strip() + "\n" + block_content

        path.write_text(new_text)


    def ensure_systemd_override(self):
        os.makedirs(SYSTEMD_OVERRIDE_DIR, exist_ok=True)
        with open(SYSTEMD_OVERRIDE_FILE, "w") as f:
            f.write(SYSTEMD_OVERRIDE_CONTENT)


    def restart_services(self):
        try:
            run_command(['pkill', '-f', 'salt-minion'], name='salt-minion')
            log.debug("Killed existing salt-minion processes")
        except RuntimeError:
            log.debug("No existing salt-minion processes found to kill")
        time.sleep(1)
        run_command(["systemctl", "daemon-reexec"])
        run_command(["systemctl", "daemon-reload"])
        run_command(["systemctl", "restart", "salt-minion"])
      

    def configure_salt_minion_wireguard(self):
        """
        This configuration is used to fix the timeout issue with salt-minion under wireguard. 
        The salt-minion maintains a persistent ZeroMQ connection to the salt-master. 
        If the WireGuard tunnel goes down temporarily, the connection is broken and does not automatically recover in some cases. 
        You then get timeouts or stuck minions until a restart. """
        
        
    def get_nodecontrol_url(self):
        """
        The get_nodecontrol_url function returns the URL of the nodecontrol server based on environment.
        If the environment is prod, it will return https://portal.usdatanetworks.com, otherwise it
        will return https://stage-vmanage.usdatanetworks.com

        :param self: Represent the instance of the class
        :return: A string
        :doc-author: Phan Dang
        """
        # if self.environment == "dev":
        #     return "https://nodecontrol-stage.usdatanetworks.com"
        # elif self.environment == "local":
        #     return "http://localhost:8000"
        return "https://vmanage.usdatanetworks.com"

    @retry(
        wait=wait_fixed(15),
        stop=stop_after_delay(300),  # Stop after 300 seconds (5 minutes)
        retry=retry_if_exception_type(
            requests.RequestException
        ),  # Retry on request exceptions
    )
    def join_salt_master(self, url, jwt_token):
        log.debug(f"Using token: {jwt_token}")
        response = requests.post(
            url,
            data={"token": jwt_token},
        )
        if not response.ok:
            log.error(f"Joining salt master failed! Response: {response.text}")
            log.error("Will restart salt-minion and try again...")
            run_command(["systemctl", "restart", "salt-minion"], name="salt-minion")
            log.debug("Retrying to join salt master after 15s...")
            raise requests.RequestException(
                f"Joining salt master failed! Response: {response.text}"
            )
        log.info("Minion has joined salt master! Minion service completed!")
        log.debug("Writing salt-minion configuration to /etc/salt/minion.d/...")
        self.append_or_replace_block(
            MINION_CONFIG_PATH,
            "#-- wireguard salt auto-recovery start --",
            "#-- wireguard salt auto-recovery end --",
            MINION_CONFIG_BLOCK,
        )
        log.info("Salt-minion configuration updated successfully!")
        self.ensure_systemd_override()
        log.info("Systemd override for salt-minion created successfully!")
        self.restart_services()
        log.info("Salt-minion service restarted successfully!")
        log.debug("Minion has successfully joined the salt master.")
        
        return response

      
    def send_authenticated_request(self, payload, blockchain_private_key):
        """
        Send device registration request with cryptographic signature.
        
        Security Model:
        1. Device signs payload with its blockchain private key (RSA signature)
        2. Backend verifies signature using the blockchain public key in payload
        3. This proves:
           - Device possesses the private key corresponding to public key
           - Payload hasn't been tampered with
           - Request authenticity (not replay if nonce checked)
        
        Args:
            payload: Registration data including public keys
            blockchain_private_key: Device's blockchain private key (PEM)
        
        Returns:
            bool: True if registration successful
        """
        try:
            # Add timestamp and nonce for replay protection
            payload_with_meta = {
                **payload,
                'timestamp': datetime.utcnow().isoformat(),
                'nonce': secrets.token_urlsafe(32)
            }
            
            # Serialize payload for signing
            payload_json = json.dumps(payload_with_meta, sort_keys=True)
            payload_bytes = payload_json.encode('utf-8')
            
            # Load private key
            private_key = serialization.load_pem_private_key(
                blockchain_private_key.encode('utf-8'),
                password=None,
                backend=default_backend()
            )
            
            # Sign the payload with device's blockchain private key
            signature = private_key.sign(
                payload_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            # Convert signature to hex for transmission
            signature_hex = signature.hex()
            
            log.info("Signing registration payload with device blockchain private key...")
            log.debug(f"Payload hash: {hashlib.sha256(payload_bytes).hexdigest()[:20]}...")
            log.debug(f"Signature: {signature_hex[:40]}...")
            
            # Create JWT with signed payload
            jwt_payload = {
                'data': payload_with_meta,
                'signature': signature_hex
            }
            
            jwt_token = jwt.encode(
                payload=jwt_payload,
                key=secrets.token_urlsafe(32),  # Random key (backend doesn't verify JWT, just transports data)
                algorithm="HS256"
            )
            
            url = self.request_url + "/api/v1/devices/add/"
            log.info(f"Sending authenticated registration to {url}")
            
            response = self.join_salt_master(url, jwt_token)
            return True
            
        except Exception as e:
            log.error(f"Failed to send authenticated request: {e}", exc_info=True)
            return False

    def send_request(self, encrypted_text):
        """
        DEPRECATED: Old registration method using shared PGP key.
        Use send_authenticated_request() instead.
        """
        log.warning(
            "send_request() is DEPRECATED. "
            "Use send_authenticated_request() with device-specific signature."
        )
        return None

    def pgp_encrypt_data(self, payload, public_key):
        """
        DEPRECATED: PGP encryption using shared key is insecure.
        Use send_authenticated_request() instead.
        
        This method is kept for backward compatibility but logs a warning.
        """
        log.warning(
            "pgp_encrypt_data() is DEPRECATED and insecure (shared key across devices). "
            "Use send_authenticated_request() with device-specific signature instead."
        )
        return None

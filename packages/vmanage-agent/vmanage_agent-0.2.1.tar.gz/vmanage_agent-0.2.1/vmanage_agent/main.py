#!/usr/bin/python
"""Module run main functionality"""
import argparse
import os
import sys
from loguru import logger as log
from .minion import Minion
from .key_manager import KeyManager
from .utils import (
    check_hostname,
    get_system_serial_number,
    get_version,
    check_saltminion_service,
    normalize_hostname,
    run_command,
    set_hostname,
    get_public_ip,
)

ERROR_MARK = " \033[1;31m✖\033[0m "
SUCCESS_MARK = " \033[1;32m✔\033[0m "

LOG_PATH = "/var/log/vmanage-agent.log"

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{function}</cyan>:<cyan>{message}</cyan>"
)
log.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "level": "DEBUG",
            "format": log_format,
        },
        {
            "sink": LOG_PATH,
            "level": "DEBUG",
            "rotation": "10 MB",
            "format": log_format,
        },
    ]
)


def run():
    """
    The run function is the entry point for this module.
    It will be called by the minion service when it starts up.
    The run function should return a dictionary with keys:

    :return: Whether minion is successfully joined the salt master
    :doc-author: Phan Dang
    """
    if not os.getuid() == 0:
        log.error("You need to have root privileges to run this script. Exiting.")
        sys.exit(-1)

    # print out vmanage agent version
    version = get_version()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Vmanage-agent version {version}. Developed by US Data Networks. All rights reserved.",
        help="Show minion version",
    )

    parser.add_argument("-m", "--master", help="Salt master address.")

    parser.add_argument(
        "-mf", "--master-finger", help="Salt master finger to verify master."
    )

    parser.add_argument(
        "-e",
        "--env",
        default="production",
        choices=["production", "staging"],
        help="Environment (production or staging). Defaults to production."
    )

    config_namespace = argparse.Namespace()
    args = parser.parse_args(namespace=config_namespace)

    if not args.master:
        raise RuntimeError("Salt master address is required! Please add -m <master>")

    if not args.master_finger:
        raise RuntimeError(
            "Salt master finger is required! Please add -mf <master_finger>"
        )
    log.info("Checking salt-minion service...")
    check_saltminion_service()

    raw_serial = get_system_serial_number()
    hostname = normalize_hostname(raw_serial)
    log.info(f"This nodes serial number is: {hostname}")
    fqdn = hostname + ".usdatanetworks.com"
    log.info(f"Setting fqdn to {fqdn}")
    set_hostname(fqdn)
    check_hostname(fix_etc_hosts=True)

    log.debug("Writing saltmaster config to /etc/salt/minion.d/...")

    with open("/etc/salt/minion.d/id.conf", "w") as id_file:
        id_file.write("id: " + hostname)

    with open("/etc/salt/minion.d/master.conf", "w") as master_file:
        master_file.write("master: " + args.master + "\n")
        master_file.write("master_finger: " + args.master_finger)

    log.info("Restarting salt-minion service...")
    run_command(["systemctl", "restart", "salt-minion"], name="salt-minion")
    log.info("Salt-minion service restarted!")
    log.info("Now attempting to join salt master...")
    minion = Minion(environment=args.env)
    
    # Initialize key manager
    log.info("Initializing cryptographic keys...")
    key_manager = KeyManager()
    
    # Generate all three key types
    all_keys = key_manager.initialize_all_keys()
    
    # Extract public keys for registration (NEVER send private keys!)
    wg_controller_public = all_keys['wg_controller'][1]
    wg_tunnel_public = all_keys['wg_tunnel'][1]
    blockchain_public = all_keys['blockchain'][1]
    
    log.info("✓ All cryptographic keys initialized successfully!")
    log.debug(f"Controller WG public key: {wg_controller_public[:20]}...")
    log.debug(f"Tunnel WG public key: {wg_tunnel_public[:20]}...")
    log.info(f"Public IP: {get_public_ip()}")

    # Prepare registration payload with PUBLIC keys only
    registration_payload = {
        "serial_number": raw_serial,
        "hostname": hostname,
        "master": args.master,
        "master_finger": args.master_finger,
        "wireguard_controller_public_key": wg_controller_public,
        "wireguard_tunnel_public_key": wg_tunnel_public,
        "blockchain_public_key": blockchain_public,
        "public_ip": get_public_ip(),
    }
    
    # Get blockchain private key to sign the request (proves device authenticity)
    blockchain_private = all_keys['blockchain'][0]
    
    # Send authenticated request
    success = minion.send_authenticated_request(
        registration_payload,
        blockchain_private_key=blockchain_private
    )
    if not success:
        log.error("Device registration failed!")
        sys.exit(-1)

    log.info("vmanage-agent run completed!")

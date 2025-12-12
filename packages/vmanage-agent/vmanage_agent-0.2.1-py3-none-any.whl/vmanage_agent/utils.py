"""Utility functions"""

import configparser
import json
import subprocess
from gettext import gettext as _
from cryptography.fernet import Fernet
import subprocess
import requests

from loguru import logger as log


def run_command(args, env=None, name=None):
    """Run the command defined by args and return its output

    :param args: List of arguments for the command to be run.
    :param env: Dict defining the environment variables. Pass None to use
        the current environment.
    :param name: User-friendly name for the command being run. A value of
        None will cause args[0] to be used.
    """

    if name is None:
        name = args[0]
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, env=env)
        if isinstance(output, bytes):
            output = output.decode("utf-8")
        return output
    except subprocess.CalledProcessError as e:
        message = f"{name} failed: {e.output}"
        log.error(message)
        raise RuntimeError(message)


def run_command_and_log(cmd, cwd=None, env=None, retcode_only=True):
    """Run command and log output

    :param cmd: command in list form
    :type cmd: List

    :param cwd: current worknig directory for execution
    :type cmd: String

    :param env: modified environment for command run
    :type env: List

    :param retcode_only: Returns only retcode instead or proc objec
    :type retcdode_only: Boolean
    """
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        cwd=cwd,
        env=env,
    )
    if retcode_only:
        while True:
            try:
                line = proc.stdout.readline()
            except StopIteration:
                break
            if line != b"":
                if isinstance(line, bytes):
                    line = line.decode("utf-8")
                log.warning(line.rstrip())
            else:
                break
        proc.stdout.close()
        return proc.wait()
    else:
        return proc


def check_salt_master_connection(master_finger):
    """
    Check connection to salt master
    """
    pass


def check_saltminion_service():

    try:
        run_command(
            ["systemctl", "is-active", "--quiet", "salt-minion"], name="salt-minion"
        )
        log.info("Salt-minion service is running!")

    except RuntimeError as _:
        log.error(
            "Salt-minion not install and/or its service is not installed!",
            exc_info=True,
        )

def normalize_hostname(serial):
    """
    Normalize serial number to valid hostname format:
    - Convert to lowercase
    - Replace special characters with hyphens
    - Handle cloud provider specific formats
    - Ensure uniqueness is maintained
    - Keep length reasonable (max 63 chars for valid DNS)
    """
    import re
    
    # Convert to lowercase
    serial = serial.lower()
    
    # Check for AWS-style UUID
    if re.match(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', serial):
        # Extract first 8 chars and last 12 chars to maintain uniqueness
        return f"aws-{serial[:8]}-{serial[-12:]}"
    
    # Check for Azure-style serial with many hyphens
    if serial.count('-') > 4:
        # Remove all hyphens and take first 16 chars
        clean = serial.replace('-', '')
        return f"az-{clean[:16]}"
    
    # For other serial numbers, replace invalid chars with hyphens
    clean = re.sub(r'[^a-z0-9-]', '-', serial)
    
    # Replace multiple hyphens with single hyphen
    clean = re.sub(r'-+', '-', clean)
    
    # Trim leading/trailing hyphens
    clean = clean.strip('-')
    
    # Limit length to 63 chars max (DNS standard)
    if len(clean) > 59:
        clean = clean[:59]
    
    return clean
def get_system_serial_number():
    """
    The get_system_serial_number function is used to find and return the serial number of the local machine.
    The function uses a system command to get the serial number from dmidecode, which is a tool for dumping
    a computer's DMI (some say SMBIOS) table contents in human-readable format. This table contains a description
    of the system's hardware components, as well as other useful pieces of information such as serial numbers
    and BIOS revision.

    :param self: Represent the instance of the class
    :return: The serial number of the local machine
    """

    args = ["sudo", "dmidecode", "-s", "system-serial-number"]
    serial_number = run_command(args, name="dmidecode")

    if isinstance(serial_number, str):
        return serial_number.strip()
    log.error("Unable to get serial number from the device!")
    return None


def write_to_file(location: str, val: str):
    """
    The write_to_file function writes a string to a file.

    :param location: str: Specify the location of the file to be written
    :param val: str: Pass in the value that is to be written to the file
    :return: None
    :doc-author: Phan Dang
    """

    with open(location, "w", encoding="utf-8") as pub_file:
        pub_file.write(val)
        pub_file.close()


def get_short_hostname():
    """Returns the local short hostname

    :return string
    """
    p = subprocess.Popen(
        ["hostname", "-s"], stdout=subprocess.PIPE, universal_newlines=True
    )
    return p.communicate()[0].rstrip().lower()


def get_version():
    """Returns the version of the vmanage-agent

    :return string
    """
    return "vmanage-agent-0.1.0"  # Placeholder version, replace with actual version retrieval logic


def set_hostname(hostname):
    """Set system hostname to provided hostname

    :param hostname: The hostname to set
    """
    args = ["sudo", "hostnamectl", "set-hostname", hostname]
    log.debug(f"Running command: {' '.join(args)}")
    return run_command(args, name="hostnamectl")


def decrypt_token(encrypted_message, key):
    """
    Decrypts an encrypted message
    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return json.loads(decrypted_message.decode())


def check_hostname(fix_etc_hosts=True):
    """Check system hostname configuration

    Rabbit and Puppet require pretty specific hostname configuration. This
    function ensures that the system hostname settings are valid before
    continuing with the installation.

    :param fix_etc_hosts: Boolean to to enable adding hostname to /etc/hosts
        if not found.
    """
    log.info("Checking for a FQDN hostname...")
    args = ["hostnamectl", "--static"]
    detected_static_hostname = run_command(args, name="hostnamectl").rstrip()
    log.debug(f"Static hostname detected as {detected_static_hostname}")
    args = ["hostnamectl", "--transient"]
    detected_transient_hostname = run_command(args, name="hostnamectl").rstrip()
    log.debug(
        f"Transient hostname detected as {detected_transient_hostname}",
        detected_transient_hostname,
    )
    if detected_static_hostname != detected_transient_hostname:
        log.error(
            f"Static hostname {detected_static_hostname} does not match transient hostname {detected_transient_hostname} "
        )
        log.error("Use hostnamectl to set matching hostnames.")
        raise RuntimeError("Static and transient hostnames do not match")
    short_hostname = detected_static_hostname.split(".")[0]
    log.debug(f"Short hostname detected as {short_hostname}")
    if short_hostname == detected_static_hostname:
        message = _("Configured hostname is not fully qualified.")
        log.error(message)
        raise RuntimeError(message)
    with open("/etc/hosts") as hosts_file:
        for line in hosts_file:
            # check if hostname is in /etc/hosts
            if (
                not line.lstrip().startswith("#")
                and detected_static_hostname in line.split()
            ):
                break
        else:
            # hostname not found, add it to /etc/hosts
            log.warning(f"Hostname {detected_static_hostname} not found in /etc/hosts")
            if not fix_etc_hosts:
                return
            sed_cmd = (
                r'sed -i "s/127.0.0.1\(\s*\)/127.0.0.1\\1%s %s /" '
                "/etc/hosts" % (detected_static_hostname, short_hostname)
            )
            args = ["sudo", "/bin/bash", "-c", sed_cmd]
            run_command(args, name="hostname-to-etc-hosts")
            log.info(f"Added hostname {detected_static_hostname} to /etc/hosts")


def read_ini(file_path):
    """Read config ini"""
    obj = {}
    config = configparser.ConfigParser()
    config.read(file_path)
    for section in config.sections():
        for key in config[section]:
            obj[key] = config[section][key]
    return obj


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        ip = response.json().get("ip")
        return ip
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None


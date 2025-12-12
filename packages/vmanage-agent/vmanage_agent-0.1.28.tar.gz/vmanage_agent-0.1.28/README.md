# Table of Contents

-----------------

* [Overview](#overview)
* [Requirements](#requirements)
* [Installation](#installation)
* [Pre-requisites](#pre-requisites)
* [Usage](#usage)
* [File Location](#file-location)
* [Contributing](#contributing)
* [License](#license)

## Overview

Module ***vmanage-agent*** allows **node** to make request to vmanage and add this device to USDN system.

### Enhanced Security Features

The agent now implements **three separate cryptographic key types** for maximum security:

1. **Controller WireGuard Keys** - Management plane (node ↔ controller)
2. **Tunnel WireGuard Keys** - Data plane (node ↔ node via VPP)  
3. **Blockchain RSA Keys** - Configuration encryption/decryption

**Security Guarantee**: Private keys NEVER leave the device. Only public keys are transmitted to backend.

See [SECURITY_KEY_MANAGEMENT.md](./SECURITY_KEY_MANAGEMENT.md) for complete details.

## Requirements

Make sure python and the package manager [pip](https://pip.pypa.io/en/stable/) are installed. Salt-minion >= 3005.1 is also required.

* [python][python] >=3.10
* [pip][pip] >= 3.10
* [salt-minion][salt-minion] == 3005.1

## Installation


Install package with the command below:

```bash
sudo pip3 install https://usdn-repo-bucket.s3.amazonaws.com/vmanage-agent/vmanage_agent-latest.tar.gz 
```

## Pre-requisites

### Salt-minion is running

Checking if salt-minion is running

```bash
sudo systemctl status salt-minion
```

If the output return error, try to stop salt-minion and run in debug mode (salt-minion -l debug)


## Usage

### Run manually

```bash
sudo  /usr/local/bin/vmanage-agent -m [master-address] -mf [master-fingerprint]
```

### File Location

* *Log*: /var/log/minion.log
* *Config*: /opt/minion/config.ini

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[US Data Networks](https://usdatanetworks/docs/license)

[python]: https://www.python.org/downloads/release/python-380/
[pip]:https://pip.pypa.io/en/stable/installation/
[salt-minion]:https://docs.saltproject.io/salt/install-guide/en/latest/topics/bootstrap.html#install-bootstrap


2023-03-14
==========

Removed
-------

- Unused dependencies
- remove loguru as log manager

Changed
-------

- Formatting

Security
--------

- Remove pinned cryptography

2022-12-09
==========

Removed
-------

- Dependencies on config file. Config file must be created manually.

Added
-----

- Minion service

Changed
-------

- Change salt-minion config from /etc/salt/minion/minion.d/master.conf to /etc/salt/minion

Deprecated
----------

- Cryptography Deprecated v37

2022-10-25
==========

Removed
-------

- config.ini: MASTER section removed. Salt master config is assumed to exist beforehand.

Added
-----

- verbose mode: -v --verbose to enable debug mode

Changed
-------

- nodecontrol API endpoint

Deprecated
----------

- Crytography 37.0.0 is deprecated but used as a required dependency for pgpy. Looking for an option to upgrade in future.

2022-10-17
==========

Changed
-------

- User master public fingerprint intead of minion to ensure integrity
- Remove salt-key get local key

2022-10-05
==========

### Security
------------

- Remove public and private key return as payload

### Fixed
---------

- Update main module with a new methodology
- Remove system module

2022-09-29
==========

### Changed
- update README.md
- update Gitlab CI/CD

### Fixed
- When private key and public key not generated it should exit gracefully and notify user.

2022-09-28
==========

### Added
- Refactor code and prepare to publish to pip package

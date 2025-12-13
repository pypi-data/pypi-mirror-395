# check_ldap_ppolicy_lockout

## Overview

This is Nagios plugin to check for LDAP accounts, which have been
locked by the ppolicy overlay due to too many failed login attempts.

## Installation

Best install the plugin in a virtual environment, e.g.:

```shell
python -m venv /usr/local/lib/check_ldap_ppolicy_lockout
. /usr/local/lib/check_ldap_ppolicy_lockout/bin/activate
pip install check_ldap_ppolicy_lockout
ln -s $(which check_ldap_ppolicy_lockout) /usr/lib/nagios/plugins/check_ldap_ppolicy_lockout
```

## Configuration

Configuration is loaded from `~/.check_ldap_ppolicy_lockout.yaml`
or as fallback from `/etc/check_ldap_ppolicy_lockout.yaml`. This
behaviour may be overruled via the -f command line option.
The following parameters are supported with the defaults shown
for the optional parameters:

```yaml
alarms:
  warning: 1
  critical: 5
  expire_seconds: 600
ldap:
  uri: ldap://localhost  # Required
  binddn: cn=nagios,ou=services,dc=example,dc=com  # Required
  bindpw: xxx  # Required
  tls: true
  tls_ca_file: /etc/ssl/certs/ldap_ca.crt  # Required if ldap.tls is true
  users_base_dn: ou=users,dc=example,dc=com  # Required
```

## Usage

```shell
usage: check_ldap_ppolicy_lockout [-h] [-f CONFIG_FILE] [-w WARNING] [-c CRITICAL] [-e EXPIRE_SECONDS]

Check for user accounts locked by LDAP ppolicy overlay

options:
  -h, --help            show this help message and exit
  -f, --config-file CONFIG_FILE
                        Path to configuration file
  -w, --warning WARNING
                        Number of locked users to trigger warning (Default 1).
  -c, --critical CRITICAL
                        Number of locked users to trigger critical alert (Default 5)
  -e, --expire-seconds EXPIRE_SECONDS
                        Seconds after which locks expire (Default 300 - should match your ppolicy lockout-time)```

## Remarks

For AD installations a plugin check_ldap_lockout seems to exist, see also:

* https://nagios.fm4dd.com/plugins/manual/check_ldap_lockout.shtm

A first check suggests that this plugin does not support TLS,
which does not allow an easy adaptation for modern setups.
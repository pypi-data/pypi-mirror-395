from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


class ConfigError(Exception):
    pass


@dataclass
class AlarmConfig:
    warning: int = 1
    critical: int = 5
    expire_seconds: int = 600


@dataclass
class LdapConfig:
    uri: str
    binddn: str
    bindpw: str
    users_base_dn: str
    tls: bool = True
    tls_ca_file: Optional[str] = None


@dataclass
class _MetaConfig:
    config_file: Path


@dataclass
class Config:
    alarms: AlarmConfig
    ldap: LdapConfig
    _meta: _MetaConfig


def load_config(config_file: Optional[Path] = None) -> Config:
    raw, config_file = _load_raw_config(config_file)
    _validate(raw, config_file)

    alarms_data = raw.get("alarms", {})
    ldap_data = raw.get("ldap", {})
    return Config(
        alarms=AlarmConfig(
            warning=alarms_data.get("warning", 1),
            critical=alarms_data.get("critical", 5),
            expire_seconds=alarms_data.get("expire_seconds", 600),
        ),
        ldap=LdapConfig(
            uri=ldap_data["uri"],
            binddn=ldap_data["binddn"],
            bindpw=ldap_data["bindpw"],
            users_base_dn=ldap_data["users_base_dn"],
            tls=ldap_data.get("tls", True),
            tls_ca_file=ldap_data.get("tls_ca_file"),
        ),
        _meta=_MetaConfig(config_file=config_file)
    )


def _load_raw_config(config_file: Optional[Path] = None) -> tuple[dict, Path]:
    if config_file:
        config_paths = [config_file]
    else:
        config_paths = [
            Path.home() / ".check_ldap_ppolicy_lockout.yaml",
            Path("/etc/check_ldap_ppolicy_lockout.yaml"),
        ]
    for path in config_paths:
        if path.exists():
            with open(path) as f:
                try:
                    config_data = yaml.safe_load(f)
                    if config_data is None:
                        raise ConfigError(f"Configuration file {path} is empty")
                except Exception as e:
                    raise ConfigError(f"Failed to load configuration file {path}: {e}") from e
                return dict(config_data), path

    raise ConfigError(
        f"Configuration file not found in any of: {[str(p) for p in config_paths]}"
    )


def _validate(raw: dict, config_file: Path):
    ldap_data = raw.get("ldap", {})
    for field in ["uri", "binddn", "bindpw", "users_base_dn"]:
        if field not in ldap_data:
            raise ConfigError(f"Required configuration parameter 'ldap.{field}' is missing in {config_file}")
    tls = ldap_data.get("tls", True)
    if tls and not ldap_data.get("tls_ca_file"):
        raise ConfigError("Required configuration parameter 'ldap.tls_ca_file' is missing when ldap.tls is true")


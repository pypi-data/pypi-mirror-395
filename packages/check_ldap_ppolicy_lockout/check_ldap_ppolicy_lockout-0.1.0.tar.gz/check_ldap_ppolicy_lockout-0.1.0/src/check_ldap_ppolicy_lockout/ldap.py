from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ldap3 import Connection, Server, Tls, SUBTREE, AUTO_BIND_TLS_BEFORE_BIND
import ssl

from .config import LdapConfig


class LdapError(Exception):
    pass


@dataclass
class LockedUser:
    dn: str
    uid: str
    locked_since: datetime


class Ldap:
    def __init__(self, ldap_config: LdapConfig):
        self._ldap_config = ldap_config
        self._client: Optional[Connection] = None

    def get_locked_users(self) -> list[LockedUser]:
        self._connect()
        try:
            self._client.search(
                search_base=self._ldap_config.users_base_dn,
                search_filter='(pwdAccountLockedTime=*)',
                search_scope=SUBTREE,
                attributes=['uid', 'pwdAccountLockedTime'],
            )
        except Exception as e:
            raise LdapError(f"Failed to query LDAP: {e}") from e
        
        locked_users = []
        for entry in self._client.entries:
            if hasattr(entry, "pwdAccountLockedTime"):
                locked_since = entry.pwdAccountLockedTime.value
                locked_users.append(
                    LockedUser(
                        dn=entry.entry_dn,
                        uid=entry.uid,
                        locked_since=locked_since,
                    ))
        
        return locked_users

    def _connect(self) -> None:
        if self._client is not None:
            return

        try:
            if self._ldap_config.tls:
                tls = Tls(
                    ca_certs_file=self._ldap_config.tls_ca_file,
                    validate=ssl.CERT_REQUIRED,
                    version =ssl.PROTOCOL_TLSv1_2,
                )
                server = Server(self._ldap_config.uri, tls=tls, use_ssl=True)
                auto_bind = AUTO_BIND_TLS_BEFORE_BIND
            else:
                server = Server(self._ldap_config.uri)
                auto_bind = True

            self._client = Connection(
                server,
                user=self._ldap_config.binddn,
                password=self._ldap_config.bindpw,
                auto_bind=auto_bind,
                raise_exceptions=True,
            )
        except Exception as e:
            raise LdapError(f"Failed to connect to LDAP: {e}") from e

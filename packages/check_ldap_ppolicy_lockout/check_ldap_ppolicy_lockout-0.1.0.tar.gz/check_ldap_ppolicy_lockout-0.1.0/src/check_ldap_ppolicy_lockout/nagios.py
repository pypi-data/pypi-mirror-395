import sys
from datetime import datetime, timezone
from enum import Enum

from check_ldap_ppolicy_lockout.config import load_config, Config, ConfigError
from check_ldap_ppolicy_lockout.args import parse_cli_args, merge_cli_args
from check_ldap_ppolicy_lockout.ldap import Ldap, LockedUser, LdapError


class NagiosExitCodes(Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


def main() -> None:
    try:
        args = parse_cli_args()
        base_config = load_config(args.config_file)
        config = merge_cli_args(base_config, args)
        ldap = Ldap(config.ldap)
        locked_users = ldap.get_locked_users()
        recent_locked_users = _filter_locked_users(locked_users, config.alarms.expire_seconds)
        status, message = _get_result(config, recent_locked_users)
    except Exception as e:
        if isinstance(e, ConfigError) or isinstance(e, LdapError):
            status = NagiosExitCodes.UNKNOWN
            message = f"{status.name} {e}"
        else:
            raise
    print(message)
    sys.exit(status.value)


def _filter_locked_users(locked_users: list[LockedUser], expire_seconds: int) -> list[LockedUser]:
    now = datetime.now(timezone.utc)
    recent_locked_users = [
        user for user in locked_users
        if (now - user.locked_since.replace(tzinfo=timezone.utc)).total_seconds() <= expire_seconds
    ]
    return recent_locked_users


def _get_result(config: Config, locked_users: list[LockedUser]) -> tuple[NagiosExitCodes, str]:
    locked_count = len(locked_users)
    status = NagiosExitCodes.OK
    if locked_count >= config.alarms.critical:
        status = NagiosExitCodes.CRITICAL
    elif locked_count >= config.alarms.warning:
        status = NagiosExitCodes.WARNING

    message = _get_message(locked_users)
    statistics = f"locked_users={locked_count};{config.alarms.warning};{config.alarms.critical};0"
    return status, f"{status.name}: {message} | {statistics}"


def _get_message(locked_users: list[LockedUser]) -> str:
    count = len(locked_users)
    if count == 0:
        return "No locked users"
    if count == 1:
        return f"One locked user: {locked_users[0].uid}"

    uids = [user.uid for user in locked_users[:5]]
    message = f"{count} locked user(s)"
    if count <= 5:
        return f"{message}: {', '.join(uids)}"
    else:
        return f"{message}, including: {', '.join(uids)}"


if __name__ == '__main__':
    main()

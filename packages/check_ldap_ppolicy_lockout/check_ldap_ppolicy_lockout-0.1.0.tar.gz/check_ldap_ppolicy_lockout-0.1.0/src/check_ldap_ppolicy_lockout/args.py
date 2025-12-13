import argparse
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .config import Config


@dataclass
class Args:
    config_file: Optional[Path] = None
    warning: Optional[int] = None
    critical: Optional[int] = None
    expire_seconds: Optional[int] = None


def parse_cli_args() -> Args:
    parser = argparse.ArgumentParser(
        description="Check for user accounts locked by LDAP ppolicy overlay"
    )
    parser.add_argument(
        "-f", "--config-file",
        type=Path,
        help=f"Path to configuration file",
    )
    parser.add_argument(
        "-w", "--warning",
        type=int,
        help=f"Number of locked users to trigger warning (Default 1).",
    )
    parser.add_argument(
        "-c", "--critical",
        type=int,
        help=f"Number of locked users to trigger critical alert (Default 5)",
    )
    parser.add_argument(
        "-e", "--expire-seconds",
        type=int,
        help=f"Seconds after which locks expire (Default 300 - should match your ppolicy lockout-time)",
    )

    raw = parser.parse_args()
    return Args(**raw.__dict__)


def merge_cli_args(config: Config, args: Args) -> Config:
    result = deepcopy(config)
    if args.warning is not None:
        result.alarms.warning = args.warning
    if args.critical is not None:
        result.alarms.critical = args.critical
    if args.expire_seconds is not None:
        result.alarms.expire_seconds = args.expire_seconds
    return result

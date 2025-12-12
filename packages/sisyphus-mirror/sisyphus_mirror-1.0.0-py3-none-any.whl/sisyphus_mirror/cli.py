from argparse import SUPPRESS, ArgumentParser
from collections.abc import Sequence
from pathlib import Path

from sisyphus_mirror.checks import is_rsync_rate_limit
from sisyphus_mirror.consts import (
    ARCH_LIST,
    BRANCH_LIST,
    DEFAULT_ARCH,
    DEFAULT_CONF_PATH,
    DEFAULT_CONN_TIMEOUT,
    DEFAULT_EXCLUDE_FILES,
    DEFAULT_HOME_PATH,
    DEFAULT_INCLUDE_FILES,
    DEFAULT_IO_TIMEOUT,
    DEFAULT_RATE_LIMIT,
    DEFAULT_SNAPSHOTS_LIMIT,
    DEFAULT_SOURCE,
)
from sisyphus_mirror.errors import CommandError
from sisyphus_mirror.typedefs import CLIArgsT


def handle_cli_options(
    args: Sequence[str] | None = None,  # for pytest
) -> CLIArgsT:
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--config", type=Path, default=SUPPRESS,
        help=f"Path to TOML configuration file. Defaults: {DEFAULT_CONF_PATH}.",
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true", default=SUPPRESS,
        help="Perform a trial run without making changes.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=SUPPRESS,
        help="Enable verbose mode with detailed output.",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", default=SUPPRESS,
        help=("Enable debug mode."),
    )
    parser.add_argument(
        "-b", "--branch-list", choices=BRANCH_LIST, nargs="*", default=SUPPRESS,
        help="Explicitly defined repository branches.",
    )
    parser.add_argument(
        "-s", "--source-url", default=SUPPRESS,
        help=f"Repository source URL. Defaults: {DEFAULT_SOURCE}.",
    )
    parser.add_argument(
        "-w", "--working-dir", type=Path, default=SUPPRESS,
        help=(
            "Working directory for snapshots and temporary synchronization data. "
            f"Defaults: {DEFAULT_HOME_PATH}."
        ),
    )
    parser.add_argument(
        "-a", "--arch-list", choices=ARCH_LIST, nargs="*", default=SUPPRESS,
        help=f"Target CPU architectures. Defaults: {DEFAULT_ARCH}.",
    )
    parser.add_argument(
        "-I", "--include-files", nargs="*", default=SUPPRESS,
        help=(
            "File patterns to include during synchronization. "
            f"Defaults: {DEFAULT_INCLUDE_FILES}."
        ),
    )
    parser.add_argument(
        "-E", "--exclude-files", nargs="*", default=SUPPRESS,
        help=("File patterns to exclude from synchronization. "
              f"Defaults: {DEFAULT_EXCLUDE_FILES}."),
    )
    parser.add_argument(
        "-S", "--snapshot-limit", type=int, default=SUPPRESS,
        help=(
            "Maximum number of snapshots to keep. Must be >= 1. "
            f"Defaults: {DEFAULT_SNAPSHOTS_LIMIT}."
        ),
    )
    parser.add_argument(
        "-R", "--rate-limit", default=SUPPRESS,
        help=(
            "limit socket I/O bandwidth. "
            f"Defaults: {DEFAULT_RATE_LIMIT}."
        ),
    )
    parser.add_argument(
        "--conn-timeout", type=int, default=SUPPRESS,
        help=(
            "Connection timeout in seconds. "
            f"Defaults: {DEFAULT_CONN_TIMEOUT}."
        ),
    )
    parser.add_argument(
        "--io-timeout", type=int, default=SUPPRESS,
        help=(
            "I/O timeout in seconds. "
            f"Defaults: {DEFAULT_IO_TIMEOUT}."
        ),
    )
    cli_options = vars(parser.parse_args(args))

    snapshot_limit = cli_options.get("snapshot_limit")
    if isinstance(snapshot_limit, int) and snapshot_limit < 1:
        msg = (
            "CLI option -S or --snapshot-limit must be >= 1. "
            f"Got: {snapshot_limit}."
        )
        raise CommandError(msg)

    rate_limit = cli_options.get("rate_limit")
    if isinstance(rate_limit, str) and not is_rsync_rate_limit(rate_limit):
        msg = (
            f'CLI option -R --rate-limit '
            'must be integer (512) or string ("1.5m"). '
            f"Got: {rate_limit}."
        )
        raise CommandError(msg)

    conn_timeout = cli_options.get("conn_timeout")
    if isinstance(conn_timeout, int) and conn_timeout < 0:
        msg = (
            "CLI option --conn-timeout must be >= 0. "
            f"Got: {conn_timeout}."
        )
        raise CommandError(msg)

    io_timeout = cli_options.get("io_timeout")
    if isinstance(io_timeout, int) and io_timeout < 0:
        msg = (
            "CLI option --io-timeout must be >= 0. "
            f"Got: {io_timeout}."
        )
        raise CommandError(msg)

    return cli_options  # type: ignore[return-value]

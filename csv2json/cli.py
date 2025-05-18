from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TimeRemainingColumn
from tabulate import tabulate

from .core import convert, detect_encoding

console = Console()

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="csv2json",
        description="Convert CSV to JSON with optional filtering",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    p.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Input CSV file path",
        metavar="FILE",
    )

    p.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Output JSON file path",
        metavar="FILE",
    )

    p.add_argument(
        "--indent",
        "-n",
        type=int,
        default=2,
        help="Indentation level for JSON output",
        metavar="N",
    )

    p.add_argument(
        "--filter",
        "-f",
        type=str,
        help="Filter expression (e.g., 'age > 30')",
        metavar="EXPR",
    )

    p.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print JSON output before conversion",
    )

    p.add_argument(
        "--progress",
        action="store_true",
        help="Show progress bar during conversion",
    )

    p.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="-v for INFO, -vv for DEBUG",
    )

    return p


def _setup_logging(level: int) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def _show_preview(csv_path: Path, rows: int = 5) -> None:
    import itertools

    enc = detect_encoding(csv_path)
    with csv_path.open(encoding=enc, newline="") as f:
        reader = csv.DictReader(f)
        sample = list(itertools.islice(reader, rows))  # max rows safely

    if not sample:
        console.print("No data found in the CSV file.", style="bold red")
        return

    table = tabulate(
        sample,
        headers="keys",
        tablefmt="fancy_grid",
    )
    console.print(table)
    console.print(
        f"Rows: {len(list(sample))} | {enc} | " f"Size: {csv_path.stat().st_size} B",
        style="bold cyan",
    )


def _convert_with_progress(src: Path, dst: Path, indent: int, expr: str | None) -> None:

    total_bytes = src.stat().st_size

    with Progress(
        SpinnerColumn(),
        "[progress.description]Reading",
        BarColumn(bar_width=None),
        "{task.completed}/{task.total} bytes",
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("read", total=total_bytes)
        convert(
            src=src,
            dst=dst,
            indent=indent,
            expr=expr,
            progress=lambda done, total: progress.update(
                task, completed=done, total=total
            ),
        )


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    level = logging.WARNING - min(args.verbose, 2) * 10
    _setup_logging(level)
    log.debug("args: %s, args")
    log.debug("Input CSV file: %s", args.input)

    try:
        if args.pretty:
            _show_preview(args.input)

        if args.progress:
            _convert_with_progress(
                src=args.input,
                dst=args.output,
                indent=args.indent,
                expr=args.filter,
            )
        else:
            convert(
                src=args.input,
                dst=args.output,
                indent=args.indent,
                expr=args.filter,
            )
        log.info("Conversion completed successfully.")
    except Exception as e:
        log.error("Error during conversion: %s", e)
        if level <= logging.DEBUG:
            log.exception("Exception details")
        sys.exit(1)


if __name__ == "__main__":
    main()

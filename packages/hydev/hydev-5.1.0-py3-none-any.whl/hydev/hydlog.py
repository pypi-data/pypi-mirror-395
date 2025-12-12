#!/usr/bin/env python3

import argparse
import contextlib
import datetime
import json
import os
import select
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import coloredlogs
from humanfriendly.terminal import (
    ansi_wrap,
    enable_ansi_support,
    terminal_supports_colors,
)

try:
    import hyapp.logs as hyapp_logs
except ImportError:

    def serialize_extra(data: dict[str, Any], *args: Any, **kwargs: Any) -> str:
        return json.dumps(data)

    def postprocess_extra(data: str, *args: Any, **kwargs: Any) -> str:
        return data.strip()

else:
    serialize_extra = hyapp_logs.serialize_extra
    postprocess_extra = hyapp_logs.postprocess_extra


LOG_FMT = "%(time)s %(levelname)-5s %(name)s %(message)s%(_extras)s%(exc_info)s"
FMT_FIELDS = {"time", "ts", "levelname", "name", "message", "_extras", "exc_info"}
SKIP_FIELDS = {
    # Can be added to the format if needed:
    "ts",
    "level",
    "hostname",
    "pid",
    "aio_task",
    # Processed into `exc_info`:
    "error",
}
OUTER_KEYS = ["Line"]


def loads_dict(value: bytes | str) -> dict[str, Any]:
    result = json.loads(value)
    if not isinstance(result, dict):
        raise ValueError("Non-dict item")
    return result


def ensure_str(value: bytes | str) -> str:
    if isinstance(value, str):
        return value
    return bytes(value).decode("utf-8", errors="replace")


def ensure_newline(value: str) -> str:
    if value.endswith("\n"):
        return value
    return f"{value}\n"


def preprocess_line(line: bytes | str) -> bytes | str | dict[str, Any]:
    try:
        item = loads_dict(line)
    except Exception:
        return line

    # For handling the systems that wrap the log lines.
    inner_line: str | None = None
    for key in OUTER_KEYS:
        inner_line = item.get(key)
        if inner_line is None:
            continue
        if isinstance(inner_line, (bytes, str)):
            try:
                item = loads_dict(inner_line)
            except Exception:
                return inner_line

    out_item = {**dict.fromkeys(FMT_FIELDS, ""), **item}
    if not item.get("time") and isinstance(item.get("ts"), float):
        out_item["time"] = datetime.datetime.fromtimestamp(item["ts"], datetime.UTC).isoformat().replace("+00:00", "Z")

    extra = {key: val for key, val in item.items() if key not in FMT_FIELDS}
    if extra:
        extra_s = serialize_extra(extra)
        extra_s = postprocess_extra(extra_s)
        # Might or might not have a newline in it.
        out_item["_extras"] = extra_s

    if item.get("exc_info"):
        out_item["exc_info"] = f"\n{item['exc_info']}"

    elif isinstance(item.get("error"), dict):
        out_item["exc_info"] = f"\n{item['error'].get('message') or ''}\n{item['error'].get('stack') or ''}"

    return out_item


class ColoredFormatterHelper:
    log_fmt: str = LOG_FMT

    def __init__(self, out_stream: Any, *, no_color: bool = False, force_color: bool = False) -> None:
        self.no_color = no_color
        self.force_color = force_color
        self.use_colors = self.force_color or (
            not self.no_color and terminal_supports_colors(out_stream) and enable_ansi_support()
        )
        self.coloredlogs_formatter = coloredlogs.ColoredFormatter()
        self.log_fmt_colorized = (
            self.coloredlogs_formatter.colorize_format(self.log_fmt) if self.use_colors else self.log_fmt
        )

    def format(self, data: dict) -> str:
        data = data.copy()
        if self.use_colors:
            style = self.coloredlogs_formatter.nn.get(self.coloredlogs_formatter.level_styles, data["levelname"])
            if style:
                data["message"] = ansi_wrap(data["message"], **style)
        return self.log_fmt_colorized % data


def main_inner(log: Iterable[str], *, no_color: bool = False, force_color: bool = False) -> None:
    out_stream = sys.stdout
    formatter_helper = ColoredFormatterHelper(out_stream=out_stream, no_color=no_color, force_color=force_color)
    for line in log:
        output: str | None = None

        line_proc = preprocess_line(line)
        if not isinstance(line_proc, dict):
            if line_proc:
                output = ensure_str(line)
        else:
            output = formatter_helper.format(line_proc)

        if output:
            out_stream.write(ensure_newline(output))


def _stdin_has_data(timeout_sec: float = 0.05) -> bool:
    stdin_fd = sys.stdin.fileno()  # normally, `0`
    ready, _, _ = select.select([stdin_fd], [], [], timeout_sec)
    return bool(ready)


CLI_PARSER = argparse.ArgumentParser(description="Format `hyapp` json logs for the eyes")
CLI_PARSER.add_argument("source", nargs="?", default="-", help=("File to read (defaults to '-' i.e. read from stdin)"))
CLI_PARSER.add_argument(
    "-C",
    "--color",
    action="store_true",
    help="Force color output regardless of the terminal",
)
CLI_PARSER.add_argument(
    "--no-color",
    action="store_true",
    help="Disable color output regardless of the terminal",
)


def main() -> None:
    params = CLI_PARSER.parse_args(sys.argv[1:])
    filepath = params.source

    with contextlib.ExitStack() as cm:
        if filepath == "-":
            if not _stdin_has_data():
                # Warn when running without parameters and without data ready.
                sys.stderr.write("Reading from stdin...\n")

            fileobj = sys.stdin
        else:
            fileobj = cm.enter_context(Path(filepath).open())

        with contextlib.suppress(KeyboardInterrupt):  # Exit silently on C-c
            main_inner(fileobj, force_color=params.color, no_color=params.no_color or bool(os.environ.get("NO_COLOR")))


if __name__ == "__main__":
    main()

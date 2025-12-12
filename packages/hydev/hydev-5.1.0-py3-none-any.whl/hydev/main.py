from __future__ import annotations

import contextlib
import functools
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import click
import toml

from .utils import TCfg, deep_merge, dumps_configparser, getitem_path, pair_window

if TYPE_CHECKING:
    from collections.abc import Collection, Generator, Sequence

HERE = Path(__file__).parent
DEFAULT_ENCODING = "utf-8"
MAIN_CONFIG = toml.loads((HERE / "common_pyproject.toml").read_text(encoding=DEFAULT_ENCODING))
DEFAULT_UV_RUN_ARGS = ("--group=dev", "--isolated")
ENVWRAP_RERUN_FLAG_KEY = "HYD_ENVWRAP_RERUN_DONE"


class LocalConfigManager:
    def __init__(self, local_config_path: str | Path = "pyproject.toml") -> None:
        self.local_config_path = local_config_path

    @functools.cached_property
    def local_config(self) -> TCfg:
        try:
            config_text = Path(self.local_config_path).read_text(encoding=DEFAULT_ENCODING)
        except FileNotFoundError:
            return {}
        return toml.loads(config_text)

    @functools.cached_property
    def is_poetry(self) -> bool:
        local_config = self.local_config
        try:
            getitem_path(local_config, ("tool", "poetry"))
        except KeyError:
            return False
        return True

    @functools.cached_property
    def is_uv(self) -> bool:
        local_config = self.local_config

        try:
            hydev_uv = getitem_path(local_config, ("tool", "hydev", "uv"))
        except KeyError:
            hydev_uv = False

        if hydev_uv:
            return True

        try:
            build_sys = getitem_path(local_config, ("build-system", "requires"))
        except KeyError:
            build_sys = None

        # A bit of a heuristic; but should be close enough.
        # An alternative to consider: check for "uv" in `project.depedencies`.
        build_backend = str(build_sys[0]) if isinstance(build_sys, list) and len(build_sys) == 1 else ""
        return build_backend.startswith(("hatchling", "uv_build"))

    @functools.cached_property
    def command_run_uv_args(self) -> list[str]:
        local_config = self.local_config
        try:
            args = getitem_path(local_config, ("tool", "hydev", "uv_run_args"))
        except KeyError:
            return list(DEFAULT_UV_RUN_ARGS)
        return ensure_str_list(args, "tool.hydev.uv_run_args")

    @functools.cached_property
    def command_run_prefix(self) -> list[str]:
        if self.is_poetry:
            return ["poetry", "run"]
        if self.is_uv:
            return ["uv", "run", *self.command_run_uv_args, "--"]
        return []


DEFAULT_LOCAL_CONFIG_MGR = LocalConfigManager()


def ensure_str_list(value: Any, context: str) -> list[str]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"Expecting list of strings at {context}, found {type(value)!r}")
    non_strings = [type(item) for item in value if not isinstance(item, str)]
    if not all(isinstance(item, str) for item in value):
        raise ValueError(f"Expecting list of strings at {context}, found non-strings {non_strings!r}")
    return list(value)


def glob_to_re(glob_str: str) -> str:
    return glob_str.replace("\\", r"\\").replace(".", r"\.").replace("*", ".*")


def extend_ignore_paths(config, paths: list[str]):
    cfg_tool = config.get("tool") or {}

    cfg_ruff = cfg_tool.get("ruff") or {}
    cfg_ruff_exclude = cfg_ruff.get("extend-exclude") or []
    assert isinstance(cfg_ruff_exclude, list)

    cfg_isort = cfg_tool.get("isort") or {}
    cfg_isort_skip = cfg_isort.get("skip") or []
    assert isinstance(cfg_isort_skip, list)

    cfg_flake8 = cfg_tool.get("flake8") or {}
    cfg_flake8_exclude = cfg_flake8.get("extend-exclude") or []
    assert isinstance(cfg_flake8_exclude, list)

    cfg_mypy = cfg_tool.get("mypy") or {}
    cfg_mypy_exclude = cfg_mypy.get("exclude") or []
    assert isinstance(cfg_mypy_exclude, list)

    cfg_pytest = cfg_tool.get("pytest") or {}
    cfg_pytest_ini = cfg_pytest.get("ini_options") or {}
    cfg_pytest_exclude = cfg_pytest_ini.get("norecursedirs") or []
    assert isinstance(cfg_pytest_exclude, list)

    paths_re = [glob_to_re(path) for path in paths]

    return {
        **config,
        "tool": {
            **cfg_tool,
            "isort": {**cfg_isort, "skip": [*cfg_isort_skip, *paths]},
            "ruff": {**cfg_ruff, "extend-exclude": [*cfg_ruff_exclude, *paths]},
            "flake8": {**cfg_flake8, "extend-exclude": [*cfg_flake8_exclude, *paths]},
            "mypy": {**cfg_mypy, "exclude": [*cfg_mypy_exclude, *paths_re]},
            "pytest": {**cfg_pytest, "ini_options": {**cfg_pytest_ini, "norecursedirs": [*cfg_pytest_exclude, *paths]}},
        },
    }


class CLIToolBase:
    local_config_mgr: ClassVar[LocalConfigManager] = DEFAULT_LOCAL_CONFIG_MGR

    def run(self) -> None:
        raise NotImplementedError

    @classmethod
    def run_cli(cls) -> None:
        cls().run()


class CommonEnvWrapTool(CLIToolBase):
    """Ensures the tool is running in the current uv/poetry environment"""

    auto_wrap_rerun: ClassVar[bool] = True

    @staticmethod
    def _log(msg: str) -> None:
        # Writing to stderr so that piping the output works correctly.
        click.echo(msg, err=True)

    @classmethod
    def run_cmd(cls, cmd: Sequence[str], env: dict[str, str] | None = None) -> None:
        cmd_s = shlex.join(cmd)
        cls._log(f"Running:    {cmd_s}")
        ret = subprocess.call(cmd, env=env)
        if ret:
            cls._log(f"Command returned {ret}")
            sys.exit(ret)

    @classmethod
    def run_cli(cls) -> None:
        if not cls.auto_wrap_rerun:  # auto-wrap disabled
            super().run_cli()
            return

        if os.environ.get(ENVWRAP_RERUN_FLAG_KEY):  # already wrapped
            super().run_cli()
            return

        config_mgr = cls.local_config_mgr
        command_prefix = config_mgr.command_run_prefix
        if not command_prefix:  # no wrapping specified
            super().run_cli()
            return

        requested_cmd = sys.argv
        # In the `requested_cmd[0]` replace `/path/to/cmd` with `cmd`, to re-resolve the path.
        main_cmd = requested_cmd[0]
        main_cmd = main_cmd.rsplit("/", 1)[-1]
        requested_cmd[0] = main_cmd

        cmd = [*command_prefix, *requested_cmd]
        env = {**os.environ, ENVWRAP_RERUN_FLAG_KEY: "1"}
        cls.run_cmd(cmd, env=env)


class CommonCLITool(CommonEnvWrapTool):
    tool_name: str
    should_add_default_path: bool = False
    ignored_args: frozenset[str] = frozenset(["--check"])
    concatenate_disable_suffix: ClassVar[str] = "__replace"
    concatenated_list_paths: ClassVar[Collection[Sequence[str]]] = (
        # Makes it possible to add more opts to addopts.
        ("tool", "pytest", "ini_options", "addopts"),
        ("tool", "hydev", "ignore_paths"),
    )

    @staticmethod
    def has_positional_args(args: Sequence[str]) -> bool:
        # TODO: a better heuristic.
        for prev_arg, arg in pair_window(["", *args]):
            if arg.startswith("-"):
                # assyme an option
                continue
            if prev_arg.startswith("--"):
                # Assume a value for an option
                continue
            return True
        return False

    @classmethod
    def merge_configs_base(cls, common_config: TCfg, local_config: TCfg) -> TCfg:
        result = deep_merge(common_config, local_config)

        # Merge some lists explicitly (unless disabled).
        # Note: expecting all `concatenated_list_paths` paths to exist
        # in the common config (and, thus, in the merged config).
        for concat_path in cls.concatenated_list_paths:
            assert concat_path, "must be non-empty"
            parent_path = concat_path[:-1]
            key = concat_path[-1]
            skip_marker_key = f"{key}{cls.concatenate_disable_suffix}"

            common_value = getitem_path(common_config, concat_path)
            assert isinstance(common_value, list), f"path {concat_path} must point to a list"

            parent = getitem_path(result, parent_path)
            assert isinstance(parent, dict), f"path {parent_path} must point to a dict"
            if skip_marker_key in parent:
                assert parent[skip_marker_key] is True or parent[skip_marker_key] is False
                parent.pop(skip_marker_key)
                continue

            try:
                local_value = getitem_path(local_config, concat_path)
            except KeyError:
                # No local value, nothing to do.
                continue

            assert isinstance(local_value, list), f"path {concat_path} can only be overridden by a list"
            parent[key] = [*common_value, *local_value]

        return result

    @classmethod
    def merge_configs(cls, common_config: TCfg, local_config: TCfg) -> TCfg:
        result = cls.merge_configs_base(common_config, local_config)
        ignore_paths_raw = getitem_path(result, ("tool", "hydev", "ignore_paths"))
        ignore_paths = ensure_str_list(ignore_paths_raw, "tool.hydev.ignore_paths")
        return extend_ignore_paths(result, ignore_paths)

    @classmethod
    def read_merged_config(
        cls,
        local_path: str | Path = "pyproject.toml",
        common_config: TCfg = MAIN_CONFIG,
    ) -> TCfg:
        local_config = cls.local_config_mgr.local_config
        return cls.merge_configs(common_config, local_config)

    def add_default_path(self, extra_args: Sequence[str], path: str = ".") -> Sequence[str]:
        # A very approximate heuristic: do not add path if any non-flags are present.
        if self.has_positional_args(extra_args):
            return extra_args
        return [*extra_args, path]

    def tool_extra_args(self) -> Sequence[str]:
        return []

    def make_cmd(self, extra_args: Sequence[str] = ()) -> Sequence[str]:
        if self.should_add_default_path:
            extra_args = self.add_default_path(extra_args)
        if self.ignored_args:
            extra_args = [arg for arg in extra_args if arg not in self.ignored_args]

        run_prefix = self.local_config_mgr.command_run_prefix

        return [
            *run_prefix,
            "python",
            "-m",
            self.tool_name,
            *self.tool_extra_args(),
            *extra_args,
        ]

    def run(self) -> None:
        cmd = self.make_cmd(extra_args=sys.argv[1:])
        self.run_cmd(cmd)


class ConfiguredCLITool(CommonCLITool):
    config_flag: str
    config_ext: str = "toml"

    def dumps_config(self, data: dict[Any, Any]) -> str:
        return toml.dumps(data)

    @contextlib.contextmanager
    def merged_config(
        self,
        local_path: str | Path = "pyproject.toml",
        common_config: dict[Any, Any] = MAIN_CONFIG,
    ) -> Generator[Path, None, None]:
        full_config = self.read_merged_config()
        full_config_s = self.dumps_config(full_config)

        target_path = Path(f"./.tmp_config.{self.config_ext}")
        target_path.write_text(full_config_s)

        try:
            yield target_path
        finally:
            target_path.unlink()

    def run(self) -> None:
        with self.merged_config() as config_path:
            config_args = [self.config_flag, str(config_path)]
            cmd = self.make_cmd(extra_args=[*config_args, *sys.argv[1:]])
            self.run_cmd(cmd)


class RuffBase(ConfiguredCLITool):
    ruff_command: str

    tool_name: str = "ruff"
    config_flag: str = "--config"

    def tool_extra_args(self) -> Sequence[str]:
        return [self.ruff_command, *super().tool_extra_args()]

    def dumps_config(self, data: dict[Any, Any]) -> str:
        data_root = data["tool"]["ruff"]
        return super().dumps_config(data_root)


class RuffCheck(RuffBase):
    ruff_command: str = "check"


class RuffFormat(RuffBase):
    ruff_command: str = "format"
    ignored_args: frozenset[str] = ConfiguredCLITool.ignored_args - {"--check"}


class Autoflake(CommonCLITool):
    """
    Note that this wrapper doesn't support common configuration,
    because autoflake doesn't have a `--config` flag,
    so it isn't currently possible to override the extra args this class provides.

    If necessary, this wrapper can be modified use `self.read_merged_config` to
    build the extra args.
    """

    tool_name: str = "autoflake"
    should_add_default_path: bool = True
    ignored_args: frozenset[str] = ConfiguredCLITool.ignored_args - {"--check"}

    def tool_extra_args(self) -> Sequence[str]:
        return [
            "--in-place",
            "--recursive",
            "--ignore-init-module-imports",
            "--remove-all-unused-imports",
            "--quiet",
        ]


class ISort(ConfiguredCLITool):
    tool_name: str = "isort"
    config_flag: str = "--settings"
    should_add_default_path: bool = True
    ignored_args: frozenset[str] = ConfiguredCLITool.ignored_args - {"--check"}


class Black(ConfiguredCLITool):
    tool_name: str = "black"
    config_flag: str = "--config"
    should_add_default_path: bool = True
    ignored_args: frozenset[str] = ConfiguredCLITool.ignored_args - {"--check"}


class Flake8(ConfiguredCLITool):
    tool_name: str = "flake8"
    config_flag: str = "--config"
    config_ext: str = "cfg"  # as in `setup.cfg`

    def dumps_config(self, data: dict[Any, Any]) -> str:
        return dumps_configparser({"flake8": data["tool"]["flake8"]})


class Mypy(ConfiguredCLITool):
    tool_name: str = "mypy"
    config_flag: str = "--config-file"


class Pytest(ConfiguredCLITool):
    tool_name: str = "pytest"
    config_flag: str = "-c"

    def tool_extra_args(self) -> Sequence[str]:
        return ["--doctest-modules"]


class CLIToolWrapper(CommonEnvWrapTool):
    wrapped: tuple[type[CLIToolBase], ...]

    def run(self) -> None:
        for tool in self.wrapped:
            tool.run_cli()


class Format(CLIToolWrapper):
    wrapped: tuple[type[CLIToolBase], ...] = (Autoflake, ISort, RuffFormat)


class Fulltest(CLIToolWrapper):
    wrapped: tuple[type[CLIToolBase], ...] = (*Format.wrapped, RuffCheck, Flake8, Mypy, Pytest)

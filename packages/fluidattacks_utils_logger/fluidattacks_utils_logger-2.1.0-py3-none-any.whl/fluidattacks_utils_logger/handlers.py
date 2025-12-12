import logging
from dataclasses import (
    dataclass,
)
from logging import (
    Handler,
)
from typing import (
    IO,
)

import bugsnag
from bugsnag.handlers import (
    BugsnagHandler,
)
from fa_purity import (
    Cmd,
)
from fluidattacks_core.logging.formatters import (
    ColorfulFormatter,
    CustomJsonFormatter,
)

from fluidattacks_utils_logger.env import (
    Envs,
    current_app_env,
)
from fluidattacks_utils_logger.levels import (
    LoggingLvl,
)


@dataclass(frozen=True)
class LoggingConf:
    app_type: str
    app_version: str
    project_root: str
    auto_capture_sessions: bool
    api_key: str
    release_stage: Envs
    app_name: str


def bug_handler(conf: LoggingConf, min_lvl: LoggingLvl) -> Cmd[Handler]:
    def _action() -> Handler:
        bugsnag.configure(  # type: ignore[no-untyped-call]
            app_type=conf.app_type,
            app_version=conf.app_version,
            project_root=conf.project_root,
            auto_capture_sessions=conf.auto_capture_sessions,
            api_key=conf.api_key,
            release_stage=conf.release_stage.value,
        )
        handler = BugsnagHandler()  # type: ignore[no-untyped-call]
        handler.setLevel(min_lvl.value)
        return handler

    return Cmd.wrap_impure(_action)


def logger_handler_with_env(
    target: IO[str],
    env: Envs,
) -> Cmd[Handler]:
    def _action() -> Handler:
        formatter = CustomJsonFormatter() if env == Envs.PROD else ColorfulFormatter()
        handler = logging.StreamHandler(target)
        handler.setFormatter(formatter)
        return handler

    return Cmd.wrap_impure(_action)


def logger_handler(target: IO[str]) -> Cmd[Handler]:
    return current_app_env().bind(lambda env: logger_handler_with_env(target, env))

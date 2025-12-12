import pathlib
import sys
from typing import Literal

from loguru import logger

DEFAULT_LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSSSSS}</green> | <level>{level: <8}</level> | <level>{message}</level> (<cyan>{name}</cyan>:<cyan>{line}</cyan>)"


def setup_logger(
    log_file_name: str = "",
    log_base_dir: pathlib.Path = pathlib.Path("logs"),
    file_level: Literal["", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "",
    echo_level: Literal["", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    rotation: bool = False,
    retention: str = "7 days",
    log_fmt: str = DEFAULT_LOG_FORMAT,
) -> None:
    """Log to `log_base_dir/log_file_name.YYYY-MM-DD.log` with optional rotation and retention

    Args:
        log_file_name (str): _description_. Defaults to "".
        log_base_dir (pathlib.Path, optional): _description_. Defaults to pathlib.Path("logs").
        file_level (Literal[&quot;&quot;, &quot;DEBUG&quot;, &quot;INFO&quot;, &quot;WARNING&quot;, &quot;ERROR&quot;, &quot;CRITICAL&quot;], optional): _description_. Defaults to "DEBUG".
        echo_level (Literal[&quot;&quot;, &quot;DEBUG&quot;, &quot;INFO&quot;, &quot;WARNING&quot;, &quot;ERROR&quot;, &quot;CRITICAL&quot;], optional): _description_. Defaults to "INFO".
        rotation (bool, optional): _description_. Defaults to False.
        retention (str, optional): _description_. Defaults to "7 days".
        log_fmt (str, optional): _description_. Defaults to DEFAULT_LOG_FORMAT.
    """
    logger.configure(handlers=None)
    all_handlers_cfg: list = []
    # echo handler to stdout/stderr
    if echo_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        echo_handler_cfg = dict(sink=sys.stdout, level=echo_level, format=log_fmt)
        all_handlers_cfg.append(echo_handler_cfg)
    # file handler
    if file_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        if not log_file_name:
            raise ValueError("log_file_name must be specified when file_level is specified")
        if log_file_name.endswith(".log"):
            log_file_name = log_file_name.replace(".log", "")
        log_base_dir.mkdir(parents=True, exist_ok=True)
        if rotation:
            sink_path = log_base_dir / (log_file_name + ".{time:YYYY-MM-DD}" + ".log")
        else:
            sink_path = log_base_dir / (log_file_name + ".log")
        file_handler_cfg = dict(sink=sink_path, level=file_level, format=log_fmt)
        if rotation:
            file_handler_cfg["rotation"] = "00:00"
        if retention:
            file_handler_cfg["retention"] = retention
        all_handlers_cfg.append(file_handler_cfg)
    logger.configure(handlers=all_handlers_cfg)

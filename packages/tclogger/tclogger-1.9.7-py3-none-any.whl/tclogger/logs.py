import functools
import logging

from typing import Literal

from .colors import colored
from .fills import add_fills
from .times import get_now

LOG_METHOD_COLORS = {
    "err": ("error", "red"),
    "erro": ("error", "red"),
    "warn": ("warning", "light_red"),
    "hint": ("info", "light_yellow"),
    "glow": ("info", "black"),
    "note": ("info", "light_magenta"),
    "mesg": ("info", "light_cyan"),
    "file": ("info", "light_blue"),
    "line": ("info", "white"),
    "okay": ("info", "light_green"),
    "success": ("info", "light_green"),
    "fail": ("info", "light_red"),
    "back": ("debug", "light_cyan"),
    "dbug": ("debug", "light_cyan"),
}

LOG_METHOD_BG_COLORS = {
    "glow": "bg_blue",
}


class TCLogstr:
    def __init__(self):
        self.COLORS = {k: v[1] for k, v in LOG_METHOD_COLORS.items()}

    def colored_str(self, msg, method, *args, **kwargs):
        return colored(
            msg,
            color=self.COLORS[method.lower()],
            bg_color=LOG_METHOD_BG_COLORS.get(method, None),
            *args,
            **kwargs,
        )

    def err(self, msg: str = ""):
        return self.colored_str(msg, "err")

    def erro(self, msg: str = ""):
        return self.colored_str(msg, "erro")

    def warn(self, msg: str = ""):
        return self.colored_str(msg, "warn")

    def hint(self, msg: str = ""):
        return self.colored_str(msg, "hint")

    def glow(self, msg: str = ""):
        return self.colored_str(msg, "glow")

    def note(self, msg: str = ""):
        return self.colored_str(msg, "note")

    def mesg(self, msg: str = ""):
        return self.colored_str(msg, "mesg")

    def file(self, msg: str = ""):
        return self.colored_str(msg, "file")

    def line(self, msg: str = ""):
        return self.colored_str(msg, "line")

    def success(self, msg: str = ""):
        return self.colored_str(msg, "success")

    def okay(self, msg: str = ""):
        return self.colored_str(msg, "okay")

    def fail(self, msg: str = ""):
        return self.colored_str(msg, "fail")

    def back(self, msg: str = ""):
        return self.colored_str(msg, "back")

    def dbug(self, msg: str = ""):
        return self.colored_str(msg, "dbug")


logstr = TCLogstr()


class TCLogger(logging.Logger):
    INDENT_METHODS = [
        "indent",
        "set_indent",
        "reset_indent",
        "store_indent",
        "restore_indent",
        "log_indent",
    ]
    LEVEL_METHODS = [
        "set_level",
        "store_level",
        "restore_level",
        "quiet",
        "enter_quiet",
        "exit_quiet",
    ]
    LEVEL_NAMES = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }

    def __init__(
        self,
        name: str = None,
        use_prefix: bool = False,
        use_prefix_ms: bool = False,
        use_prefix_color: bool = False,
        verbose: bool = True,
    ):
        self.name = str(name) if name is not None else "TCLogger"
        self.use_prefix = use_prefix
        self.use_prefix_ms = use_prefix_ms
        self.use_prefix_color = use_prefix_color
        self.verbose = verbose

        super().__init__(self.name)
        self.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        self.addHandler(stream_handler)
        self.log_indent = 0
        self.log_indents = []
        self.log_level = "info"
        self.log_levels = []

    def indent(self, indent=2):
        self.log_indent += indent

    def set_indent(self, indent=2):
        self.log_indent = indent

    def reset_indent(self):
        self.log_indent = 0

    def store_indent(self):
        self.log_indents.append(self.log_indent)

    def restore_indent(self):
        self.log_indent = self.log_indents.pop(-1)

    def set_level(
        self, level: Literal["critical", "error", "warning", "info", "debug"]
    ):
        self.log_level = level
        self.setLevel(self.LEVEL_NAMES[level])
        for handler in self.handlers:
            handler.setLevel(self.LEVEL_NAMES[level])

    def store_level(self):
        self.log_levels.append(self.log_level)

    def restore_level(self):
        self.log_level = self.log_levels.pop(-1)
        self.set_level(self.log_level)

    def quiet(self):
        self.set_level("error")

    def enter_quiet(self, quiet=False):
        if quiet:
            self.store_level()
            self.quiet()

    def exit_quiet(self, quiet=False):
        if quiet:
            self.restore_level()

    def get_prefix_str(self, method: str) -> str:
        """Generate prefix string with timestamp, log level, and logger name."""
        now = get_now()
        if self.use_prefix_ms:
            time_str = (
                now.strftime("%Y-%m-%d %H:%M:%S") + f".{now.microsecond // 1000:03d}"
            )
        else:
            time_str = now.strftime("%Y-%m-%d %H:%M:%S")

        method_upper = method.upper()
        if self.use_prefix_color:
            method_str = logstr.colored_str(method_upper, method)
        else:
            method_str = method_upper

        prefix_str = f"[{time_str}] [{method_str}] [{self.name}] "

        if self.use_prefix and self.use_prefix_color:
            prefix_str = logstr.colored_str(prefix_str, method)

        return prefix_str

    def log(
        self,
        method,
        msg,
        indent=0,
        fill=False,
        fill_side="both",
        end="\n",
        use_prefix: bool = None,
        verbose: bool = None,
        *args,
        **kwargs,
    ):
        verbose = self.verbose if verbose is None else verbose
        if not verbose:
            return

        if type(msg) == str:
            msg_str = msg
        else:
            msg_str = repr(msg)
            quotes = ["'", '"']
            if msg_str[0] in quotes and msg_str[-1] in quotes:
                msg_str = msg_str[1:-1]

        if use_prefix is True or (use_prefix is None and self.use_prefix):
            prefix_str = self.get_prefix_str(method)
        else:
            prefix_str = ""

        level, color = LOG_METHOD_COLORS[method]

        indent_str = " " * (self.log_indent + indent)
        indented_msg = "\n".join(
            [
                prefix_str + indent_str + logstr.colored_str(line, method)
                for line in msg_str.split("\n")
            ]
        )

        if fill:
            indented_msg = add_fills(indented_msg, fill_side=fill_side)

        handler = self.handlers[0]
        handler.terminator = end

        getattr(self, level)(indented_msg, *args, **kwargs)

    def route_log(self, method, msg, *args, **kwargs):
        level, color = LOG_METHOD_COLORS[method]
        # if level is lower (less important) than self.log_level, do not log
        if self.LEVEL_NAMES[level] < self.LEVEL_NAMES[self.log_level]:
            return
        functools.partial(self.log, method, msg)(*args, **kwargs)

    def err(self, msg: str = "", *args, **kwargs):
        self.route_log("err", msg, *args, **kwargs)

    def erro(self, msg: str = "", *args, **kwargs):
        self.route_log("erro", msg, *args, **kwargs)

    def warn(self, msg: str = "", *args, **kwargs):
        self.route_log("warn", msg, *args, **kwargs)

    def glow(self, msg: str = "", *args, **kwargs):
        self.route_log("glow", msg, *args, **kwargs)

    def hint(self, msg: str = "", *args, **kwargs):
        self.route_log("hint", msg, *args, **kwargs)

    def note(self, msg: str = "", *args, **kwargs):
        self.route_log("note", msg, *args, **kwargs)

    def mesg(self, msg: str = "", *args, **kwargs):
        self.route_log("mesg", msg, *args, **kwargs)

    def file(self, msg: str = "", *args, **kwargs):
        self.route_log("file", msg, *args, **kwargs)

    def line(self, msg: str = "", *args, **kwargs):
        self.route_log("line", msg, *args, **kwargs)

    def success(self, msg: str = "", *args, **kwargs):
        self.route_log("success", msg, *args, **kwargs)

    def okay(self, msg: str = "", *args, **kwargs):
        self.route_log("okay", msg, *args, **kwargs)

    def fail(self, msg: str = "", *args, **kwargs):
        self.route_log("fail", msg, *args, **kwargs)

    def back(self, msg: str = "", *args, **kwargs):
        self.route_log("back", msg, *args, **kwargs)

    def dbug(self, msg: str = "", *args, **kwargs):
        self.route_log("dbug", msg, *args, **kwargs)

    class TempIndent:
        def __init__(self, logger: "TCLogger", indent=2):
            self.logger: "TCLogger" = logger
            self.indent = indent

        def __enter__(self):
            self.logger.store_indent()
            self.logger.indent(self.indent)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.logger.restore_indent()

    def temp_indent(self, indent=2):
        return self.TempIndent(self, indent=indent)


logger = TCLogger()


def log_error(mesg: str, error_type: type = ValueError):
    logger.warn(mesg)
    raise error_type(mesg)

import os
import signal

from loguru import logger

SIGNAL_TRANSLATION_MAP = {
    signal.SIGINT: "SIGINT",
    signal.SIGTERM: "SIGTERM",
}


def name_process(name, with_pid: bool = False):
    import os
    import setproctitle

    pid = os.getpid()
    if with_pid:
        setproctitle.setproctitle(f"{name} - {pid}")
    else:
        setproctitle.setproctitle(name)
    return name


def parse_args(args: list[str]):
    parsed = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                value: str | bool | int = args[i + 1]
                if value in ("true", "false"):
                    value = value == "true"
                elif value.isdigit():  # type: ignore[union-attr]
                    value = int(value)
                parsed[key.replace("-", "_")] = value
                i += 2
            else:
                raise ValueError(f"Missing value for argument {args[i]}")
        else:
            raise ValueError(f"Unexpected value without preceding argument: {args[i]}")
    return parsed


class KeyboardInterruptHandler:
    def __init__(self, propagate_to_forked_processes=None):
        """
        Constructs a context manager that suppresses SIGINT & SIGTERM signal handlers
        for a block of code.

        The signal handlers are called on exit from the block.

        Inspired by: https://stackoverflow.com/a/21919644

        :param propagate_to_forked_processes: This parameter controls behavior of this context manager
        in forked processes.
        If True, this context manager behaves the same way in forked processes as in parent process.
        If False, signals received in forked processes are handled by the original signal handler.
        If None, signals received in forked processes are ignored (default).
        """
        self._pid = os.getpid()
        self._propagate_to_forked_processes = propagate_to_forked_processes
        self._sig = None
        self._frame = None
        self._old_signal_handler_map = {}

    def __enter__(self):
        self._old_signal_handler_map = {
            sig: signal.signal(sig, self._handler)
            for sig, _ in SIGNAL_TRANSLATION_MAP.items()
        }

    def __exit__(self, exc_type, exc_val, exc_tb):
        for sig, handler in self._old_signal_handler_map.items():
            signal.signal(sig, handler)

        if self._sig is None:
            return

        self._on_signal(self._sig, self._frame)

    def _on_signal(self, signum, frame):
        if self._sig in self._old_signal_handler_map:
            self._old_signal_handler_map[self._sig](self._sig, self._frame)

    def _handler(self, sig, frame):
        self._sig = sig
        self._frame = frame

        #
        # Protection against fork.
        #
        if os.getpid() != self._pid:
            if self._propagate_to_forked_processes is False:
                logger.debug(
                    f"!!! DelayedKeyboardInterrupt._handler: {SIGNAL_TRANSLATION_MAP[sig]} received; "
                    f"PID mismatch: {os.getpid()=}, {self._pid=}, calling original handler"
                )
                self._on_signal(self._sig, self._frame)
            elif self._propagate_to_forked_processes is None:
                logger.debug(
                    f"!!! DelayedKeyboardInterrupt._handler: {SIGNAL_TRANSLATION_MAP[sig]} received; "
                    f"PID mismatch: {os.getpid()=}, ignoring the signal"
                )
                return
            # elif self._propagate_to_forked_processes is True:
            #   ... passthrough

        logger.debug(
            f"!!! DelayedKeyboardInterrupt._handler: {SIGNAL_TRANSLATION_MAP[sig]} received; delaying KeyboardInterrupt"
        )

from dynapyt.analyses.BaseAnalysis import BaseAnalysis
import logging
import time
import threading
import traceback


def _short_repr(obj, max_len=200):
    try:
        r = repr(obj)
    except Exception:
        r = "<unrepresentable>"
    if len(r) > max_len:
        return r[: max_len - 3] + "..."
    return r


logger = logging.getLogger("dynapyt.analysis.trace")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [DynaPyt] %(levelname)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class Trace(BaseAnalysis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._start_times = {}

    def function_enter(self, dyn_ast, iid, args, name, is_lambda):
        """
        Called when a function is entered.
        Logs name, a short summary of args and records a timestamp to compute
        duration on exit.
        """
        thread_id = threading.get_ident()
        now = time.perf_counter()
        self._start_times.setdefault(thread_id, {}).setdefault(iid, []).append(now)

        args_summary = _short_repr(args)
        src = None
        try:
            filename = getattr(dyn_ast, "filename", None)
            lineno = getattr(dyn_ast, "lineno", None)
            if filename or lineno:
                src = f"{filename or '<unknown>'}:{lineno or '?'}"
        except Exception:
            src = None

        logger.info(f"Entering function: {name} iid={iid} thread={thread_id} is_lambda={is_lambda} src={src} args={args_summary}")

    def function_exit(self, *args):
        """
        Called when a function exits. Attempts to extract (name, ret) and
        log duration if a start time was recorded.
        """
        name = None
        ret = None

        for a in args:
            if isinstance(a, str) and name is None:
                name = a
            elif ret is None:
                ret = a

        if name is None:
            name = "<unknown>"

        thread_id = threading.get_ident()
        duration = None
        try:
            stack = self._start_times.get(thread_id, {}).get(args[0] if args else None)
            if stack and isinstance(stack, list) and stack:
                start = stack.pop()
                duration = time.perf_counter() - start
            else:
                thread_stack = self._start_times.get(thread_id, {})
                for k, v in thread_stack.items():
                    if v:
                        start = v.pop()
                        duration = time.perf_counter() - start
                        break
        except Exception:
            duration = None

        ret_summary = _short_repr(ret)
        if duration is not None:
            logger.info(f"Exiting function: {name} return={ret_summary} duration={duration:.6f}s")
        else:
            logger.info(f"Exiting function: {name} return={ret_summary} duration=<unknown>")

    def function_exception(self, *args):
        """
        Optional hook to capture exceptions if the runtime calls it.
        Accepts flexible arguments and logs the traceback when available.
        """
        try:
            exc = None
            for a in args:
                if isinstance(a, BaseException):
                    exc = a
                    break

            if exc is not None:
                tb = traceback.format_exception(type(exc), exc, exc.__traceback__)
                logger.error(f"Function raised exception: {exc!r}\n{''.join(tb)}")
            else:
                # generic logging of provided args
                logger.error(f"Function raised exception, args={_short_repr(args)}")
        except Exception:
            logger.exception("Error while logging function exception")

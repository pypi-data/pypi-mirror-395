import time as _time
from .logger import logger
from functools import wraps

class Timer:
    """一个用于测量代码执行时间的工具。
    可以作为上下文管理器使用，也可以作为装饰器使用。

    Usage
    -----

    上下文管理器(with 语句) 用法：

        >>> with Timer("My Task"):
        >>>     # 你的代码
        >>>     ...s

    装饰器用法：

        >>> @Timer.decorate
        >>> def your_function(...):
        >>>     ...
        >>>
        >>> your_function()

    手动控制用法：

        >>> timer = Timer("My Task")
        >>> timer.start()
        >>> # 你的代码
        >>> ...
        >>> timer.stop()


    """
    def __init__(self, name: str = None):
        """初始化计时器，可以为计时器命名。

        Parameters
        ----------
        name : str, optional
            记时器的名称，默认为 None。
        """
        self.name = (name + " timer") if name else "Timer"
        self.perf_start = None
        self.proc_start = None


    @staticmethod
    def _time_format(seconds: float) -> str:
        if seconds < 1e-3:
            return f"{seconds * 1e6:.2f} µs"
        elif seconds < 1:
            return f"{seconds * 1e3:.2f} ms"
        elif seconds < 60:
            return f"{seconds:.2f} sec"
        elif seconds < 3600:
            return f"{seconds // 60:.0f} min {seconds % 60:.1f} sec"
        else:
            return f"{seconds // 3600:.0f} hr {(seconds % 3600) // 60:.1f} min"


    def __enter__(self):
        self.perf_start = _time.perf_counter()
        self.proc_start = _time.process_time()
        logger.info(f"{self.name} started.")
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        perf_end = _time.perf_counter()
        proc_end = _time.process_time()
        all_time = perf_end - self.perf_start
        cpu_time = proc_end - self.proc_start
        io_time = all_time - cpu_time
        logger.info(f"{self.name} ended.")
        logger.info(f"{self.name} elapsed time: \n"
                    f"  Total: {self._time_format(all_time)} "
                    f"(CPU: {self._time_format(cpu_time)}, "
                    f"Wait: {self._time_format(io_time)})")

    def start(self):
        """手动启动计时器。"""
        self.__enter__()


    def stop(self):
        """手动停止计时器。"""
        self.__exit__(None, None, None)


    @staticmethod
    def decorate(func):
        """一个计时装饰器，用于测量函数执行时间。

            >>> @Timer.decorate
            >>> def your_function(...):
            >>>     ...

        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Timer(func.__name__):
                return func(*args, **kwargs)
        return wrapper
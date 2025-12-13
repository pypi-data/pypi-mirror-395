from flight_profiler.plugins.server_plugin import ServerQueue

def init_gil_interceptor(
    out_q: ServerQueue,
    take_gil_addr: int,
    drop_gil_addr: int,
    take_threshold: int,
    hold_threshold: int,
    stat_interval: int,
    max_stat_threads: int
) -> None: ...

def deinit_gil_interceptor() -> None: ...

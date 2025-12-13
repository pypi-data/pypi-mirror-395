from typing import Any, Callable, List, Optional

from flight_profiler.plugins.server_plugin import ServerQueue
from flight_profiler.plugins.trace.trace_profiler import TraceProfiler

def set_trace_profile(
    target: Callable[[ServerQueue, List[Any]], Any] | None,
    out_q: ServerQueue,
    interval: int,
    async_func: bool,
    depth: int
) -> TraceProfiler: ...
def remove_trace_profile(profiler: Optional[TraceProfiler]) -> None: ...

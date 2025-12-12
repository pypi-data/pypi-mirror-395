"""A templating system with support for nested dictionary keys with the internal Template class."""

from string import Template
from typing import TYPE_CHECKING, Any

from funcy_bear.sentinels import SentinelDict
from lazy_bear import LazyLoader

if TYPE_CHECKING:
    from collections import ChainMap
    from collections.abc import Mapping
    import re

    from funcy_bear.tools.simple_queue import SimpooQueue
else:
    re = LazyLoader("re")
    ChainMap = LazyLoader("collections").to("ChainMap")
    SimpooQueue = LazyLoader("funcy_bear.tools.simple_queue").to("SimpooQueue")
    Mapping = LazyLoader("collections.abc").to("Mapping")

_sentinel_dict: SentinelDict = SentinelDict()


class DotTemplate(Template):
    """An alternative Template class that checks nested dictionaries for keys in format strings."""

    delimiter = "$"

    def safe_substitute(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        mapping: dict = _sentinel_dict,
        unique_keys: set[str] | None = None,
        queue: SimpooQueue | None = None,
        /,
        **kws,
    ) -> str:
        """Perform a safe substitution, checking nested dictionaries for keys.

        Args:
            mapping: The mapping to use for substitution, defaults to a sentinel to use kws.
            unique_keys: An optional set of unique keys to improve performance.
            queue: An optional SimpooQueue to use for flattening nested dictionaries.
            **kwds: Additional keyword arguments to include in the mapping.

        Returns:
            The resulting string after substitution.
        """
        local_cache: dict | ChainMap = mapping if mapping is not _sentinel_dict else ChainMap(kws, mapping)
        has_nested: bool = has_nested_dicts(local_cache)

        def flatten() -> dict[str, Any]:
            local_queue: SimpooQueue = queue or SimpooQueue()
            flat_cache: dict[str, Any] = {}
            local_queue.put(local_cache)
            while local_queue:
                current: dict[str, Any] = local_queue.get()
                for key, value in current.items():
                    if isinstance(value, dict):
                        local_queue.put(value)
                    if unique_keys is None or key in unique_keys:
                        flat_cache[key] = value
            return flat_cache

        if has_nested:
            local_cache = flatten()

        def convert(mo: re.Match[str]) -> str:
            named: str | None = mo.group("named")
            if named is not None:
                if named in local_cache:
                    return str(local_cache[named])
                return mo.group(0)
            braced: str | None = mo.group("braced")
            if braced is not None:
                if braced in local_cache:
                    return str(local_cache[braced])
                return mo.group(0)
            raise ValueError("Unrecognized named group in pattern", self.pattern)

        return self.pattern.sub(convert, self.template)


def cache_unique(t: Template) -> set[str]:
    """Extract the keys used in the format string.

    Args:
        fmt: The format string.

    Returns:
        A set of keys used in the format string.
    """
    keys: set[str] = set()
    for match in t.pattern.finditer(t.template):
        named: str | None = match.group("named") or match.group("braced")
        if named is not None:
            keys.add(named)
    return keys


def has_nested_dicts(mapping: Mapping) -> bool:
    """Quick check if dict contains any nested dicts."""
    return any(isinstance(v, dict) for v in mapping.values())


# if __name__ == "__main__":
#     import timeit


#     nested_dict = {
#         "msg": "Test message",
#         "level": "INFO",
#         "stack_info": {
#             "filename": "test.py",
#             "caller_function": "test_func",
#             "line_number": 42,
#             "exception": None,
#         },
#         "timestamp": "2025-10-22T15:38:00",
#     }

#     temp = "$timestamp |$level| {$filename|$caller_function|$line_number} $msg"

#     template_str = "$timestamp |$level| {$filename|$caller_function|$line_number} $msg"
#     short_str = "$timestamp |$level| $msg"
#     compiler = FormatCompiler(template_str)

#     def test_first_compile() -> None:
#         """Test the first compilation to measure time including caching overhead."""
#         compiler.compile(**nested_dict)

#     RUNS = 10000
#     first_run_time: float = timeit.timeit(test_first_compile, number=RUNS) / RUNS
#     compiler.compile(**nested_dict)
#     subsequent_run_time: float = timeit.timeit(lambda: compiler.compile(**nested_dict), number=RUNS) / RUNS
#     del compiler
#     new = FormatCompiler(short_str)

#     def test_short_compile() -> None:
#         """Test the compilation of a short template string."""
#         new.compile(**nested_dict)

#     short_run_time: float = timeit.timeit(test_short_compile, number=RUNS) / RUNS
#     new.compile(**nested_dict)
#     short_subsequent_run_time: float = timeit.timeit(lambda: new.compile(**nested_dict), number=RUNS) / RUNS
#     times = [
#         ("First Compile Long", first_run_time),
#         ("Subsequent Compile Long", subsequent_run_time),
#         ("First Compile Short", short_run_time),
#         ("Subsequent Compile Short", short_subsequent_run_time),
#     ]

#     table = Table(title="FormatCompiler Performance Benchmark", show_lines=True)
#     table.add_column("Test Case", justify="left", style="cyan", no_wrap=True)
#     table.add_column("Time (ms)", justify="right", style="magenta")
#     table.add_column("Speedup Multiple", justify="right", style="green")
#     table.add_column("Total Time (s)", justify="right", style="yellow")

#     slowest_time = max(t[1] for t in times)
#     for test_case, time_taken in times:
#         difference = slowest_time / time_taken
#         total_time = time_taken * RUNS
#         table.add_row(
#             test_case,
#             f"{time_taken * 1000:.6f}",
#             f"{difference:.2f}",
#             f"{total_time:.4f}",
#         )
#     console.print(table)

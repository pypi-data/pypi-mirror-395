import inspect
import re
from aocd.get import current_day, get_data, most_recent_year
from collections.abc import Iterator
# from io import StringIO
from itertools import islice
# from prettyprinter import pformat, cpprint
from pprint import pformat
from shutil import get_terminal_size
from textwrap import dedent, indent
from time import perf_counter
from traceback import format_exception

def _get_calling_file_match(match):
    return int(match.group()) if match is not None else None

def solve(*funcs, day=None, year=None, data=None, format_custom_data=True, preview_iterators=8):
    if data is None:
        calling_file = inspect.stack()[1].filename
        year_exp, day_exp = ("{0}(?!.*{0}.*)".format(pattern) for pattern in (r"20\d\d", r"[12]?\d"))
        year_match = re.search(year_exp, calling_file)
        calling_file = re.sub(year_exp, "XXXX", calling_file)
        day_match = re.search(day_exp, calling_file)
        year = year or _get_calling_file_match(year_match) or most_recent_year()
        day = day or _get_calling_file_match(day_match) or current_day()
        data = get_data(year=year, day=day)
    elif format_custom_data:
        data = dedent(data).strip()

    for idx, func in enumerate(funcs):
        func_name = f"Function {idx+1}" if (n:=getattr(func, "__name__", "<")).startswith("<") else n
        time_start = perf_counter()

        try:
            func_output = func(data)
        except Exception as e:
            func_output = e

        time = (perf_counter() - time_start) * 1000
        output_type = type(func_output).__qualname__
        ltitle = f"{func_name} -> {output_type}:  "
        rtitle = f"  [{time:.2f}ms]"
        term_width = get_terminal_size().columns
        width_avail = term_width - len(ltitle+rtitle)

        if preview_iterators and isinstance(func_output, Iterator):
            if preview_iterators is True:
                func_output = tuple(func_output)
            else:
                output_preview = list(islice(func_output, preview_iterators))
                try:
                    next(func_output)
                    output_preview.append("...")
                except StopIteration:
                    pass
                func_output = tuple(output_preview)

        if isinstance(func_output, str) and "\n" in func_output:
            pass
        elif isinstance(func_output, Exception):
            func_output = "".join(format_exception(func_output, limit=-1))
        else:
            # stream = StringIO()
            # cpprint(func_output, stream, compact=True, max_seq_len = 10)
            # func_output = stream.getvalue().strip()
            func_output = pformat(func_output, compact=True, width=term_width-2)

        if "\n" not in func_output and len(func_output) <= width_avail:
            print(ltitle + func_output.ljust(width_avail) + rtitle)
        else:
            print(f"{ltitle}{" "*width_avail}{rtitle}\n{indent(func_output, "  ")}\n")

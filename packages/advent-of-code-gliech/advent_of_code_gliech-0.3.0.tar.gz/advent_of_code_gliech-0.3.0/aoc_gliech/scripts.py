from aocd.get import current_day, most_recent_year
from docopt import docopt
from importlib.metadata import version
from itertools import chain
from operator import methodcaller
from pathlib import Path
from textwrap import dedent
import tomllib

aoc_file = """\
def prep(data):
    return data.split("\\n")

def part_a(data):
    return prep(data)

def part_b(data):
    return None

if __name__ == "__main__":
    from aoc_gliech import solve
    solve(part_a, part_b)
"""

def read_tool_config(tool_key):
    current_dir = Path.cwd()
    for path in chain((current_dir,), current_dir.parents):
        project_file = path / "pyproject.toml"
        if project_file.exists():
            break
    else:
        raise FileNotFoundError("Could not locate pyproject.toml file")
    project_config = tomllib.loads(project_file.read_text())
    tool_section = project_config.get("tool", {}).get(tool_key, {})
    return (project_file.parent, tool_section)

def create_day_file():
    """
    Create a new file to solve advent of code.

    Usage:
        aoc-scaffold [--day=<number>] [--year=<number>] [--path=<string>]
        aoc-scaffold (-h | --help)
        aoc-scaffold --version

    Options:
        -d, --day=<number>   Day for the file path and templating values. Defaults
                             to the current (closest) day.
        -y, --year=<number>  Year for the file path and templating values. Defaults
                             to the currently running year.
        -p, --path=<string>  Path to write the template to. May contain placeholders
                             for {day} and {year}. A default can be set in your
                             pyproject.toml file, under tool.advent-of-code-gliech
                             with the key puzzle_path. If set in pyproject.toml, the
                             path will be relative to your project root.
        --version            Show version info.
        -h --help            Show this help screen.
    """

    arguments = docopt(dedent(create_day_file.__doc__), version=version("advent-of-code-gliech"))
    year = int(arguments.year or most_recent_year())
    day = int(arguments.day or current_day())
    path_formatter = methodcaller("format", day=day, year=year)
    if arguments.path is not None:
        file_path = Path(path_formatter(arguments.path))
    else:
        project_root, tool_config = read_tool_config("advent-of-code-gliech")
        puzzle_path = tool_config.get("puzzle_path")
        if puzzle_path is None:
            raise KeyError(
                "Please set a puzzle_path in your pyproject.toml under"
                " tool.advent-of-code-gliech or provide a path with the --path"
                " argument"
            )
        file_path = project_root / path_formatter(puzzle_path)
        # file_path = puzzle_path / f"y{year}" / f"d{day:02d}.py"
    if file_path.exists():
        raise FileExistsError(f"File {file_path} already exists")
    file_path.parent.mkdir(exist_ok=True)
    file_path.write_text(aoc_file)
    print(f"Created file at {file_path}")

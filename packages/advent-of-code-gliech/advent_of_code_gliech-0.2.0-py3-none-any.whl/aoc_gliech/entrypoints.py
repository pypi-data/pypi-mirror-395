import importlib
import json
import subprocess
from pathlib import Path

def python(year, day, data):
    puzzle_module_name = f"aoc_gliech.y{year}.d{day:02d}"
    try:
        puzzle_solutions = importlib.import_module(puzzle_module_name)
    except ModuleNotFoundError as e:
        if e.name == puzzle_module_name:
            return None, None
        else:
            raise e
    return puzzle_solutions.part_a(data), puzzle_solutions.part_b(data)

def tofu(year, day, data):
    module_path = Path(__file__).parent / "tofu" / str(year) / f"{day:02d}"
    if not module_path.is_dir():
        return None, None
    if not ( module_path / ".terraform" ).is_dir():
        subprocess.check_output(("tofu", "init"), cwd=module_path)
    tofu_proc_out = subprocess.check_output(
        ("tofu", "apply", "-auto-approve", "-json", "-var", f"puzzle_input='{data}'"),
        cwd=module_path
    )
    # stdout of tofu in json mode should be one object per line
    tofu_messages = (json.loads(line) for line in tofu_proc_out.splitlines())
    # There should be 2 messages of type outputs. One for the plan and one for
    # the apply.
    plan_out, apply_out = filter(lambda a: a["type"]=="outputs", tofu_messages)
    # Remove fluff around the output key-value pairs
    module_outputs = {name: attrs["value"] for name, attrs in apply_out["outputs"].items()}
    return module_outputs.get("solution_a"), module_outputs.get("solution_b")

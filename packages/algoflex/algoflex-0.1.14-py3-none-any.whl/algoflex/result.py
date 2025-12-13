from textual.screen import ModalScreen
from textual.widgets import RichLog
from algoflex.questions import questions
from algoflex.db import get_db
from tinydb import Query
import tempfile
import subprocess
import os

KV = Query()


class ResultModal(ModalScreen):
    BINDINGS = [("escape", "dismiss", "dismiss")]
    DEFAULT_CSS = """
    ResultModal {
        &>* {
            max-width: 90;
        }
        align: center middle;
        RichLog {
            width: 1fr;
            height: 12;
            padding: 1 0;
            padding-left: 2;
            overflow-x: auto;
            background: $boost;
        }
    }
    """
    TEST_CODE = """
import sys

def truncate(param):
    s = str(param)
    if len(s) > 60:
        return f'{s[:32]}... (truncated {type(param)})'
    return param

def display(params):
    return [truncate(param) for param in params]

def run_tests():
    total, passed = len(test_cases), 0
    for i, [inputs, expected] in enumerate(test_cases):
        try:
            result = solution(*inputs)
            if result == expected:
                print(f"[green][b]~[/] test case {i+1} passed![/]")
                passed += 1
            else:
                print(f"[red][b]x[/] test case {i+1} failed![/] \\n\\t[b]inputs[/]: {display(inputs)}\\n\\t[b]got[/]: [red]{result}[/]\\n\\t[b]expected[/]: [green]{expected}[/]")
        except Exception as e:
            print(f"[red][b]x[/] test case {i+1} error![/]\\n\\t[b]error[/]: {e}\\n\\t[b]inputs[/]: {display(inputs)}")
            return 1
    if passed == total:
        print(f"\\n{passed}/{total} passed!")
        return 0
    if passed < total:
        print(f"\\n {total - passed} failing.")
    return 1

if __name__ == "__main__":
    sys.exit(run_tests())
    """

    def __init__(self, problem_id, user_code, elapsed):
        super().__init__()
        self.problem_id = problem_id
        self.user_code = user_code
        self.elapsed = elapsed

    def on_mount(self):
        self.run_user_code()

    def compose(self):
        yield RichLog(markup=True, wrap=True, max_lines=1_000)

    def run_user_code(self):
        stats = get_db()
        s = stats.get(KV.problem_id == self.problem_id) or {}
        success, attempts = False, s.get("attempts", 0) + 1
        passed, best = s.get("passed", 0), s.get("best", 0)
        user_code = self.user_code.strip()
        output_log = self.query_one(RichLog)
        test_cases = questions.get(self.problem_id, {}).get("test_cases", [])
        full_code = f"{user_code}\n\n{test_cases}\n\n{self.TEST_CODE}"
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".py", mode="w+", encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(full_code)
        try:
            result = subprocess.run(
                ["python", tmp_file.name], capture_output=True, text=True, timeout=5
            )
            if result.stdout:
                output_log.write(result.stdout, animate=True)
            if result.stderr:
                output_log.write(result.stderr, animate=True)
            if result.returncode == 0:
                passed += 1
                success = True
        except subprocess.TimeoutExpired:
            output_log.write(
                "[red]Execution timed out[/]\\n\\tYour solution must run within 10 seconds"
            )
        except Exception as e:
            output_log.write(f"[red]Error running code[/]\\n\\t{e}")
        finally:
            os.remove(tmp_file.name)

        stats.upsert(
            {
                "attempts": attempts,
                "passed": passed,
                "problem_id": self.problem_id,
            },
            KV.problem_id == self.problem_id,
        )

        if not success:
            stats.upsert({"last_attempt": "Failed"}, KV.problem_id == self.problem_id)

        if success:
            stats.upsert(
                {"last_attempt": self.elapsed}, KV.problem_id == self.problem_id
            )
            if not best or self.elapsed < best:
                stats.upsert({"best": self.elapsed}, KV.problem_id == self.problem_id)

from textual.app import App
from textual.screen import Screen
from textual.containers import (
    Horizontal,
    Vertical,
    VerticalScroll,
)
from textual.widgets import Footer, Markdown, Static
from textual.binding import Binding
from textual.reactive import Reactive
from algoflex.questions import questions
from algoflex.attempt import AttemptScreen
from algoflex.custom_widgets import Title, Problem
from algoflex.db import get_db
from random import shuffle
from tinydb import Query

KV = Query()


class StatScreen(Vertical):
    DEFAULT_CSS = """
    Horizontal {
        Vertical {
            background: $boost;
            padding: 1;
            margin: 1 0;
        }
        #passed, #last_attempt, #best, #rank {
            padding-top: 1;
        }
    }
    """

    def compose(self):
        with Horizontal():
            with Vertical():
                yield Static("[b]Passed[/]")
                yield Static("...", id="passed")
            with Vertical():
                yield Static("[b]Last[/]")
                yield Static("...", id="last_attempt")
            with Vertical():
                yield Static("[b]Best[/]")
                yield Static("...", id="best")
            with Vertical():
                yield Static("[b]Rank[/]")
                yield Static("...", id="rank")


class HomeScreen(App):
    BINDINGS = [
        Binding("a", "attempt", "attempt", tooltip="Attempt this question"),
        Binding("n", "next", "next", tooltip="Next question"),
        Binding("p", "previous", "previous", tooltip="Previous question"),
    ]
    DEFAULT_CSS = """
    HomeScreen {
        Problem {
            &>*{ max-width: 100; }
            align: center middle;
            margin-top: 1;
        }
        StatScreen {
            height: 7;
            &>* {max-width: 100; }
            align: center middle;
        }
    }
    """
    problem_id = Reactive(0, always_update=True)
    index = Reactive(0, bindings=True)
    PROBLEMS_COUNT = len(questions.keys())
    PROBLEMS = [i for i in range(PROBLEMS_COUNT)]

    def compose(self):
        problem = questions.get(id, {}).get("markdown", "")
        yield Title()
        with VerticalScroll():
            yield Problem(problem)
            yield StatScreen()
        yield Footer()

    def on_mount(self):
        shuffle(self.PROBLEMS)
        self.problem_id = self.PROBLEMS[self.index]

    def hrs_mins_secs(self, tm):
        if isinstance(tm, str):
            return tm
        mins, secs = divmod(tm, 60)
        hrs, mins = divmod(mins, 60)
        return f"{hrs:02,.0f}:{mins:02.0f}:{secs:02.0f}"

    def time_markup(self, tm, color):
        tm = self.hrs_mins_secs(tm)
        if tm == "..." or color == "primary":
            return f"[$primary]{tm}[/]"
        if tm == "Failed" or color == "red":
            return f"[red]{tm}[/]"
        return f"[green]{tm}[/]"

    def watch_problem_id(self, id):
        stats = get_db()
        s = stats.get(KV.problem_id == id) or {}
        p = questions.get(id, {})
        problem, rank = p.get("markdown", ""), p.get("rank", "Easy")
        passed, attempts, last, best = (
            s.get("passed", "0"),
            s.get("attempts", "0"),
            s.get("last_attempt", "..."),
            s.get("best", "..."),
        )

        last_color = "primary" if (isinstance(last, float) and last > best) else ""
        best = self.time_markup(best, color="green")
        last = self.time_markup(last, last_color)

        self.query_one(Problem).query_one(Markdown).update(markdown=problem)
        s_widget = self.query_one(StatScreen)
        s_widget.query_one("#passed").update(
            f"[$primary]{str(passed)}/{str(attempts)}[/]"
        )
        s_widget.query_one("#last_attempt").update(last)
        s_widget.query_one("#best").update(best)
        s_widget.query_one("#rank").update(f"[$primary]{rank}[/]")

    def action_attempt(self):
        def update(_id):
            self.problem_id = self.PROBLEMS[self.index]

        self.push_screen(AttemptScreen(self.problem_id), update)

    def action_next(self):
        if self.index + 1 < self.PROBLEMS_COUNT:
            self.index += 1
        self.problem_id = self.PROBLEMS[self.index]

    def action_previous(self):
        if self.index > 0:
            self.index -= 1
        self.problem_id = self.PROBLEMS[self.index]

    def check_action(self, action, parameters):
        if not self.screen.id == "_default":
            if action == "attempt" or action == "next" or action == "previous":
                return False
        if self.index == self.PROBLEMS_COUNT - 1 and action == "next":
            return
        if self.index == 0 and action == "previous":
            return
        return True

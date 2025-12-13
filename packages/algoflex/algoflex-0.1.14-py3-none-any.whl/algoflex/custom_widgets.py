from textual.containers import VerticalScroll, Center
from textual.widgets import Markdown, Static


class Problem(VerticalScroll):
    DEFAULT_CSS = """
    VerticalScroll {
        Markdown {
            height: 1fr;
            padding: 0 1;
        }
    }
    """

    def __init__(self, problem):
        super().__init__()
        self.problem = problem

    def compose(self):
        yield Markdown(self.problem)


class Title(Center):
    DEFAULT_CSS = """
    Title {
        height: 3;
        Static {
            height: 1fr;
            color: $markdown-h1-color;
            background: $boost;
            content-align: center middle;
        }
    }
    """

    def compose(self):
        yield Static("[b]Algoflex - The terminal code practice app[/]")

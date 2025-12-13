from textual.screen import ModalScreen
from textual.widgets import Input
from textual.message import Message


class Search(Message):
    """Search complete."""
    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query


class SearchScreen(ModalScreen[str]):
    DEFAULT_CSS = """
    SearchScreen {
        align: center middle;
    }
    Input {
        width: 50;
        height: 1;
    }
    """

    def compose(self):
        yield Input(placeholder="Search node labels...", classes="primary")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.input.value.strip().lower()
        if query:
            self.post_message(Search(query))
        self.dismiss()

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Input, Label, TextArea


class FilenamePrompt(ModalScreen[str | None]):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("Tudix - Enter file path"),
            Input(placeholder="path/to/file.txt", id="filename-input"),
            Horizontal(
                Button("OK", id="ok"),
                Button("Cancel", id="cancel"),
            ),
        )

    def on_mount(self) -> None:
        self.query_one("#filename-input", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            name = self.query_one("#filename-input", Input).value.strip()
            self.dismiss(name or None)
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        name = event.value.strip()
        self.dismiss(name or None)


class TudixApp(App):
    """A minimal Textual-based text editor.

    This is intentionally simple for now; we'll port more Qudix behavior
    incrementally (status messages, prompts, additional keybindings, etc.).
    """

    TITLE = "Tudix"

    BINDINGS = [
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+z", "undo", "Undo"),
        Binding("ctrl+y", "redo", "Redo"),
        Binding("ctrl+n", "quit", "Quit"),
    ]

    def __init__(self, file_path: Optional[Path] = None) -> None:
        super().__init__()
        self._path: Optional[Path] = file_path
        self._last_saved_text: str = ""
        self._confirm_exit: bool = False

    def compose(self) -> ComposeResult:
        editor = TextArea(id="editor", show_line_numbers=True, soft_wrap=True)
        status = Label("Tudix - Ready", id="status")
        footer = Footer()
        yield editor
        yield status
        yield footer

    def on_mount(self) -> None:
        status = self.query_one("#status", Label)

        if self._path is None:
            status.update("Tudix - Ready (no file path supplied)")
            self.push_screen(FilenamePrompt(), self._on_filename_selected)
            return

        self._open_or_prepare_path(self._path)

    def _open_or_prepare_path(self, path: Path) -> None:
        editor = self.query_one("#editor", TextArea)
        status = self.query_one("#status", Label)

        self._path = path

        if not path.exists():
            editor.text = ""
            self._last_saved_text = ""
            self._confirm_exit = False
            status.update(f"Tudix - Creating file {path}")
            return

        try:
            text = path.read_text()
        except OSError as exc:
            status.update(f"Tudix - Failed to open {path}: {exc}")
            return

        editor.text = text
        self._last_saved_text = text
        self._confirm_exit = False
        status.update(f"Tudix - Opened {path}")

    def _on_filename_selected(self, result: str | None) -> None:
        status = self.query_one("#status", Label)
        if not result:
            status.update("Tudix - No file path supplied; quitting.")
            self.exit()
            return
        path = Path(result).expanduser()
        self._open_or_prepare_path(path)

    def action_save(self) -> None:
        editor = self.query_one("#editor", TextArea)
        status = self.query_one("#status", Label)

        if self._path is None:
            status.update("Tudix - No file path supplied; relaunch tudix with a file path to save.")
            return

        try:
            self._path.write_text(editor.text)
        except OSError as exc:
            status.update(f"Tudix - Failed to save: {exc}")
            return

        self._last_saved_text = editor.text
        self._confirm_exit = False
        status.update(f"Tudix - Saved to {self._path}")

    def action_undo(self) -> None:
        editor = self.query_one("#editor", TextArea)
        editor.action_undo()

    def action_redo(self) -> None:
        editor = self.query_one("#editor", TextArea)
        editor.action_redo()

    def action_quit(self) -> None:
        status = self.query_one("#status", Label)
        editor = self.query_one("#editor", TextArea)
        dirty = self._path is not None and editor.text != self._last_saved_text
        if dirty and not self._confirm_exit:
            self._confirm_exit = True
            status.update("Tudix - Warning: file has unsaved changes. Press Ctrl+N again to quit without saving.")
            return
        self.exit()


def run(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Launch Tudix (Textual-based editor).")
    parser.add_argument("path", nargs="?", help="Optional file path to open.")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    file_path = Path(args.path).expanduser() if args.path else None
    app = TudixApp(file_path=file_path)
    app.run()

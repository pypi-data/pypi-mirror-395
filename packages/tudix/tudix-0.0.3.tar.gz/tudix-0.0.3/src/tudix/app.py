from __future__ import annotations

import argparse
import base64
import os
import sys
from pathlib import Path
from typing import Iterable, Optional

from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, Footer, Input, Label, TextArea


class FilenamePrompt(ModalScreen[str | None]):
    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("ctrl+n", "cancel", "Cancel"),
    ]

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

    def action_cancel(self) -> None:
        self.dismiss(None)


class TudixApp(App):
    """A minimal Textual-based text editor.

    This is intentionally simple for now; we'll port more Qudix behavior
    incrementally (status messages, prompts, additional keybindings, etc.).
    """

    TITLE = "Tudix"

    CSS = """
    #status {
        height: 1;
        padding: 0 1;
    }

    #status.status-warning {
        background: #af0000;
        color: white;
    }

    #status.status-success {
        background: #005f00;
        color: white;
    }
    """

    BINDINGS = [
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+z", "undo", "Undo"),
        Binding("ctrl+y", "redo", "Redo"),
        Binding("ctrl+shift+c", "tudix_copy", "Copy"),
        Binding("ctrl+shift+x", "tudix_cut", "Cut"),
        Binding("ctrl+shift+v", "tudix_paste", "Paste"),
        Binding("ctrl+n", "quit", "Quit"),
    ]

    def __init__(self, file_path: Optional[Path] = None) -> None:
        super().__init__()
        self._path: Optional[Path] = file_path
        self._last_saved_text: str = ""
        self._dirty: bool = False
        self._confirm_exit: bool = False

    def compose(self) -> ComposeResult:
        editor = TextArea(id="editor", show_line_numbers=True, soft_wrap=True)
        status = Label("Tudix - Ready", id="status")
        footer = Footer()
        yield editor
        yield status
        yield footer

    def on_mount(self) -> None:
        if self._path is None:
            self._set_status("Tudix - Ready (no file path supplied)")
            self.push_screen(FilenamePrompt(), self._on_filename_selected)
            return

        self._open_or_prepare_path(self._path)

    def _set_status(self, message: str, *, kind: str = "normal") -> None:
        status = self.query_one("#status", Label)
        status.update(message)
        status.remove_class("status-warning", "status-success")
        if kind == "warning":
            status.add_class("status-warning")
        elif kind == "success":
            status.add_class("status-success")

    def _osc52_set_clipboard(self, text: str) -> None:
        """Send *text* to the client clipboard via OSC52 when over SSH on Unix.

        This is a best-effort mechanism for SSH sessions from capable terminals
        (e.g. iTerm2, kitty, WezTerm) and is a no-op on Windows or when not
        running under SSH.
        """
        if not text:
            return
        if sys.platform.startswith("win"):
            return
        if not (
            os.environ.get("SSH_CONNECTION")
            or os.environ.get("SSH_CLIENT")
            or os.environ.get("SSH_TTY")
        ):
            return
        try:
            encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
        except Exception:
            return
        seq = f"\x1b]52;c;{encoded}\x07"
        try:
            sys.stdout.write(seq)
            sys.stdout.flush()
        except Exception:
            pass

    def _open_or_prepare_path(self, path: Path) -> None:
        editor = self.query_one("#editor", TextArea)

        self._path = path

        if not path.exists():
            editor.text = ""
            self._last_saved_text = ""
            self._dirty = False
            self._confirm_exit = False
            self._set_status(f"Tudix - Creating file {path}")
            return

        try:
            text = path.read_text()
        except OSError as exc:
            self._set_status(f"Tudix - Failed to open {path}: {exc}", kind="warning")
            return

        editor.text = text
        self._last_saved_text = text
        self._dirty = False
        self._confirm_exit = False
        self._set_status(f"Tudix - Opened {path}")

    def _on_filename_selected(self, result: str | None) -> None:
        if not result:
            self._set_status("Tudix - No file path supplied; quitting.", kind="warning")
            self.exit()
            return
        path = Path(result).expanduser()
        self._open_or_prepare_path(path)

    def action_save(self) -> None:
        editor = self.query_one("#editor", TextArea)

        if self._path is None:
            self._set_status(
                "Tudix - No file path supplied; relaunch tudix with a file path to save.",
                kind="warning",
            )
            return

        try:
            self._path.write_text(editor.text)
        except OSError as exc:
            self._set_status(f"Tudix - Failed to save: {exc}", kind="warning")
            return

        self._last_saved_text = editor.text
        self._dirty = False
        self._confirm_exit = False
        self._set_status(f"Tudix - Saved to {self._path}", kind="success")

    def on_text_area_changed(self, event: TextArea.Changed) -> None:  # type: ignore[override]
        self._dirty = True
        self._confirm_exit = False

    def action_undo(self) -> None:
        editor = self.query_one("#editor", TextArea)
        editor.action_undo()

    def action_redo(self) -> None:
        editor = self.query_one("#editor", TextArea)
        editor.action_redo()

    def action_tudix_copy(self) -> None:
        editor = self.query_one("#editor", TextArea)
        # Use Textual's own copy so internal clipboard remains functional.
        editor.action_copy()
        self._osc52_set_clipboard(editor.selected_text or "")

    def action_tudix_cut(self) -> None:
        editor = self.query_one("#editor", TextArea)
        text = editor.selected_text or ""
        if text:
            self._osc52_set_clipboard(text)
        editor.action_cut()

    def action_tudix_paste(self) -> None:
        editor = self.query_one("#editor", TextArea)
        editor.action_paste()

    def action_quit(self) -> None:
        editor = self.query_one("#editor", TextArea)
        dirty = self._dirty and self._path is not None
        if dirty and not self._confirm_exit:
            self._confirm_exit = True
            self._set_status(
                "Tudix - Warning: file has unsaved changes. Press Ctrl+N again to quit without saving.",
                kind="warning",
            )
            return
        self.exit()

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        for cmd in super().get_system_commands(screen):
            if cmd.title in {"Maximize", "Quit"}:
                continue
            yield cmd


def run(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Launch Tudix (Textual-based editor).")
    parser.add_argument("path", nargs="?", help="Optional file path to open.")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    file_path = Path(args.path).expanduser() if args.path else None
    app = TudixApp(file_path=file_path)
    app.run()

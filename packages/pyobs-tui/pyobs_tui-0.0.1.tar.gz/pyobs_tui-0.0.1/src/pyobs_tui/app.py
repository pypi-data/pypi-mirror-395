from os.path import basename
from typing import Any, cast

from astropy.time import Time
from pyobs.events import Event, LogEvent
from pyobs.modules import Module
from pyobs.utils.shellcommand import ShellCommand
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalGroup
from textual.widget import Widget
from textual.widgets import RichLog, Input, TabbedContent, TabPane, Label


class Shell(VerticalGroup):  # type: ignore
    def compose(self) -> ComposeResult:
        yield RichLog(highlight=True, markup=True)
        yield Input()

    # def on_mount(self) -> None:
    #    self.query_one(Input).focus()

    @on(Input.Submitted)
    async def handle_submit(self, event: Input.Submitted) -> None:
        comm = cast(TuiApp, self.app).module.comm
        command = event.value.strip()

        try:
            cmd = ShellCommand.parse(command)
            self._log(str(cmd))
        except Exception as e:
            self._log(f"$ {command}")
            self._log(f"[red]{str(e)}[/red]")
            return

        # execute command
        response = await cmd.execute(comm)

        # log response
        self._log(response.bbcode)
        event.input.value = ""

    def _log(self, line: str) -> None:
        self.query_one(RichLog).write(line)


class Log(VerticalGroup):  # type: ignore
    def compose(self) -> ComposeResult:
        yield RichLog(highlight=True, markup=True)

    def process_log_entry(self, entry: Event, sender: str) -> None:
        """Process a new log entry.

        Args:
            entry: The log event.
            sender: Name of sender.
        """
        if not isinstance(entry, LogEvent):
            return

        # date
        time = Time(entry.time, format="unix")

        # level
        match entry.level:
            case "DEBUG" | "INFO":
                level = f"[green]{entry.level}[/green]"
            case "WARNING":
                level = f"[yellow]{entry.level}[/yellow]"
            case "ERROR":
                level = f"[red]{entry.level}[/red]"
            case _:
                level = entry.level

        # add line
        line = f"[{time.iso.split()[1]}] {sender} {level} {basename(entry.filename)}:{entry.line} {entry.message}"
        self.query_one(RichLog).write(line)


class TuiApp(App):
    """A Textual app for pyobs."""

    def __init__(self, module: Module, **kwargs: Any):
        App.__init__(self, **kwargs)
        self.module = module

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Log"):
                yield Log()
            with TabPane("Shell"):
                yield Shell()

    async def process_log_entry(self, entry: Event, sender: str) -> bool:
        self.query_one(Log).process_log_entry(entry, sender)
        return True

from typing import Any

from pyobs.events import LogEvent
from pyobs.modules import Module

from .app import TuiApp


class TUI(Module):
    __module__ = "pyobs_tui"

    def __init__(self, *args: Any, **kwargs: Any):
        """Inits a new TUI."""

        Module.__init__(self, *args, **kwargs)
        self.app = TuiApp(self)

    async def open(self) -> None:
        """Opens the TUI."""
        await super().open()

        # subscribe to events
        await self.comm.register_event(LogEvent, self.app.process_log_entry)

    async def main(self) -> None:
        """Main loop for application."""
        await self.app.run_async()

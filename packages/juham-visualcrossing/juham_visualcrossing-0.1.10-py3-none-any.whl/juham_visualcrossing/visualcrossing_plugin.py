from typing_extensions import override
from masterpiece import Plugin, Composite
from .visualcrossing import VisualCrossing


class VisualCrossingPlugin(Plugin):
    """Plugin class, for installing a visualcrossing specific features into the host application."""

    def __init__(self, name: str = "visual_crossing") -> None:
        """Create visualcrossing weather service."""
        super().__init__(name)

    @override
    def install(self, app: Composite) -> None:
        # Create and insert a VisualCrossing classes into the host application.
        obj = VisualCrossing()
        app.add(obj)

from typing_extensions import override
from masterpiece import Plugin, Composite
from .spothintafi import SpotHintaFi


class SpotHintaFiPlugin(Plugin):
    """Plugin class, for installing a spothintafi specific features into the host application."""

    def __init__(self, name: str = "spothintafi") -> None:
        """Create spothintafi electricity price service."""
        super().__init__(name)

    @override
    def install(self, app: Composite) -> None:
        # Create and insert a SpotHintaFi classes into the host application.
        obj = SpotHintaFi()
        app.add(obj)

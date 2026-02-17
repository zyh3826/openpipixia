"""Channel interfaces and adapters."""

from .base import BaseChannel
from .local import LocalChannel
from .manager import ChannelManager

__all__ = ["BaseChannel", "ChannelManager", "LocalChannel"]

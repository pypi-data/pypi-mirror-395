"""
IlyasMessageProtocol – простой протокол обмена сообщениями по socket’у.

"""

from .protocol import (
    HEADER_SIZE,
    send,
    receive,
)

__all__ = [
    "HEADER_SIZE",
    "send",
    "receive",
]

__version__ = "0.1.0"


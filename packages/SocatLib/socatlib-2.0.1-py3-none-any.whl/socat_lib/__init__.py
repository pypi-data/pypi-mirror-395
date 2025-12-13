"""
SocatLib - Async Python library for network communication using socat
"""

from .core import (
    sending,
    listening,
    send_file,
    reverse_shell,
    encrypted_send,
    encrypted_listen,
    receive_file
)

__version__ = "2.0.1"
__author__ = "ash404.dev"

__all__ = [
    'sending',
    'listening',
    'send_file',
    'reverse_shell',
    'encrypted_send',
    'encrypted_listen',
    'receive_file'
]
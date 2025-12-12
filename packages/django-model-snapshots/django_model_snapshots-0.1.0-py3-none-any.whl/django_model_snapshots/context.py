from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Generator

_force_versioning_context: ContextVar[bool] = ContextVar(
    "force_versioning_context", default=False
)


@contextmanager
def force_versioning() -> Generator[None, None, None]:
    """
    Context manager to force versioning even if VERSIONING_AUTO is False.
    """
    token: Token = _force_versioning_context.set(True)
    try:
        yield
    finally:
        _force_versioning_context.reset(token)


def is_versioning_forced() -> bool:
    """
    Check if versioning is currently forced.
    """
    return _force_versioning_context.get()

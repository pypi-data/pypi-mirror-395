# termdo/__init__.py
"""termdo — terminal todo manager package."""

__all__ = ["__version__", "main"]
__version__ = "1.0.0"

def main() -> None:
    # lazy import to keep import lightweight
    from .cli import main as _cli_main
    return _cli_main()

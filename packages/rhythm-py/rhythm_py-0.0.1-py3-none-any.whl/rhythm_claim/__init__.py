"""
Rhythm - A lightweight durable execution framework using only Postgres

This is a placeholder package to reserve the 'rhythm' name on PyPI.

For the production-ready implementation, please install 'rhythm-async':
    pip install rhythm-async

Repository: https://github.com/rhythmasync/rhythm
"""

__version__ = "0.0.1"

def __getattr__(name):
    """Redirect users to the actual package."""
    raise ImportError(
        f"This is a placeholder package. "
        f"Please install the actual implementation:\n\n"
        f"    pip install rhythm-async\n\n"
        f"Documentation: https://github.com/rhythmasync/rhythm"
    )

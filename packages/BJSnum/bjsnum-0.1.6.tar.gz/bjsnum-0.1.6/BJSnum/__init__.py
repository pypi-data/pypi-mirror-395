# __init__.py

# Explicitly import the functions from each module
from .add import add
from .sub import sub
from .mult import mult
from .div_norm import div_norm
from .div_flr import div_flr
from .pow_ import pow_
from mod import mod

# Define the public API
__all__ = ["add", "sub", "mult", "div_norm", "div_flr", "mod", "pow_"]

# Optional: set version if you want to expose it
try:
    from importlib.metadata import version
    __version__ = version("your-package-name")  # must match pyproject.toml name
except Exception:
    __version__ = "unknown"
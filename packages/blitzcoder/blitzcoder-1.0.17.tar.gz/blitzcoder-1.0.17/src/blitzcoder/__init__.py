"""
BlitzCoder - AI-Powered Development Assistant

A comprehensive AI-powered development assistant that helps with code generation,
refactoring, project scaffolding, and development tasks.
"""

__version__ = "1.0.17"
__author__ = "BlitzCoder Team"
__author_email__ = "raghunandanerukulla@gmail.com"
__description__ = "AI-Powered Development Assistant"
__url__ = "https://github.com/Raghu6798/Blitz_Coder"
__license__ = "MIT"
__keywords__ = ["ai", "code-generation", "development", "assistant", "cli"]

# Import main components
from . import cli

__all__ = [
    "cli",
    "__version__",
    "__author__",
    "__description__",
] 
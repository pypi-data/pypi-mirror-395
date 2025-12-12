"""exe2txt - Convert Windows EXE/DLL files into text representations for LLM prompting."""

from exe2txt.core import analyze_pe, PEInfo

__version__ = "0.1.0"
__all__ = ["analyze_pe", "PEInfo", "__version__"]

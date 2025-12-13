from dataclasses import dataclass, field
from typing import List

@dataclass
class Metadata:
    """A model representing the book's metadata."""
    title: str = field(default="")
    authors: List[str] = field(default_factory=list)
    translators: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    index: List[str] = field(default_factory=list)
    cover: str = field(default="")

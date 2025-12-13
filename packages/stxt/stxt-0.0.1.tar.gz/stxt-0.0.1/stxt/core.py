from dataclasses import dataclass

__version__ = "0.0.1"


@dataclass
class STXTDocument:
    raw: str


def parse(text: str) -> STXTDocument:
    return STXTDocument(raw=text)

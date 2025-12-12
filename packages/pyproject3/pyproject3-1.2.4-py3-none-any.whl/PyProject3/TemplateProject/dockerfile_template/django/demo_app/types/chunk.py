from dataclasses import dataclass


@dataclass
class ModelVendorChunk:
    content: str
    done: bool

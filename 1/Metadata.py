from dataclasses import dataclass


@dataclass
class Metadata:
    is_best: bool = False
    step: int = 0
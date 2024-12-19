from dataclasses import dataclass
from typing import List

@dataclass
class Step:
    name: str
    duration: int  # 以分钟为单位
    needs_focus: bool

@dataclass
class Task:
    name: str
    steps: List[Step]
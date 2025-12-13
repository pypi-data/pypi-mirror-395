from enum import Enum

class BitDepthOptions(Enum):
    BD_1  = 1
    BD_8  = 8
    BD_10 = 10
    BD_12 = 12
    BD_14 = 14
    BD_16 = 16
    BD_24 = 24
    BD_32 = 32
    BD_64 = 64

from dataclasses import dataclass

@dataclass(frozen=True)
class BitDepth:
    value: BitDepthOptions

    def max_value(self) -> int:
        return (1 << self.value.value) - 1

    def __int__(self) -> int:
        return self.value.value

    def __str__(self) -> str:
        return f"{self.value.value}-bit"

    def __eq__(self, other) -> bool:
        if isinstance(other, BitDepth):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, BitDepth):
            return self.value.value < other.value.value
        return NotImplemented

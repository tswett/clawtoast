from typing import Sequence


class SoCTarget():
    def read_memory_block32(self, addr: int, size: int) -> Sequence[int]: ...

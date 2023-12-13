from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import TracebackType
from typing import Optional, Sequence

from pyocd.core.helpers import ConnectHelper
from pyocd.core.session import Session
from pyocd.core.soc_target import SoCTarget

class NucleoBoard:
    session_context_manager: Session
    session: Optional[Session]
    # TODO: In practice, session_context_manager and session have the same
    # value; do we need both of them?
    target: Optional[SoCTarget]

    def __init__(self, session_context_manager: Session):
        self.session_context_manager = session_context_manager
        self.session = None
        self.target = None

    def __enter__(self):
        self.session = self.session_context_manager.__enter__()
        self.target = self.session.target

        return self

    def __exit__(self, exc_type: Optional[type], exc_val: object, exc_traceback: Optional[TracebackType]):
        self.session_context_manager.__exit__(exc_type, exc_val, exc_traceback)

    @property
    def gpio(self) -> GpioReference:
        return GpioReference(self)

    def read_memory_block32(self, address: int, words: int) -> Sequence[int]:
        assert self.target is not None
        return self.target.read_memory_block32(address, words)

class GpioReference:
    def __init__(self, board: NucleoBoard):
        self.board = board

    def read(self) -> GpioInfo:
        info = GpioInfo()

        info_words = self.board.read_memory_block32(0x48000000, 0x400 * 9 // 4)

        for pin in GpioPin:
            gpiox_moder_index = pin.port.value * 0x400 // 4
            mode = GpioMode((info_words[gpiox_moder_index] >> (pin.number * 2)) & 0x3)
            info[pin] = GpioPinInfo(mode)

        return info

class GpioInfo:
    dict: dict[GpioPin, GpioPinInfo]

    def __init__(self):
        self.dict = {}

    def __getitem__(self, pin: GpioPin | str) -> GpioPinInfo:
        if isinstance(pin, str):
            pin = GpioPin[pin]

        return self.dict[pin]

    def __setitem__(self, pin: GpioPin | str, value: GpioPinInfo) -> None:
        if isinstance(pin, str):
            pin = GpioPin[pin]

        self.dict[pin] = value

@dataclass
class GpioPinInfo:
    mode: GpioMode

class GpioMode(Enum):
    Input = 0
    Output = 1
    AlternateFunction = 2
    Analog = 3

class GpioPort(Enum):
    GPIOA = A = 0
    GPIOB = B = 1
    GPIOC = C = 2
    GPIOD = D = 3
    GPIOE = E = 4
    GPIOF = F = 5
    GPIOG = G = 6
    GPIOH = H = 7
    GPIOI = I = 8

    @property
    def letter(self):
        return chr(ord('A') + self.value)

class GpioPinMeta(type):
    def __iter__(cls):
        for port in GpioPort:
            for number in range(16):
                yield GpioPin(port, number)

@dataclass
class GpioPin(metaclass=GpioPinMeta):
    port: GpioPort
    number: int

    def __class_getitem__(cls, name: str) -> GpioPin:
        assert name[0] == 'P'
        assert name[1] in 'ABCDEFGHI'
        assert 0 <= int(name[2:]) <= 15

        port = GpioPort[name[1]]
        number = int(name[2:])

        return GpioPin(port, number)

    def __hash__(self):
        return hash((self.port, self.number))

def connect_to_nucleo(connect_helper: Optional[type[ConnectHelper]] = None) -> NucleoBoard:
    if connect_helper is None:
        connect_helper = ConnectHelper
        assert connect_helper is not None

    session_context_manager = connect_helper.session_with_chosen_probe()
    assert session_context_manager is not None

    return NucleoBoard(session_context_manager)

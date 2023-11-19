from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

class NucleoBoard:
    def __init__(self, session_context_manager):
        self.session_context_manager = session_context_manager
        self.session = None
        self.target = None

    def __enter__(self):
        self.session = self.session_context_manager.__enter__()
        self.target = self.session.target

        return self

    def __exit__(self, type, value, traceback):
        self.session_context_manager.__exit__(type, value, traceback)

    @property
    def gpio(self) -> GpioReference:
        return GpioReference(self)

    def read_memory_block32(self, address: int, words: int) -> list[int]:
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
    def __init__(self):
        self.dict = {}

    def __getitem__(self, pin) -> GpioPinInfo:
        if isinstance(pin, str):
            pin = GpioPin[pin]

        return self.dict[pin]

    def __setitem__(self, pin, value: GpioPinInfo) -> None:
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

def connect_to_nucleo(connect_helper = None) -> NucleoBoard:
    if connect_helper is None:
        from pyocd.core.helpers import ConnectHelper
        connect_helper = ConnectHelper

    session_context_manager = connect_helper.session_with_chosen_probe()
    return NucleoBoard(session_context_manager)

from collections import defaultdict
import pytest
import random
from typing import Any

from clawtoast import steamer
from clawtoast.steamer import GpioMode, GpioPort, NucleoBoard

def test_gpioport_letters_are_correct() -> None:
    for letter in 'ABCDEFGHI':
        assert GpioPort[letter].letter == letter
        assert GpioPort['GPIO' + letter].letter == letter

class MemoryMock:
    pages: dict[int, Any] = defaultdict(lambda: bytearray([0xff] * 0x10000))

    def __getitem__(self, address: int) -> int:
        page = address >> 16
        offset = address & 0xffff

        return self.pages[page][offset]

    def __setitem__(self, address: int, value: int) -> None:
        page = address >> 16
        offset = address & 0xffff

        self.pages[page][offset] = value

class NucleoMock:
    def __init__(self):
        self.memory = MemoryMock()

    def set_gpio_mode(self, port: GpioPort, pin: int, mode: GpioMode) -> None:
        assert 0 <= pin <= 15

        register_address = 0x48000000 + 0x400 * port.value
        byte = pin // 4
        bit = (pin % 4) * 2
        mask = 0b11 << bit

        old_value = self.memory[register_address + byte]
        new_value = (old_value & ~mask) | (mode.value << bit)
        self.memory[register_address + byte] = new_value

class ConnectHelperMock:
    def __init__(self, nucleo_mock: NucleoMock):
        self.nucleo_mock = nucleo_mock

    def session_with_chosen_probe(self):
        return SessionContextManagerMock(self.nucleo_mock)

class SessionContextManagerMock:
    def __init__(self, nucleo_mock: NucleoMock):
        self.nucleo_mock = nucleo_mock

    def __enter__(self):
        return SessionMock(self.nucleo_mock)

    def __exit__(self, type, value, traceback):
        pass

class SessionMock:
    def __init__(self, nucleo_mock: NucleoMock):
        self.nucleo_mock = nucleo_mock

    @property
    def target(self):
        return TargetMock(self.nucleo_mock)

class TargetMock:
    def __init__(self, nucleo_mock: NucleoMock):
        self.nucleo_mock = nucleo_mock

    def read_memory_block32(self, address: int, words: int) -> list[int]:
        result = []

        for n in range(words):
            value = (
                self.nucleo_mock.memory[address + n * 4] +
                (self.nucleo_mock.memory[address + n * 4 + 1] << 8) +
                (self.nucleo_mock.memory[address + n * 4 + 2] << 16) +
                (self.nucleo_mock.memory[address + n * 4 + 3] << 24))

            result.append(value)

        return result

@pytest.fixture
def nucleo_mock() -> NucleoMock:
    return NucleoMock()

@pytest.fixture
def connect_helper(nucleo_mock):
    return ConnectHelperMock(nucleo_mock)

def test_can_run_connect_to_nucleo(connect_helper) -> None:
    steamer.connect_to_nucleo(connect_helper)

def test_can_use_with_with_connect_to_nucleo(connect_helper) -> None:
    with steamer.connect_to_nucleo(connect_helper) as nucleo:
        pass

@pytest.fixture
def nucleo(connect_helper) -> NucleoBoard:
    with steamer.connect_to_nucleo(connect_helper) as nucleo:
        yield nucleo

def test_can_run_read_gpio(nucleo: NucleoBoard) -> None:
    nucleo.gpio.read()

def test_can_read_gpio_mode(nucleo: NucleoBoard) -> None:
    gpio_config = nucleo.gpio.read()

    _ = gpio_config['PC0'].mode

def test_gpio_mode_is_correct(nucleo_mock: NucleoMock, nucleo: NucleoBoard) -> None:
    config_dict = {}

    for port in GpioPort:
        for pin in range(16):
            mode = random.choice(list(GpioMode))
            config_dict[(port, pin)] = mode
            nucleo_mock.set_gpio_mode(port, pin, mode)

    gpio_config = nucleo.gpio.read()

    for port in GpioPort:
        for pin in range(16):
            pin_name = f'P{port.letter}{pin}'
            assert gpio_config[pin_name].mode == config_dict[(port, pin)]

if __name__ == '__main__':
    pytest.main([__file__])

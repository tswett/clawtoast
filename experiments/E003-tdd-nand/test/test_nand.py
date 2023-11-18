# Copyright 2023 Tanner Swett.
#
# This file is part of Clawtoast. Clawtoast is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU
# General Public License as published by the Free Software Foundation.
#
# Clawtoast is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import inspect
import random
import time

from pyocd.core.helpers import ConnectHelper

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

    @property
    def base_address(self):
        return 0x48000000 + 0x400 * self.value

    @property
    def idr_address(self):
        return self.base_address + 0x10
    
    @property
    def odr_address(self):
        return self.base_address + 0x14

    @property
    def bsrr_address(self):
        return self.base_address + 0x18

class GpioMode(Enum):
    Input = 0
    Output = 1
    AlternateFunction = 2
    Analog = 3

class GpioOutputType(Enum):
    PushPull = 0
    _None = 0
    OpenDrain = 1

class GpioOutputSpeed(Enum):
    Low = 0
    _None = 0
    Medium = 1
    High = 2
    VeryHigh = 3

class GpioPullMode(Enum):
    NoPull = 0
    PullUp = 1
    PullDown = 2

@dataclass
class GpioConfig:
    mode: GpioMode
    output_type: GpioOutputType
    output_speed: GpioOutputSpeed
    pull_mode: GpioPullMode

    @staticmethod
    def from_words(words: list[int]) -> list[GpioConfig]:
        configs = []

        for pin in range(16):
            config = GpioConfig(
                GpioMode((words[0] >> (pin * 2)) & 0x3),
                GpioOutputType((words[1] >> (pin * 1)) & 0x1),
                GpioOutputSpeed((words[2] >> (pin * 2)) & 0x3),
                GpioPullMode((words[3] >> (pin * 2)) & 0x3),
            )

            configs.append(config)

        return configs

@dataclass
class GpioPin:
    port: GpioPort
    number: int

    @staticmethod
    def from_name(name: str) -> GpioPin:
        assert name[0] == 'P'
        assert name[1] in 'ABCDEFGHI'
        assert 0 <= int(name[2:]) <= 15

        port = GpioPort[name[1]]
        number = int(name[2:])

        return GpioPin(port, number)

    # Let people write e.g. GpioPin['PA5'] instead of GpioPin.from_name('PA5').
    def __class_getitem__(cls, name: str) -> GpioPin:
        return cls.from_name(name)

def get_gpio_configs(pyocd_target, port: GpioPort) -> list[GpioConfig]:
    config_words = pyocd_target.read_memory_block32(port.base_address, 4)

    #print(f"{port.name}: " + " ".join(f"{word:08x}" for word in config_words))

    return GpioConfig.from_words(config_words)

def get_gpio_inputs(pyocd_target, port: GpioPort) -> list[bool]:
    input_word = pyocd_target.read32(port.idr_address)

    return [bool((input_word >> pin) & 1) for pin in range(16)]

def get_gpio_outputs(pyocd_target, port: GpioPort) -> list[bool]:
    output_word = pyocd_target.read32(port.odr_address)

    return [bool((output_word >> pin) & 1) for pin in range(16)]

def assert_equal(actual, expected):
    if actual != expected:
        caller = inspect.stack()[1]
        source = inspect.getframeinfo(caller[0]).code_context[0].strip()

        raise AssertionError(f"{source} - expected {expected}, got {actual}")

def write_gpio_pin(pyocd_target, pin: GpioPin, value: bool):
    address = pin.port.bsrr_address
    
    if value:
        bit = pin.number
    else:
        bit = pin.number + 16

    pyocd_target.write32(address, 1 << bit)



# Use ConnectHelper to connect to our Nucleo L4R5ZI board
with ConnectHelper.session_with_chosen_probe() as session:
    target = session.target

    target.reset()
    time.sleep(0.05)

    gpiob_configs = get_gpio_configs(target, GpioPort.GPIOB)
    gpioc_configs = get_gpio_configs(target, GpioPort.GPIOC)

    # Input pins should be pulled up
    input_config = GpioConfig(
        mode=GpioMode.Input,
        output_type=GpioOutputType._None,
        output_speed=GpioOutputSpeed._None,
        pull_mode=GpioPullMode.PullUp,
    )

    # Normal output pins should be open-drain and pulled up, low speed
    normal_output_config = GpioConfig(
        mode=GpioMode.Output,
        output_type=GpioOutputType.OpenDrain,
        output_speed=GpioOutputSpeed.Low,
        pull_mode=GpioPullMode.PullUp,
    )

    # LED output pins should be push-pull, low speed
    led_output_config = GpioConfig(
        mode=GpioMode.Output,
        output_type=GpioOutputType.PushPull,
        output_speed=GpioOutputSpeed.Low,
        pull_mode=GpioPullMode.NoPull,
    )

    assert_equal(gpioc_configs[3], input_config)
    assert_equal(gpioc_configs[4], input_config)

    assert_equal(gpioc_configs[0], normal_output_config)
    assert_equal(gpioc_configs[1], normal_output_config)
    assert_equal(gpioc_configs[5], normal_output_config)

    assert_equal(gpiob_configs[7], led_output_config)
    assert_equal(gpiob_configs[14], led_output_config)
    assert_equal(gpioc_configs[7], led_output_config)

    for _ in range(50):
        pc0 = random.choice([True, False])
        pc1 = random.choice([True, False])

        print(f"Testing with {pc0=} and {pc1=}")

        write_gpio_pin(target, GpioPin['PC0'], pc0)
        write_gpio_pin(target, GpioPin['PC1'], pc1)

        time.sleep(0.2)

        gpioc_inputs = get_gpio_inputs(target, GpioPort.GPIOC)
        gpiob_outputs = get_gpio_outputs(target, GpioPort.GPIOB)
        gpioc_outputs = get_gpio_outputs(target, GpioPort.GPIOC)

        # The input to PC3 and the output from PB14 should equal pc0
        assert_equal(gpioc_inputs[3], pc0)
        assert_equal(gpiob_outputs[14], pc0)

        # The input to PC4 and the output from PC7 should equal pc1
        assert_equal(gpioc_inputs[4], pc1)
        assert_equal(gpioc_outputs[7], pc1)

        # The outputs from PC5 and PB7 should both equal not (pc0 and pc1)
        assert_equal(gpioc_outputs[5], not (pc0 and pc1))
        assert_equal(gpiob_outputs[7], not (pc0 and pc1))

# Copyright 2023 Tanner Swett.
#
# This file is part of Clawtoast. Clawtoast is free software: you can
# redistribute it and/or modify it under the terms of version 3 of the GNU
# General Public License as published by the Free Software Foundation.
#
# Clawtoast is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

import pytest

from clawtoast import steamer
from clawtoast.steamer import GpioMode, NucleoBoard

@pytest.fixture(scope='module')
def nucleo() -> NucleoBoard:
    with steamer.connect_to_nucleo() as nucleo:
        yield nucleo

@pytest.fixture(scope='module')
def configured_nucleo(nucleo: NucleoBoard) -> NucleoBoard:
    gpio_config = nucleo.gpio.read()

    for pin_name in ['PC0', 'PC1', 'PC5']:
        assert gpio_config[pin_name].mode == GpioMode.Output, f"Pin {pin_name} is not configured as an output."

    return nucleo

def test_dummy(configured_nucleo: NucleoBoard) -> None:
    pass

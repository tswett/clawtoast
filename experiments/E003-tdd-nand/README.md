This is a simple program that implements a NAND gate. The only interesting thing
about it is that it was developed using test-driven development (kind of), using
a Python script as the test script.

## Recommended hardware and software

* A USB cable with a Micro B plug on the device end
* A Nucleo STM32 evaluation board, either a NUCLEO-L4R5ZI or a NUCLEO-L4P5ZG
* Two pin-to-pin jumper wires
* pyocd version 0.36.0

## Instructions

1. Make the following connections using the jumper wires:
    * PC0 CN9-3 (labeled as A1) to PC3 CN9-5 (labeled as A2)
    * PC1 CN9-7 (labeled as A3) to PC4 CN9-9 (labeled as A4)
2. Open this project using PlatformIO in Visual Studio Code.
3. Connect the host end of the USB cable to your PC, and the device end to the
   ST-LINK USB connector CN1 (**not** the user USB connector CN14).
4. Under PlatformIO / "Project Tasks," open the group for your board (for
   example, the "nucleo_l4r5zi" group), then open the General group and click
   Upload.
5. Run test/test_nand.py.

The Python script test_nand.py will repeatedly do the following, thereby testing
the board and also treating you to a pretty light show:

* Set PC0 and PC1 to random bits.
* Check that PC3 sees input matching PC0, and PC4 sees input matching PC1.
* Check that PB14 (the red LED) outputs the value of PC3, and PC7 (the green
  LED) outputs the value of PC4.
* Check that both PB7 (the blue LED) and PC5 output the NAND of PC3 and PC4.

The testing is performed slowly, so that you can watch and see for yourself that
the green LED is always the NAND of the red and blue LEDs.

Copyright 2023 Tanner Swett.

This file is part of Clawtoast. Clawtoast is free software: you can redistribute
it and/or modify it under the terms of version 3 of the GNU General Public
License as published by the Free Software Foundation.

Clawtoast is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

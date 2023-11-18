This is an experiment in using the ST-Link programmer on one Nucleo board to
program the microcontroller on a different Nucleo board.

## Recommended hardware

* A USB cable with a Micro B plug on the device end
* Two Nucleo STM32 evaluation boards, one NUCLEO-L4R5ZI and one NUCLEO-L4P5ZG
  (or two of one or two of the other)
* A pin-to-pin jumper cable with two wires (preferably brown, red)
* A receptacle-to-receptacle jumper cable with three wires (preferably purple,
  gray, white, black)

## Instructions

1. Designate one Nucleo board as the "host" board and the other one as the
   "target" board.
2. Remove the jumpers from CN4 and JP3 on both boards.
3. Make the following connections between the boards (see e002-wiringdiagram.pdf
   for an illustration):
    * Host CN8-11 to target CN8-11 (GND, brown)
    * Host CN8-9 to target CN8-9 (5V, red)
    * Host CN5-5 to target JP3-2 (NRST, purple)
    * Host CN5-4 to target CN4-4 (SWDIO, gray)
    * Host CN5-3 to target CN5-3 (GND, white)
    * Host CN5-2 to target CN4-2 (SWCLK, black)
4. Open the E001-blinks project using PlatformIO in Visual Studio Code.
5. Connect the host end of the USB cable to your PC, and the device end to the
   host board's ST-LINK USB connector CN1 (**not** the user USB connector CN14).
   At this point, the COM LED LD4 on the host board should be solid red
   (indicating that communication between the PC and the ST-Link on the host
   board has been initialized), and LD4 on the target board should be slowly
   blinking red (indicating that the ST-Link on the target board isn't connected
   to a PC).
6. Under PlatformIO / "Project Tasks," open the group for the *target* board
   (for example, the "nucleo_l4r5zi" group), then open the General group and
   click Upload.

After the project is built and loaded onto the target board, the green LED LD1
on the target board should immediately start blinking.

Copyright 2023 Tanner Swett.

This file is part of Clawtoast. Clawtoast is free software: you can redistribute
it and/or modify it under the terms of version 3 of the GNU General Public
License as published by the Free Software Foundation.

Clawtoast is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

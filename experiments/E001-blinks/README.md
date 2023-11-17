This is a simple program that makes the green LED on a Nucleo board blink
rapidly.

## Recommended hardware

* A USB cable with a Micro B plug on the device end
* A Nucleo STM32 evaluation board, either a NUCLEO-L4R5ZI or a NUCLEO-L4P5ZG

## Instructions

1. Open this project using PlatformIO in Visual Studio Code.
2. Connect the host end of the USB cable to your PC, and the device end to the
   ST-LINK USB connector CN1 (**not** the user USB connector CN14).
3. Under PlatformIO / "Project Tasks," open the group for your board (for
   example, the "nucleo_l4r5zi" group), then open the General group and click
   Upload.

After the project is built and loaded onto the device, the green LED LD1 should
immediately start blinking.

Copyright 2023 Tanner Swett.

This file is part of Clawtoast. Clawtoast is free software: you can redistribute
it and/or modify it under the terms of version 3 of the GNU General Public
License as published by the Free Software Foundation.

Clawtoast is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

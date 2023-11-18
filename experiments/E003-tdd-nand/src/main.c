// Copyright 2023 Tanner Swett.
//
// This file is part of Clawtoast. Clawtoast is free software: you can
// redistribute it and/or modify it under the terms of version 3 of the GNU
// General Public License as published by the Free Software Foundation.
//
// Clawtoast is distributed in the hope that it will be useful, but WITHOUT ANY
// WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
// A PARTICULAR PURPOSE. See the GNU General Public License for more details.

#include "stm32l4xx_hal.h"

int main(void) {
    HAL_Init();

    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();



    GPIO_InitTypeDef GPIO_InitStruct;

    // Configure PC3 and PC4 as inputs with pull-up resistors.

    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;

    GPIO_InitStruct.Pin = GPIO_PIN_3 | GPIO_PIN_4;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

    // Configure PC0, PC1, and PC5 as low-speed open-drain outputs with pull-up
    // resistors.

    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

    GPIO_InitStruct.Pin = GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_5;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

    // Configure PB7, PB14, and PC7 as low-speed push-pull outputs.

    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

    GPIO_InitStruct.Pin = GPIO_PIN_7 | GPIO_PIN_14;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    GPIO_InitStruct.Pin = GPIO_PIN_7;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);



    while (1) {
        // Echo PC3 on PB14, and PC4 on PC7.
        GPIO_PinState pc3 = HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_3);
        GPIO_PinState pc4 = HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_4);

        HAL_GPIO_WritePin(GPIOB, GPIO_PIN_14, pc3);
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_7, pc4);

        // Write PC3 NAND PC1 on both PC5 and PB7.
        HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, !(pc3 && pc4));
        HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7, !(pc3 && pc4));
    }
}

void SysTick_Handler(void) { }

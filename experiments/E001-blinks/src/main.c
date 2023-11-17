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

    __HAL_RCC_GPIOC_CLK_ENABLE();

    GPIO_InitTypeDef GPIO_InitStruct;

    GPIO_InitStruct.Pin = GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

    while (1) {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_7);

        HAL_Delay(100);
    }
}

void SysTick_Handler(void)
{
    HAL_IncTick();
}

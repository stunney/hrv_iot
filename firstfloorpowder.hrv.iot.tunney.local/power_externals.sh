#!/bin/ash
POWER_GPIO=7
fast-gpio set-output $POWER_GPIO
fast-gpio set $POWER_GPIO 1

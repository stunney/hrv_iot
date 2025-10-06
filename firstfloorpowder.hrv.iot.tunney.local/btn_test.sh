#!/bin/ash
COUNTER=0
BTN_GPIO=6

fast-gpio set-input $BTN_GPIO


while [ $COUNTER -eq 0 ]; do
	sleep 1

	fast-gpio read $BTN_GPIO
		
done

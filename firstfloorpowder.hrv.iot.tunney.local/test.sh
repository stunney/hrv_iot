#!/bin/ash
COUNTER=0
POWER_GPIO=7
DHT_GPIO=0
fast-gpio set-input $DHT_GPIO
fast-gpio set-output $POWER_GPIO

while [ $COUNTER -eq 0 ]; do
	sleep 2
	fast-gpio set $POWER_GPIO 0

	/root/checkHumidity $DHT_GPIO DHT22
	sleep 2
	fast-gpio set $POWER_GPIO 1
	
	sleep 2
	echo sleep 2
	sleep 2
	/root/checkHumidity $DHT_GPIO DHT22
	fast-gpio read $POWER_GPIO
		
done

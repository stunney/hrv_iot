import os
import paho.mqtt.client as mqtt
import omega_gpio
import time
from time import sleep

switch_pin = os.environ['HRV_GPIO_PIN_SWITCH']

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("HRV_IOT/#")
	client.subscribe("$SYS/#")

def on_disconnect(client, userdata, flags, rc):
	print("Disconnected with result code " + str(rc))


def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

print("switch pin == " + str(switch_pin))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("localhost", 1883, 60)
client.loop_start()

last_switch_value = 1

while True:
	switch_value = omega_gpio.readinput(switch_pin)
	if last_switch_value != switch_value:
		last_switch_value = switch_value
		if 0 == last_switch_value:
			print("Button PRESSED")
			client.publish("HRV_IOT/SWITCH_CHANGE", payload="ON", qos=2, retain=False)
		else:
			print("Button DE_PRESSED")
			client.publish("HRV_IOT/SWITCH_CHANGE", payload="OFF", qos=2, retain=False)
	sleep(0.1)
done


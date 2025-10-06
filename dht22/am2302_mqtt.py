#!/usr/bin/python

from subprocess import call
import subprocess
import json
import calendar
import uuid
from datetime import datetime, time

import os
import paho.mqtt.client as mqtt
import omega_gpio
import time
from time import sleep

dht22_pin = os.environ['HRV_GPIO_PIN_DHT22']

print("dht22 pin == " + str(dht22_pin))

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

def on_disconnect(client, userdata, flags, rc):
	print("Disconnected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("localhost", 1883, 60)
client.loop_start()

while True:	
	p = subprocess.Popen("/checkHumidity " + str(dht22_pin) + " DHT22", shell=True, stdout=subprocess.PIPE)
	dim = []
	for line in p.stdout.readlines():
		dim.append(line.decode("UTF-8").rstrip('\n').strip())

	dt = datetime
	print(dt)

	myuuid = str(uuid.uuid4())
	print(id)

	try:

		humidity = dim[0]
		tempInCelcius = dim[1]

		print("Humidity = " + humidity)
		print("Temp (C) = " + tempInCelcius)

		temp_data = {
			'id': myuuid,
			'timestamp': str(dt),
			'celcius': tempInCelcius,
		}

		humid_data = {
			'id': myuuid,
			'timestamp': str(dt),
			'humidity': humidity
		}

		client.publish("HRV_IOT/ENV_TEMPERATURE", payload=json.dumps(temp_data).encode('UTF-8'), qos=2, retain=False)
		client.publish("HRV_IOT/ENV_HUMIDITY", payload=json.dumps(humid_data).encode('UTF-8'), qos=2, retain=False)
	except IndexError:
		print("No data found.")
	finally:
		time.sleep(5)

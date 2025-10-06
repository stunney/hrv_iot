#!/usr/bin/python

import paho.mqtt.client as mqtt
from daemonize import Daemonize

from subprocess import call
import subprocess
import json
import os
from os import sys
import calendar
import uuid
import datetime
import time

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	#client.subscribe("HRV_IOT/SWITCH_CHANGE")
	#client.subscribe("HRV_IOT/ENV_HUMIDITY")
	#client.subscribe("HRV_IOT/ENV_TEMPERATURE")

def return_dht_output():
	try:
		p = subprocess.Popen("/root/checkHumidity 0 DHT22", shell=True, stdout=subprocess.PIPE)
		dim = []
		for line in p.stdout.readlines():
			dim.append(line.decode("UTF-8").rstrip('\n').strip())
		retval = p.wait()

		#print(str(retval))

		if 0 != retval:
			raise Exception("Call to checkHumidity resulted in " + str(retval))

		return dim
	except:
		#print('How did we get here?')
		raise Exception('Error processing DHT checkHumidity output')

def do_main_program():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect("192.168.1.221", 1883, 60)
	client.loop_start()

	while True:	

		try:
			dim = return_dht_output()
			humidity = dim[0]
			tempInCelcius = dim[1]

			#print("Humidity = " + humidity)
			#print("Temp (C) = " + tempInCelcius)

			dt = str(datetime.datetime.now())
			#print(dt)

			myuuid = str(uuid.uuid4())
			#print(myuuid)

			temp_data = {
				'id': myuuid,
				'timestamp': dt,
				'celcius': tempInCelcius,
			}

			humid_data = {
				'id': myuuid,
				'timestamp': dt,
				'humidity': humidity
			}

			client.publish("HRV_IOT/ENV_TEMPERATURE", payload=json.dumps(temp_data).encode('UTF-8'), qos=2, retain=False)
			client.publish("HRV_IOT/ENV_HUMIDITY", payload=json.dumps(humid_data).encode('UTF-8'), qos=2, retain=False)

			time.sleep(5)
		except Exception:
			#print('Error occured')
			time.sleep(10)

if __name__ == '__main__':
	myname=os.path.basename(sys.argv[0])
	pidfile='/tmp/%s' % myname
	daemon = Daemonize(app=myname,pid=pidfile, action=do_main_program)
	daemon.start()

import paho.mqtt.client as mqtt
import bottle
from bottle import request,response, post, get, put, delete

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

@post('/enqueue/<topic>')
def enqueue_message(topic):
	try:
		data = request.json()
	except:
		raise ValueError

	if data is None:
		raise ValueError

	if topic is None:
		raise ValueError

	try:
		publish(topic, payload=data, qos=1, ratain=False)
	except:
		raise ValueError

	pass


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

app = application = bottle.default_app()

if __name__ == '__main__':
	client.connect("localhost", 1883, 60)
	client.loop_start()
	bottle.run(host = '', port = 8080)



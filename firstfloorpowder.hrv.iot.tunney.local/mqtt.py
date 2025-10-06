import paho.mqtt.client as mqtt
import ssl

#local files being imported
import hrv_properties
import mqtt_client_config

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("HRV_IOT/SWITCH_CHANGE")
	client.subscribe("HRV_IOT/ENV_HUMIDITY")
	client.subscribe("HRV_IOT/ENV_TEMPERATURE")

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

print(hrv_properties.HUB_ADDR)

client = mqtt.Client()
mqtt_client_config.mqtt_config_tls(client)
client.on_connect = on_connect
client.on_message = on_message

client.connect(host=hrv_properties.HUB_ADDR, port=hrv_properties.MOSQUITTO_PORT, keepalive=60)

client.loop_start()
client.publish(topic="HRV_IOT/SWITCH_CHANGE",payload="HelloWorld",qos=2, retain=True)
client.loop_stop()
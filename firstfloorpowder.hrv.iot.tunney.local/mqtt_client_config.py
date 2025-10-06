import paho.mqtt.client as mqtt
import ssl

import hrv_properties

def mqtt_config_tls(client):
	client.tls_set(ca_certs=hrv_properties.CA_LIST, certfile=hrv_properties.CERT_CLIENT, keyfile=hrv_properties.KEY_CLIENT, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)



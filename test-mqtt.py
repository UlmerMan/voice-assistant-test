import paho.mqtt.client as mqtt

client = mqtt.Client()

client.connect("192.168.30.9", 1883, 60)

client.publish("main/hm/manuel/rolladen","0")
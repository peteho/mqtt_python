#!/usr/bin/env python

import sys
import time
import paho.mqtt.client as mqttClient
import json

host_name = "broker.example.com"	# Broker address
host_port = 1883									# Broker port
host_user = "mqttuser"						# Connection username
host_pass = "password"						# Connection password

class mqttDomoticz(object):

	def __init__(self, host = host_name, port = host_port, user = host_user, password = host_pass):
		self.client = mqttClient.Client("Python")               #create new instance
		self.client.username_pw_set(user, password=password)    #set username and password
		self.client.on_connect= self.on_connect                      #attach function to callback
		self.client.on_publish = self.on_publish       
		self.client.message_callback_add('domoticz/in', self.on_message)
		self.Connected = False
		
		try:
			print("connecting to: " + host + " " + str(port) + " as user: " + user)
			self.client.connect(host, port=port)          #connect to broker

			self.client.loop_start()        #start the loop
			while self.Connected != True:    #Wait for connection
				time.sleep(0.1)

			#self.client.subscribe("#")

		except Exception as e: print(e)
		#	print("no connection to broker")

	def on_connect(self, client, userdata, flags, rc):
		#global Connected
		if rc == 0:
			if not self.Connected: print("Connected to broker")
			self.Connected = True                #Signal connection
		else:
			print("Connection failed")
			self.Connected = False

	def on_publish(self, client, userdata, result):             #create function for callback
		#print("data published \n")
		pass
			
	def on_message(self, client, userdata, message):
		msgpayload = message.payload.decode('utf-8')
		#print ("Message received: "  + message.topic + " " + msgpayload)

		self.list = []
		self.list = json.loads(msgpayload)

		try:
			if self.list["name"] == "raspi2 light" and self.list["nvalue"] == 1:
				print("raspi2 light on")
			if self.list["name"] == "raspi2 light" and self.list["nvalue"] == 0:
				print("raspi2 light off")

		except:
			#print("no valid mqtt value found")
			pass

	def publish_temp(self, temp):
		self.client.publish("domoticz/in", '{"idx":101,"nvalue":0,"svalue":"' + str(temp) + '"}')

	def publish_humi(self, humi):
		self.client.publish("domoticz/in", '{"idx":102,"nvalue":' + str(int(humi)) + '}')

	def publish_volt(self, volt):
		self.client.publish("domoticz/in", '{"idx":99, "nvalue":0,"svalue":"' + str(volt) + '"}')

	def publish_curr(self, curr):
		self.client.publish("domoticz/in", '{"idx":98, "nvalue":0,"svalue":"' + str(curr) + '"}')
		
def main():
	if len(sys.argv) > 1:
		host = str(sys.argv[1])
		port = int(sys.argv[2])
		user = str(sys.argv[3])
		password = str(sys.argv[4])
		mqtt = mqttDomoticz(host, port, user, password)
	else:
		mqtt = mqttDomoticz()

	mqtt.publish_temp(25.0)
	mqtt.publish_humi(40.0)
	mqtt.publish_volt(12.0)
	mqtt.publish_curr(0.5)

	try:
		time.sleep(100)
	except Exception as e: print(e)

if __name__ == '__main__':
  main()

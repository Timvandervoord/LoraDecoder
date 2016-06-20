#########################################
## Python loraRelayer v. 1.0.0
## @author: Tim van der Voord - tim@vandervoord.nl
## (C) 2016, Tim van der Voord
##
## LoraExample relay server
## Will relay received loraData tot relayr.io cloud platform
## Configuration done in loraExample_config.ini

#import modules
import ConfigParser, sys, SocketServer, select, json, time
import paho.mqtt.client as mqtt
from loradecoder.loraPayLoad import loraPayLoad
from loradecoder.loraPacketDecoder import loraPacketDecoder
from loradecoder.loraExceptions import loraDecoderException
from loradecoder.loraExceptions import loraPayloadException

## Config parser
AppConfig = ConfigParser.ConfigParser()
AppConfig.read('loraExample_config.ini')

## MQTT Delegate object for connection events on Relayr.IO connection
class MqttDelegate(object):
    "A delegate class providing callbacks for an MQTT client."

    def __init__(self, client, credentials):
        self.client = client
        self.credentials = credentials

    def on_connect(self, client, userdata, flags, rc):
        print('Connected.')
        # self.client.subscribe(self.credentials['topic'].encode('utf-8'))
        self.client.subscribe(self.credentials['topic'] + 'cmd')

    def on_message(self, client, userdata, msg):
        print('Command received: %s' % msg.payload)

    def on_publish(self, client, userdata, mid):
        print('Message published.')

## The handler for handling the client data
class loraRequestHandler(SocketServer.BaseRequestHandler):
	## Data handler
	def handle(self):
		try:
		  # self.request is the TCP socket connected to the client
			self.data = self.request.recv(1024).strip()
			# Print client ID in debug mode
			if AppConfig.getint('APPLICATION', 'DEBUG') == 1:
				print "{} wrote: {}".format(self.client_address[0], self.data)
			# Create loraPacketDecoder
			lpD = loraPacketDecoder(self.data)
			# Get device format
			lpD.setFormat(self.getDevFormat())
			# Print payload
			self.relayData(lpD)
		except Exception, ex:
			raise loraDecoderException(ex)
  
	## Set-up device format
	def getDevFormat(self):
		if AppConfig.has_option('DEVICE_00000000ABBA0005', 'PAYLOAD_MEANINGS') and AppConfig.has_option('DEVICE_00000000ABBA0005', 'PAYLOAD_BYTES')  and AppConfig.has_option('DEVICE_00000000ABBA0005', 'PAYLOAD_DATATYPES'):
 			## Gather configuration and perform some checks
			pMeanings = AppConfig.get('DEVICE_00000000ABBA0005', 'PAYLOAD_MEANINGS').split(",")
			pBytes = AppConfig.get('DEVICE_00000000ABBA0005', 'PAYLOAD_BYTES').split(",")
			pTypes = AppConfig.get('DEVICE_00000000ABBA0005', 'PAYLOAD_DATATYPES').split(",")
			if not len(pMeanings) == len(pBytes):
				raise Exception("Device configuration incomplete, less bytes than meanings?")
			if not len(pMeanings) == len(pTypes):
				raise Exception("Device configuration incomplete, less datatypes than meanings?")
			## Now make the loraPayLoad class
			lpFormat = loraPayLoad()
			for m in pMeanings:
				i = pMeanings.index(m)
				b = pBytes[i]
				t = pTypes[i]
				lpFormat.addItem(str(m), int(b,0), str(t))
			## Return format
			return lpFormat
		else:
			raise loraDecoderException('Configuration for device incomplete')

	## Relay data to Relayr.IO loradevice
	def relayData(self, lpD):

		## Setup credentials
		clientID = AppConfig.get('RELAYR.IO', 'RELAYR_CLIENTID')
		userName = AppConfig.get('RELAYR.IO', 'RELAYR_USERNAME')
		password = AppConfig.get('RELAYR.IO', 'RELAYR_PASSWORD')
		deviceID = AppConfig.get('DEVICE_00000000ABBA0005', 'RELAYR_DEVICE_ID')
		credentials = {
			'clientId':	clientID,
			'user': userName,
			'password': password,
			'topic': '/v1/'+deviceID+'/',
			'server': 'mqtt.relayr.io',
			'port': 1883
		}

		## Setup connection
		client = mqtt.Client(client_id=credentials['clientId'])
		delegate = MqttDelegate(client, credentials)
		client.on_connect = delegate.on_connect
		client.on_message = delegate.on_message
		client.on_publish = delegate.on_publish
		user, password = credentials['user'], credentials['password']
		client.username_pw_set(user, password)

		## Connect
		try:
			print('Connecting to mqtt server.')
			server, port = credentials['server'], credentials['port']
			client.connect(server, port=port, keepalive=60)
		except:
			print('Connection failed, check your credentials!')
			return

		## Publish common data
		message = { 'meaning': 'LrrLAT', 'value': lpD.getLatitude() }
		client.publish(credentials['topic'] +'data', json.dumps(message))
		time.sleep(0.2)
		message = { 'meaning': 'LrrLON', 'value': lpD.getLongtitude() }
		client.publish(credentials['topic'] +'data', json.dumps(message))
		time.sleep(0.2)
		message = { 'meaning': 'DeviceUID', 'value': lpD.getUID() }
		client.publish(credentials['topic'] +'data', json.dumps(message))
		time.sleep(0.2)
		message = { 'meaning': 'CustomerID', 'value': lpD.getCustomerID() }
		client.publish(credentials['topic'] +'data', json.dumps(message))
		time.sleep(0.2)
		message = { 'meaning': 'CustomerData', 'value': lpD.getCustomerData() }
		client.publish(credentials['topic'] +'data', json.dumps(message))
		time.sleep(0.2)
		message = { 'meaning': 'LastUpdate', 'value': unicode(lpD.getTime()) }
		client.publish(credentials['topic'] +'data', json.dumps(message))
		time.sleep(0.2)
		message = { 'meaning': 'RSSI', 'value': lpD.getRSSI() }
		client.publish(credentials['topic'] +'data', json.dumps(message))
		time.sleep(0.2)

		## Publish the received data
		for (key, value) in lpD.getPayloadItems().iteritems():
			message = {
				'meaning': key,
				'value': value
			}
			client.publish(credentials['topic'] +'data', json.dumps(message))
			time.sleep(0.2)

## The TCP server for receiving loraRequests
def loraReceiver():
	try:
		server = SocketServer.TCPServer((AppConfig.get('APPLICATION', 'HOST'), AppConfig.getint('APPLICATION', 'PORT')), loraRequestHandler, False)
		server.allow_reuse_address = True
		server.server_bind()
		server.server_activate()
		if AppConfig.getint('APPLICATION', 'DEBUG') == 1:
			print "Socketserver started on: {}:{}".format(AppConfig.get('APPLICATION', 'HOST'), AppConfig.get('APPLICATION', 'PORT'))
	except socket.error as msg:
		print 'Can not bind to socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	## Start serving requests
	server.serve_forever()

## Init on calling of this file directly
if __name__ == "__main__":
		loraReceiver()
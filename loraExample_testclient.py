#########################################
## Python loraRelayer v. 1.0.0
## @author: Tim van der Voord - tim@vandervoord.nl
## (C) 2016, Tim van der Voord
##
## Fake client to test the server

# import libraries
import socket, sys, ConfigParser, time

## Config parser
AppConfig = ConfigParser.ConfigParser()
AppConfig.read('loraExample_config.ini')

## Fake data
data = 'HTTP/1.1 200 OK Date: Mon, 27 Jul 2009 12:28:53 GMT Server: Apache/2.2.14 (Win32) Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT Content-Length: 88 Content-Type: text/html Connection: Closed <?xml version="1.0" encoding="UTF-8"?><DevEUI_uplink xmlns="http://uri.actility.com/lora"><Time>2015-06-04T22:25:04.417+02:00</Time><DevEUI>00000000ABBA0005</DevEUI><FPort>10</FPort><FCntUp>10</FCntUp><FCntDn>0</FCntDn><payload_hex>74696d0ded3b347834</payload_hex><mic_hex>b034b910</mic_hex><Lrcid>00000065</Lrcid><LrrRSSI>-76.000000</LrrRSSI><LrrSNR>9.500000</LrrSNR><SpFact>7</SpFact><SubBand>G1</SubBand><Channel>LC3</Channel><DevLrrCnt>1</DevLrrCnt><Lrrid>2900000b</Lrrid><LrrLAT>52.070118</LrrLAT><LrrLON>4.478749</LrrLON><Lrrs><Lrr><Lrrid>2900000b</Lrrid><LrrRSSI>-76.000000</LrrRSSI><LrrSNR>9.500000</LrrSNR></Lrr></Lrrs><CustomerID>100000571</CustomerID><CustomerData>{"alr":{"pro":"MC/IOT","ver":"1"}}</CustomerData></DevEUI_uplink>'

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while 1:
	try:
		# Connect to server and send data
		sock.connect((AppConfig.get('APPLICATION', 'HOST'), AppConfig.getint('APPLICATION', 'PORT')))
		sock.sendall(data)
	finally:
		sock.close()

	print "Sent data"
	time.sleep(120)
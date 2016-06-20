# LoraPacket decoder
Python library for decoding LoraWAN 1.0. protocol messages

## Example usage

The RAW HTTP response data of the LoraWAN concentrator containing the data
```
	RAW_LORA_DATA = 'HTTP/1.1 200 OK Date: Mon, 27 Jul 2009 12:28:53 GMT Server: Apache/2.2.14 (Win32) Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT Content-Length: 88 Content-Type: text/html Connection: Closed <?xml version="1.0" encoding="UTF-8"?><DevEUI_uplink xmlns="http://uri.actility.com/lora"><Time>2015-06-04T22:25:04.417+02:00</Time><DevEUI>00000000ABBA0005</DevEUI><FPort>10</FPort><FCntUp>10</FCntUp><FCntDn>0</FCntDn><payload_hex>74696d0ded3b347834</payload_hex><mic_hex>b034b910</mic_hex><Lrcid>00000065</Lrcid><LrrRSSI>-76.000000</LrrRSSI><LrrSNR>9.500000</LrrSNR><SpFact>7</SpFact><SubBand>G1</SubBand><Channel>LC3</Channel><DevLrrCnt>1</DevLrrCnt><Lrrid>2900000b</Lrrid><LrrLAT>52.070118</LrrLAT><LrrLON>4.478749</LrrLON><Lrrs><Lrr><Lrrid>2900000b</Lrrid><LrrRSSI>-76.000000</LrrRSSI><LrrSNR>9.500000</LrrSNR></Lrr></Lrrs><CustomerID>100000571</CustomerID><CustomerData>{"alr":{"pro":"MC/IOT","ver":"1"}}</CustomerData></DevEUI_uplink>'
```

Define a format for the package. This can also be done after initialization of the decoder class, for example if you wish to select for format based on UID, customerID or customerData
```
	LPformat = loraPayLoad()
```

Define format items as <MEANING>, <NUMBER OF BYTES IN PAYLOAD>, <REPRESENTATION CHOOSE: INT, STRING or FLOAT>
```
	LPformat.addItem('TEMP', 	1, 'INT')  # Add item TEMP that is represented in the first byte as an integer in the payload
	LPformat.addItem('HUM', 	1, 'INT')  	# Add item HUM that is represented in the second byte as an integer in the payload
```

Define a new loraPacketDecoder class
```
	Lp = loraPacketDecoder(RAW_LORA_DATA, LPformat)

	## Lp.setFormat(LPformat) # for setting the format after initialization
```

Print the received data using the format
```
	for (key, value) in lpD.getPayloadItems().iteritems():
		print key, value
```
#########################################
## Python loraDecoder v. 1.0.0
## @author: Tim van der Voord - tim@vandervoord.nl
## (C) 2016, Tim van der Voord
##
## Lora payload class
## will convert data in the payload of the lora package into usable data.
## 
## Using the class:
## l = loraPayLoad() 

from collections import OrderedDict
import struct, binascii
from loradecoder.loraExceptions import loraPayloadException

## Class for processing a packet from an lora device
class loraPayLoad:
	## Contains payload format in correct order
	## example: meaning as key <name for meaning of the data> contains dict -> { numBytes : <number of bytes>, type : <INT | STRING | FLOAT>, startFrom : <byte to start from in payloaddata> }
	payLoadFormat = OrderedDict()
	# count the number of bytes to check incoming payload
	numBytesPayload = 0
	# variable to hold the payload itself
	payLoadData = None

	####
	## initialization
	def __init__(self, format = None):
		## set format of payload from given DICT var using format above 
		if not format == None:
			if isinstance(ele,dict):
				payLoadFormat = format

  ####
  ## get number of bytes
	def getNumbytes(self):
		return self.numBytesPayload

	####
	## set the payload
	def setPayload(self, p):
		if len(p) == self.numBytesPayload*2:
			self.payLoadData = p
		elif len(p) >= self.numBytesPayload*2:
			self.payLoadData = p
		else:
			self.payLoadData = None
			raise loraPayloadException("ERROR: payload data smaller ("+str(len(p))+" bytes) than format ("+str(self.numBytesPayload*2)+" bytes)")

	####
	## return payload data value
	def getValue(self, meaning):
		if meaning in self.payLoadFormat:
			s = self.payLoadFormat[meaning]['startFrom'] * 2
			e = s + self.payLoadFormat[meaning]['numBytes'] * 2
			data = self.payLoadData[s:e]
			if self.payLoadFormat[meaning]['type'] == "INT":
				return int(data, 16)
			if self.payLoadFormat[meaning]['type'] == 'STRING':
				return data.decode("hex")
			if self.payLoadFormat[meaning]['type'] == 'FLOAT':
				return struct.unpack('!f', binascii.unhexlify(data))[0]
			else:
				raise loraPayloadException("Warning: incompatible type format for loraPayLoad")
		else:
			raise loraPayloadException("Warning: meaning "+meaning+" for payload data is not defined")

	####
	## addItem to format dictionary
	def addItem(self, MEANING, NUMBYTES = 1, REPRESENTATION = 'INT'):
		if REPRESENTATION is "FLOAT":
			if NUMBYTES < 4:
				raise loraPayloadException("Warning: for FLOAT type a minimum bytes of 2 is required")
		self.payLoadFormat[MEANING] = { 'numBytes' : NUMBYTES, 'type' : REPRESENTATION, 'startFrom' : self.numBytesPayload }
		self.numBytesPayload = self.numBytesPayload + NUMBYTES

	####
	## Returns a string containing a table with the payload format
	def printFormat(self):
		output = ""
		output += "| LoraPacket payload format"
		output += "| meaning | number of bytes | type | startposition"
		for (key, value) in self.payLoadFormat.items():
			output += "| {} : {} : {} : {}".format(key, str(value['numBytes']), str(value['type']), str(value['startFrom']))
		return output

	####
	## Returns a string containing a table with the payload format and current data
	def printValues(self):
		output = "| LoraPacket payload"
		output += "|-------------------"
		output += "| {:<20} {:<20} {:<10} {:<20} {:<10}".format("meaning","number of bytes","type","startposition","data")
		for (key, value) in self.payLoadFormat.items():
			output += "| {:<20} {:<20} {:<10} {:<20} {:<10}".format(key, str(value['numBytes']), str(value['type']), str(value['startFrom']), self.getValue(key))
		return output

	####
	## returns payload data as associative array
	def getPayload(self):
		if not self.payLoadData == None:
			dataArray = {}
			for (key, value) in self.payLoadFormat.items():
					dataArray[key] = self.getValue(key)
			return dataArray
		else:
			return None
#########################################
## Python loraDecoder v. 1.0.0
## @author: Tim van der Voord - tim@vandervoord.nl
## (C) 2016, Tim van der Voord
##
## Lora packet decoder class

#####
## Excpected LORA PACKET DATA FORMAT
##
## UTC Timestamp
## Local Timestamp: Timestamp translated to browser timezone
## Device UID: Device EUI
## Port: Application port of the message
## Counter UP
## LRR RSSI: RSSI of the received message on LRR side
## LRR SNR: Signal to Noise ratio of the received message on LRR side
## Sp Fact: Spreading Factor
## Sub Band: LoRa sub band used for the message
## Channel: LoRa logical channel used for the message
## LRC Id
## LRR Id: LRR with better SNR
## LRR Lat: LRR latitude
## LRR Long: LRR longitude
## LRR Count: number of LRR receiving the message
## Device Lat: Device latitude
## Device Lon: Device longitude
## LoS Distance (m): distance between the device and the LRR
## Map: displays the device and LRR on a map
## Trip: displays the location path of the device (if device location available)
## Checksum

## XML processing
import xml.etree.ElementTree as ET
import struct
from datetime import datetime
from loradecoder.loraPayLoad import loraPayLoad
from loradecoder.loraExceptions import loraPayloadException
from loradecoder.loraExceptions import loraDecoderException

## Class for processing a packet from an lora device
class loraPacketDecoder:
   #####
   ## The loraWan decoding class
   ##
   ##  Example
   ##  RAW_LORA_DATA = 'HTTP/1.1 200 OK Date: Mon, 27 Jul 2009 12:28:53 GMT Server: Apache/2.2.14 (Win32) Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT Content-Length: 88 Content-Type: text/html Connection: Closed <?xml version="1.0" encoding="UTF-8"?><DevEUI_uplink xmlns="http://uri.actility.com/lora"><Time>2015-06-04T22:25:04.417+02:00</Time><DevEUI>00000000ABBA0005</DevEUI><FPort>10</FPort><FCntUp>10</FCntUp><FCntDn>0</FCntDn><payload_hex>74696d0ded3b347834</payload_hex><mic_hex>b034b910</mic_hex><Lrcid>00000065</Lrcid><LrrRSSI>-76.000000</LrrRSSI><LrrSNR>9.500000</LrrSNR><SpFact>7</SpFact><SubBand>G1</SubBand><Channel>LC3</Channel><DevLrrCnt>1</DevLrrCnt><Lrrid>2900000b</Lrrid><LrrLAT>52.070118</LrrLAT><LrrLON>4.478749</LrrLON><Lrrs><Lrr><Lrrid>2900000b</Lrrid><LrrRSSI>-76.000000</LrrRSSI><LrrSNR>9.500000</LrrSNR></Lrr></Lrrs><CustomerID>100000571</CustomerID><CustomerData>{"alr":{"pro":"MC/IOT","ver":"1"}}</CustomerData></DevEUI_uplink>'
   ##
   ##  Lp = loraPacketDecoder(RAW_LORA_DATA)
   ##  LPformat = loraPayLoad()
   ##  LPformat.addItem('TEMP', 1, 'INT')  # Add item TEMP that is represented in the first byte as an integer in the payload
   ##  LPformat.addItem('HUM', 1, 'INT')  # Add item HUM that is represented in the second byte as an integer in the payload
   ##  Lp.setFormat(LPformat)
   ##
   ##  Print the received data using the format
   ##   for (key, value) in lpD.getPayloadItems().iteritems():
   ##      print key, value

   rawData = ""
   dataFormat = None
   dataArray = {}

   ####
   ## initialization
   def __init__(self, rawData, dataFormat = None):
      if isinstance(dataFormat, loraPayLoad):
         self.dataFormat = dataFormat
      self.rawData = rawData
      self.processRawData()
   
   #####
   ## Function to process incoming XML data
   def processRawData(self):
     try:
      # find start of data
      startData = self.rawData.find('<?xml version="1.0"')
      if startData < 0:
       return
      self.rawData = self.rawData[startData:]
      # parse XML data
      realData = ET.fromstring(self.rawData)
      # data to dictonary self.dataArray
      for item in realData:
       s = item.tag.find('}');
       name = item.tag[s+1:]
       self.dataArray[name] = item.text
      if isinstance(self.dataFormat, loraPayLoad):
       self.dataFormat.setPayload(self.getPayloadRaw())
     except Exception:
       raise loraDecoderException("Incorrect raw data supplied")
   
   ####
   ## get timestamp of message
   ## loraformat: 2015-06-04T22:25:04.417+02:00
   def getTime(self):
      try:
         time = self.dataArray['Time'][0:19]
         return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S');
      except ValueError:
         loraDecoderException('Error in datetime inside of the loraPacket: ' + ValueError)

   ####
   ## set dataformat used
   def setFormat(self, dataFormat):
      if isinstance(dataFormat, loraPayLoad):
         self.dataFormat = dataFormat
         self.dataFormat.setPayload(self.getPayloadRaw())
      else:
         loraDecoderException("Supplied lora format is not of class loraPayload")

   ####
   ## get dataformat used
   def getFormat(self):
      return self.dataFormat

   ####
   ## get lattitude
   def getLatitude(self):
      return float(self.dataArray['LrrLAT'])

   ####
   ## get lattitude
   def getLongtitude(self):
      return float(self.dataArray['LrrLON'])

   ####
   ## get lora device uid as a HEX string
   def getUID(self):
      return str(self.dataArray['DevEUI'])

   ####
   ## get raw payload data as a HEX string
   def getPayloadRaw(self):
      return str(self.dataArray['payload_hex'])

   ####
   ## get payload value of meaning
   def getPayloadValue(self, meaning):
      if not isinstance(self.dataFormat, loraPayLoad):
         raise loraDecoderException("No dataformat supplied to lora packet decoder")
      return self.dataFormat.getValue(meaning)

   ####
   ## get payload value of meaning
   def getPayloadBytes(self):
      return self.dataFormat.getNumbytes()

   ####
   ## get payload value of meaning
   def getPayloadItems(self):
      return self.dataFormat.getPayload()

   ####
   ## get payload value of meaning
   def printPayload(self):
      return self.dataFormat.printValues()

   ####
   ## get customer ID as string
   def getCustomerID(self):
      return str(self.dataArray['CustomerID'])

   ####
   ## get customer DATA as string
   def getCustomerData(self):
      return str(self.dataArray['CustomerData'])

   ####
   ## get average signal strength
   def getRSSI(self):
      return float(self.dataArray['LrrRSSI'])

   ####
   ## get signal to noise ratio as a float value
   def getSNR(self):
      return float(self.dataArray['LrrSNR'])

   ####
   ## get signal to noise ratio as a float value
   def getPort(self):
      return float(self.dataArray['FPort'])

   ####
   ## returns lora gateway ID as HEX string
   def getLoraGatewayID(self):
      return str(self.dataArray['Lrrid'])

   ####
   ## returns lora concentrator ID as HEX string
   def getLoraGatewayID(self):
      return str(self.dataArray['Lrcid'])

   ####
   ## get any other value than default getters above
   def get(self, varName):
      try:
         return self.dataArray[varName]
      except:
         return None

   ####
   ## get payload data as integer
   ## startByte: byte to start from
   ## numBytes: number of bytes to convert
   def getPayloadDataHex(self, startByte = 0, numBytes = 1):
      return self.dataArray['payload_hex'][startByte:numBytes*2]

   ####
   ## get payload data as integer
   ## startByte: byte to start from
   ## numBytes: number of bytes to convert
   def getPayloadDataInt(self, startByte = 0, numBytes = 1):
      return int(self.dataArray['payload_hex'][startByte:numBytes*2], 16)

   ####
   ## get payload data as string
   ## startByte: byte to start from
   ## numBytes: number of bytes to convert
   def getPayloadDataString(self, startByte = 0, numBytes = 1):
      return self.dataArray['payload_hex'][startByte:numBytes*2].decode("hex")

   ####
   ## get payload data as a floating point 32bit single precision value
   ## startByte: byte to start from
   ## numBytes: number of bytes to convert
   def getPayloadDataFloat(self, startByte = 0, numBytes = 1):
      return struct.unpack('!f', self.dataArray['payload_hex'][startByte:numBytes*2])[0]
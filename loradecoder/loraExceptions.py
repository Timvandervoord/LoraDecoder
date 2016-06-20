"""
This module contains exceptions raised when an operation
on the LoraWAN data fails, 
for example: missing formats, invalid values, etc.

At the moment two exception classes are provided: 
- ``loraPayloadException``: raised for exceptions caused by API calls
- ``loraDecoderException``: raised for other exceptions
"""

class loraPayloadException(Exception):
    """
    LoraPayLoadException
    """

class loraDecoderException(Exception):
    """
    loraDecoderException
    """
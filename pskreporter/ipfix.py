import struct
from time import time

class IPFIX:
    IPFIX_SETID_TEMPLATE_RECORD = 0x02
    IPFIX_SETID_OPTIONS_TEMPLATE_RECORD = 0x03


    def __init__(self):
        self.fields = []
        self.data = b""
        self.message = b""
        self._message = b""


    def _create_ipfix_header(self, timestamp = None, sequence = 0, identifier = 0):
        length = len(self._message)
        length += 16 # Add the length of the IPFIX header

        if timestamp is None:
            timestamp = time()

        return struct.pack("!HHIII", 10, length, int(timestamp), sequence, identifier)

    
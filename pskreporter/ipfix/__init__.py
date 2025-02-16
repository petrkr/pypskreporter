from struct import pack
from time import time

IPFIX_SETID_TEMPLATE_RECORD = 0x02
IPFIX_SETID_OPTIONS_TEMPLATE_RECORD = 0x03


class OptionsTemplateField:
    def __init__(self, fieldId, length, enterpriseNumber, value):
        self._id = fieldId
        self._len = length
        self._enum = enterpriseNumber
        self._value = value

    @property
    def header(self):
        return pack("!HHI", self._id, self._len, self._enum)

    @property
    def data(self):
        if self._len != 0xFFFF:
            raise NotImplementedError("Field without variable lenght is not supported")

        if len(self._value) < 255:
            return pack("!B", len(self._value)) + self._value

        return pack("!BH", 255, len(self._value)) + self._value


class OptionsTemplateRecord():
    def __init__(self, templateId, templateFields, scope = 1):
        self._templateId = templateId
        self._fields = templateFields
        self._scope = scope


    def _generate_header(self):
        length = 0
        length += 4 # Size of header
        length += 6 # Size of record set

        field_data = b""
        for field in self._fields:
            data = field.header
            length += len(data)
            field_data += data

        # Header
        record = pack("!HH", IPFIX_SETID_OPTIONS_TEMPLATE_RECORD, length)

        # Options template header
        record += pack("!HHH", self._templateId, len(self._fields), self._scope)

        # Fields
        record += field_data

        return record


    def _generate_data(self):
        length = 0
        length += 4 # Size of header

        field_data = b""
        for field in self._fields:
            data = field.data
            length += len(data)
            field_data += data

        # Data record header
        record = pack("!HH", self._templateId, length)

        # Field data
        record += field_data

        return record


    @property
    def header(self):
        return self._generate_header()
    

    @property
    def data(self):
        return self._generate_data()


class IPFIX:
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

    
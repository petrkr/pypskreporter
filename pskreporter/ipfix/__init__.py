from struct import pack
from time import time

IPFIX_MESSAGE_VERSION = 0x0A
IPFIX_SETID_TEMPLATE_RECORD = 0x02
IPFIX_SETID_OPTIONS_TEMPLATE_RECORD = 0x03


class DataRecord:
    def __init__(self):
        self._records = b''


    def add_value(self, value, dynamic_length = True):
        record = b''

        if not dynamic_length:
            raise NotImplementedError("Only dynamic length record is supported for now")

        if type(value) == str:
            value = value.encode("UTF-8")

        if len(value) < 255:
            record += pack("!B", len(value))
        else:
            record += pack("!BH", 0xFF, len(value))

        record += value
        self._records += record


    @property
    def record(self):
        return self._records


class DataRecordSet:
    def __init__(self, templateid):
        self._templateid = templateid
        self._records = b''
        self._length = 4 # Tempalte ID + lenght itself


    def add_record(self, data):
        self._length += len(data.record)
        self._records += data.record


    @property
    def data(self):
        length = self._length
        padding = b'\x00' * 2
        length += 2

        header = pack("!HH", self._templateid, length)

        return header + self._records + padding


class OptionsTemplateField:
    def __init__(self, fieldId, length, enterpriseNumber):
        self._id = fieldId
        self._len = length
        self._enum = enterpriseNumber

    @property
    def header(self):
        return pack("!HHI", self._id, self._len, self._enum)


class OptionsTemplateRecord:
    def __init__(self, templateId, templateFields = [], scope = 1):
        self._templateId = templateId
        self._scope = scope

        self._fieldsdata = b''
        self._fieldsnum = 0

        # Size of header + size of record set
        self._length = 10

        for field in [f.header for f in templateFields]:
            print(f"Add field {len(field)}")
            self._length += len(field)
            self._fieldsdata += field
            self._fieldsnum += 1


    def add_field(self, field):
        header = field.header

        self._length += len(header)
        self._fieldsnum += 1
        self._fieldsdata += header


    def _generate_header(self):
        length = self._length

        padding = b'\x00' * 2
        length += 2

        # Header
        record = pack("!HH", IPFIX_SETID_OPTIONS_TEMPLATE_RECORD, length)

        # Options template header
        record += pack("!HHH", self._templateId, self._fieldsnum, self._scope)

        # Fields
        record += self._fieldsdata

        # Padding
        record += padding

        return record


    @property
    def data(self):
        return self._generate_header()


class IPFIXHeader:
    def __init__(self, length, sequence = 0, observation = 0, exporttime=None):
        self._length = length
        self._seq = sequence
        self._obid = observation
        self._time = exporttime


    def _generate_header(self):
        # Version number + Length + Export time + Seq + Observ
        self._length += 16 # Version number
        exporttime = self._time

        if not exporttime:
            exporttime = time()

        # Header
        record = pack("!HHIII", IPFIX_MESSAGE_VERSION, self._length, int(exporttime), self._seq, self._obid)

        return record

    @property
    def data(self):
        return self._generate_header()


class IPFIX:
    def __init__(self):
        self._header = None
        self._sets = []


    def add_set(self, setrecord):
        self._sets.append(setrecord)


    @property
    def data(self):
        data = b''
        length = 0

        for s in self._sets:
            length += len(s.data)
            data += s.data

        header = IPFIXHeader(length).data

        return header + data

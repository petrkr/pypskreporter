from struct import pack
from time import time

IPFIX_MESSAGE_VERSION = 0x0A
IPFIX_SETID_TEMPLATE_RECORD = 0x02
IPFIX_SETID_OPTIONS_TEMPLATE_RECORD = 0x03


class DataRecord:
    def __init__(self):
        self._records = b''


    def add_value(self, value = None, dynamic_length = True):
        record = b''

        if not value and not dynamic_length:
            raise ValueError("Value must be set for fixed fields")

        # Empty dynamic field, just fill zero length
        if not value:
            self._records += b'\x00'
            return


        if type(value) == str:
            value = value.encode("UTF-8")

        if dynamic_length:
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

        # Align DataRecordSet to 4 bytes
        padding = b'\x00' * (-1 * self._length % 4)
        length += len(padding)

        header = pack("!HH", self._templateid, length)

        return header + self._records + padding


class FieldSpecifierFormat:
    def __init__(self, fieldId, length, enterpriseNumber = None):
        self._id = fieldId
        self._len = length
        self._enum = enterpriseNumber

    @property
    def header(self):
        if self._enum:
            return pack("!HHI", self._id, self._len, self._enum)
        else:
            return pack("!HH", self._id, self._len)


class OptionsTemplateRecord:
    def __init__(self, templateId, templateFields = [], scope = 1):
        self._templateId = templateId
        self._scope = scope

        self._fieldsdata = b''
        self._fieldsnum = 0

        # Size of header + size of record set
        self._length = 8

        if scope is not None:
            self._length += 2

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

        padding = b'\x00' * (-1 * self._length % 4)
        length += len(padding)

        # Header
        record = pack("!HH", IPFIX_SETID_TEMPLATE_RECORD if self._scope is None else IPFIX_SETID_OPTIONS_TEMPLATE_RECORD, length)

        # Template Record
        record += pack("!HH", self._templateId, self._fieldsnum)

        # Options Template Record
        if self._scope is not None:
            record += pack("!H", self._scope)

        # Fields
        record += self._fieldsdata

        # Padding
        record += padding

        return record


    @property
    def data(self):
        return self._generate_header()


class TemplateRecord(OptionsTemplateRecord):
    def __init__(self, templateId, templateFields = []):
        super().__init__(templateId, templateFields, None)


class IPFIXHeader:
    def __init__(self, length, sequence = 0, observation = 0, exporttime=None):
        self._length = length
        self._seq = sequence
        self._obid = observation
        self._time = exporttime


    def _generate_header(self):
        # Version number + Length + Export time + Seq + Observ
        length = self._length + 16

        exporttime = self._time

        if not exporttime:
            exporttime = time()

        # Header
        record = pack("!HHIII", IPFIX_MESSAGE_VERSION, length, int(exporttime), self._seq, self._obid)

        return record


    @property
    def data(self):
        return self._generate_header()


class IPFIX:
    def __init__(self, sequence = 0, observation = 0):
        self._header = None
        self._sets = []
        self._seq = sequence
        self._obid = observation


    def add_set(self, setrecord):
        self._sets.append(setrecord)


    @property
    def data(self):
        data = b''
        length = 0

        for s in self._sets:
            length += len(s.data)
            data += s.data

        header = IPFIXHeader(length, self._seq, self._obid).data

        return header + data

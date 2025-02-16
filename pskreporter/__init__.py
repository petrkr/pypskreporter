import struct
import socket
from pskreporter.ipfix import IPFIX, FieldSpecifierFormat, OptionsTemplateRecord, TemplateRecord

class PSKReporter:
    PSK_REPORTER_SERVER = "report.pskreporter.info"
    PSK_REPORTER_PORT = 14739 # TODO: Change to prod port when library is ready, Default dev port for now

    # PSK Reporter Template IDs
    RECEIVER_ID = 0x9992
    SENDER_ID = 0x9993
    ENTERPRISE_ID = 0x0000768F # 30351

    # PSK Reporter Information Elements including Enterprise ID
    SENDER_CALLSIGN = 0x8001
    RECEIVER_CALLSIGN = 0x8002
    SENDER_LOCATOR = 0x8003
    RECEIVER_LOCATOR = 0x8004
    FREQUENCY = 0x8005
    SNR = 0x8006
    IMD = 0x8007
    DECODER_SOFTWARE = 0x8008
    ANTENNA_INFO = 0x8009
    MODE = 0x800A
    INFORMATION_SOURCE = 0x800B
    PERSISTENT_IDENTIFIER = 0x800C
    RIG_INFO = 0x800D

    # Generic Information Elements
    TIME = 0x96


    def __init__(self, server = PSK_REPORTER_SERVER, port = PSK_REPORTER_PORT):
        self._server = server
        self._port = port

        # Define base templates
        self._receiverDataSet = OptionsTemplateRecord(PSKReporter.RECEIVER_ID)
        self._senderDataSet = TemplateRecord(PSKReporter.SENDER_ID)

        # Define mandatory receiver fields
        self._receiverDataSet.add_field(FieldSpecifierFormat(PSKReporter.RECEIVER_CALLSIGN, 0xFFFF, PSKReporter.ENTERPRISE_ID))
        self._receiverDataSet.add_field(FieldSpecifierFormat(PSKReporter.RECEIVER_LOCATOR, 0xFFFF, PSKReporter.ENTERPRISE_ID))
        self._receiverDataSet.add_field(FieldSpecifierFormat(PSKReporter.DECODER_SOFTWARE, 0xFFFF, PSKReporter.ENTERPRISE_ID))

        # Define mandatory sender fields
        self._senderDataSet.add_field(FieldSpecifierFormat(PSKReporter.SENDER_CALLSIGN, 0xFFFF, PSKReporter.ENTERPRISE_ID))
        self._senderDataSet.add_field(FieldSpecifierFormat(PSKReporter.MODE, 0xFFFF, PSKReporter.ENTERPRISE_ID))
        self._senderDataSet.add_field(FieldSpecifierFormat(PSKReporter.INFORMATION_SOURCE, 0xFFFF, PSKReporter.ENTERPRISE_ID))
        self._senderDataSet.add_field(FieldSpecifierFormat(PSKReporter.TIME, 4))

        self._reportQueue = []


    def __str__(self):
        return f"PSKReporter(server={self._server}, port={self._port})"


    def __repr__(self):
        return self.__str__()


    # Method which corespond with DLL
    def reporter_seen_callsign(self, remoteInfo, localInfo):
        print(remoteInfo)
        print(localInfo)

        self._reportQueue.append((remoteInfo, localInfo))


    def _send_psk_report(self):
        """
        Sends a reception reports to PSK Reporter.
        """

        data = b""

        server_address = (self._server, self._port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, server_address)
        sock.close()

import struct


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


    def __init__(self, server = PSK_REPORTER_SERVER, port = PSK_REPORTER_PORT):
        self._server = server
        self._port = port


    def reporter_seen_callsign(self, remoteInfo, localInfo):
        print(remoteInfo)
        print(localInfo)

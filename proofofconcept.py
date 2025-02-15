import socket
import struct
import time


# IPFIX Information Elements
PSK_IPFIX_ENTERPRISEID_BIT = 0x8000

IPFIX_SETID_TEMPLATE_RECORD = 0x02
IPFIX_SETID_OPTIONS_TEMPLATE_RECORD = 0x03

# PSK Reporter IPFIX Information Elements
PSK_IPFIX_RECEIVER_ID = 0x99_92
PSK_IPFIX_SENDER_ID = 0x99_93
PSK_IPFIX_ENTERPRISE_ID = 0x00_00_76_8F

# PSK Reporter Information Elements
PSK_SENDER_CALLSIGN = 0x01
PSK_RECEIVER_CALLSIGN = 0x02
PSK_SENDER_LOCATOR = 0x03
PSK_RECEIVER_LOCATOR = 0x04
PSK_FREQUENCY = 0x05
PSK_SNR = 0x06
PSK_IMD = 0x07
PSK_DECODER_SOFTWARE = 0x08
PSK_ANTENNA_INFO = 0x09
PSK_MODE = 0x0A
PSK_INFORMATION_SOURCE = 0x0B
PSK_PERSISTENT_IDENTIFIER = 0x0C
PSK_RIG_INFO = 0x0D


def create_ipfix_header(message_len, sequence = 0, identifier = 0):
    length = message_len
    length += 16 # Add the length of the IPFIX header

    return struct.pack("!HHIII", 10, length, int(time.time()), sequence, identifier)


# Return header and data for IPFIX message
def get_receiver_callsign_record(callsign):
    field = struct.pack("!HHI", PSK_RECEIVER_CALLSIGN | PSK_IPFIX_ENTERPRISEID_BIT, 0xFFFF, PSK_IPFIX_ENTERPRISE_ID)
    data = struct.pack("!H", len(callsign)) + callsign.encode("utf-8")

    return field, data

# 00 03 00 24 99 92 00 03 00 01
def get_set_record(field_id, fields = [], scope = 0x01, padding_num_bytes = 2):
    length = 0
    length += 4 # Add the length of the set header
    length += 6 # Add the length of the options template header
    length += padding_num_bytes

    field_data = b""

    for field in fields:
        length += len(field)
        field_data += field

    # Set record header
    record = struct.pack("!HH", IPFIX_SETID_OPTIONS_TEMPLATE_RECORD, length)

    # Options template header
    record += struct.pack("!HHH", field_id, len(fields), scope)

    # Field data
    record += field_data

    # Padding
    record += b"\x00" * padding_num_bytes

    return record


def get_data_record(field_id, fields, padding_num_bytes = 2):
    length = 0
    length += 4 # Add the length of the set header
    length += padding_num_bytes

    field_data = b""

    for field in fields:
        length += len(field)
        field_data += field

    # Data record header
    record = struct.pack("!HH", field_id, length)

    # Field data
    record += field_data

    # Padding
    record += b"\x00" * padding_num_bytes
    
    return record


def create_ipfix_message():
    fields = []
    fields.append(get_receiver_callsign_record("TESTCALL"))

    data = get_set_record(PSK_IPFIX_RECEIVER_ID, [ f[0] for f in fields ])
    data += get_data_record(PSK_IPFIX_RECEIVER_ID, [ f[1] for f in fields ])
    message = create_ipfix_header(len(data))
    message += data
    return message


def send_psk_report(ipfx_message):
    """
    Sends a reception report to PSK Reporter.
    """
    
    server_address = ('127.0.0.1', 14739)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(ipfx_message, server_address)
    sock.close()

ipfx_message = create_ipfix_message()
print(ipfx_message)
send_psk_report(ipfx_message)

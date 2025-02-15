import socket
import struct
import time



def create_ipfix_message(sender_callsign, receiver_callsign, frequency, snr, mode, grid_locator):
    """
    Constructs a simple IPFIX message to send reception data to PSK Reporter.
    """
    # IPFIX Header (Version 10, Length placeholder, Export Time, Sequence Number, Observation ID)
    ipfix_header = struct.pack("!HHIII", 10, 0, int(time.time()), 0, 0)
    
    message = ipfix_header
    message = message[:2] + struct.pack("!H", len(message)) + message[4:]
    
    return message

def send_psk_report(sender_callsign, receiver_callsign, frequency, snr, mode, grid_locator):
    """
    Sends a reception report to PSK Reporter.
    """
    message = create_ipfix_message(sender_callsign, receiver_callsign, frequency, snr, mode, grid_locator)
    
    server_address = ('report.pskreporter.info', 14739)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, server_address)
    sock.close()

send_psk_report("", "", 14074000, -10, "FT8", "")

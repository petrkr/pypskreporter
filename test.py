import socket

from pskreporter import PSKReporter
from pskreporter.remoteinfo import RemoteInfo
from pskreporter.localinfo import LocalInfo

from pskreporter.ipfix import OptionsTemplateField, OptionsTemplateRecord, DataRecord, DataRecordSet, IPFIX
from struct import pack


def send_psk_report(ipfx_message):
    """
    Sends a reception report to PSK Reporter.
    """

    server_address = ('report.pskreporter.info', 14739)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(ipfx_message, server_address)
    sock.close()


def main():
    remote = RemoteInfo("OK1PKR-REMOTE", 14095, "FREEDV", -3, "JO70FC")
    local = LocalInfo("OK1PKR-LOCAL", "JO70FC", "PyPSKReporter", "0.0.1", "35.89421911 139.94637467", "Antenna in trees")

    # Use development port
    # Check https://pskreporter.info/cgi-bin/psk-analysis.pl for reports
    pskr = PSKReporter("report.pskreporter.info", 14739)

    print(pskr)

    pskr.reporter_seen_callsign(remote, local)

    # Define template fields
    field_receivercall = OptionsTemplateField(PSKReporter.RECEIVER_CALLSIGN, 0xFFFF, 0x0000768F)
    field_receivergrid = OptionsTemplateField(PSKReporter.RECEIVER_LOCATOR, 0xFFFF, 0x0000768F)
    field_decodersw = OptionsTemplateField(PSKReporter.DECODER_SOFTWARE, 0xFFFF, 0x0000768F)

    field_sendercall = OptionsTemplateField(PSKReporter.SENDER_CALLSIGN, 0xFFFF, 0x0000768F)
    field_sendergrid = OptionsTemplateField(PSKReporter.SENDER_LOCATOR, 0xFFFF, 0x0000768F)
    field_snr = OptionsTemplateField(PSKReporter.SNR, 0xFFFF, 0x0000768F)

    print(f"Receivercall field: {field_receivercall.header}")
    print(f"Receivergrid field: {field_receivergrid.header}")
    print(f"Decodersw field: {field_decodersw.header}")

    print(f"Sendercall field: {field_sendercall.header}")
    print(f"Sendergrid field: {field_sendergrid.header}")
    print(f"Sendergrid field: {field_snr.header}")

    # Define template based on fields
    template1 = OptionsTemplateRecord(0x9992)
    template1.add_field(field_receivercall)
    template1.add_field(field_receivergrid)
    template1.add_field(field_decodersw)

    # Define template based on fields
    template2 = OptionsTemplateRecord(0x9993)
    template2.add_field(field_sendercall)
    template2.add_field(field_sendergrid)
    template2.add_field(field_snr)

    print(f"Template1 record: {template1.data}")
    print(f"Template2 record: {template2.data}")

    # Add values to template 0x9992
    dataset1 = DataRecordSet(0x9992)
    dataset2 = DataRecordSet(0x9993)

    # Create one data record
    record1 = DataRecord()
    record1.add_value("TESTCALL-1")
    record1.add_value("JO70FC")
    record1.add_value("PyPSK Reporter v0.0.1")

    record2 = DataRecord()
    record2.add_value("TESTCALL-2")
    record2.add_value("JO70QM")
    record2.add_value(pack("!b", -15))

    record3 = DataRecord()
    record3.add_value("TESTCALL-3")
    record3.add_value("JO70FC")
    record3.add_value(pack("!b", -2))

    print(f"Record 1: {record1.record}")
    print(f"Record 2: {record2.record}")
    print(f"Record 3: {record3.record}")

    # Add records to dataset
    dataset1.add_record(record1)
    dataset2.add_record(record2)
    dataset2.add_record(record3)

    print (f"Record Data set: {dataset1.data}")
    print (f"Record Data set: {dataset2.data}")

    payload = IPFIX()

    # Add templates
    payload.add_set(template1)
    payload.add_set(template2)

    # Add data for this tempalte
    payload.add_set(dataset1)
    payload.add_set(dataset2)

    # whole IPFix packet
    print(f"Whole IPFIX packet ({len(payload.data)}): {payload.data}")

    send_psk_report(payload.data)

if __name__ == "__main__":
    main()

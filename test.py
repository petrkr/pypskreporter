import socket

from pskreporter import PSKReporter
from pskreporter.remoteinfo import RemoteInfo
from pskreporter.localinfo import LocalInfo

from pskreporter.ipfix import OptionsTemplateField, OptionsTemplateRecord, DataRecord, DataRecordSet, IPFIX

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
    field_receivercall = OptionsTemplateField(0x8002, 0xFFFF, 0x0000768F)
    field_receivergrid = OptionsTemplateField(0x8004, 0xFFFF, 0x0000768F)

    print(f"Receivercall field: {field_receivercall.header}")
    print(f"Receivergrid field: {field_receivergrid.header}")

    # Define template based on fields
    template = OptionsTemplateRecord(0x9992, [field_receivercall])
    template.add_field(field_receivergrid)

    print(f"Template record: {template.data}")

    # Add values to template 0x9992
    dataset = DataRecordSet(0x9992)

    # Create one data record
    record1 = DataRecord()
    record1.add_value("TESTCALL-1")
    record1.add_value("JO70FC")

    record2 = DataRecord()
    record2.add_value("TESTCALL-2")
    record2.add_value("JO70QM")

    print(f"Record 1: {record1.record}")
    print(f"Record 2: {record2.record}")

    # Add records to dataset
    dataset.add_record(record1)
    dataset.add_record(record2)

    print (f"Record Data set: {dataset.data}")

    payload = IPFIX()

    # Add field template
    payload.add_set(template)

    # Add data for this tempalte
    payload.add_set(dataset)

    # whole IPFix packet
    print(f"Whole IPFIX packet ({len(payload.data)}): {payload.data}")

    send_psk_report(payload.data)

if __name__ == "__main__":
    main()

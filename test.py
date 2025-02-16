from pskreporter import PSKReporter
from pskreporter.remoteinfo import RemoteInfo
from pskreporter.localinfo import LocalInfo

from pskreporter.ipfix import OptionsTemplateField, OptionsTemplateRecord

def main():
    remote = RemoteInfo("OK1PKR-REMOTE", 14095, "FREEDV", -3, "JO70FC")
    local = LocalInfo("OK1PKR-LOCAL", "JO70FC", "PyPSKReporter", "0.0.1", "35.89421911 139.94637467", "Antenna in trees")

    # Use development port
    # Check https://pskreporter.info/cgi-bin/psk-analysis.pl for reports
    pskr = PSKReporter("report.pskreporter.info", 14739)

    print(pskr)

    pskr.reporter_seen_callsign(remote, local)

    field1 = OptionsTemplateField(0x8001, 0xFFFF, 0x0000768F, "OK1PKR-SND".encode("UTF-8"))
    field2 = OptionsTemplateField(0x8002, 0xFFFF, 0x0000768F, "OK1PKR-RCV".encode("UTF-8"))
    print(field1.get_header())
    print(field1.get_data())

    print(field2.get_header())
    print(field2.get_data())

    record = OptionsTemplateRecord(0x9992, [field1, field2])

    print(record.header)
    print(record.data)


if __name__ == "__main__":
    main()

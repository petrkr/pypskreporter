from pskreporter import PSKReporter
from pskreporter.remoteinfo import RemoteInfo
from pskreporter.localinfo import LocalInfo


def main():
    remote = RemoteInfo("OK1PKR-REMOTE", 14095, "FREEDV", -3, "JO70FC")
    local = LocalInfo("OK1PKR-LOCAL", "JO70FC", "PyPSKReporter", "0.0.1", "35.89421911 139.94637467", "Antenna in trees")

    # Use development port
    # Check https://pskreporter.info/cgi-bin/psk-analysis.pl for reports
    pskreporter = PSKReporter("report.pskreporter.info", 14739)

    print(pskreporter)

    pskreporter.reporter_seen_callsign(remote, local)


if __name__ == "__main__":
    main()

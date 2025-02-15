from pskreporter import PSKReporter
from pskreporter.remoteinfo import RemoteInfo
from pskreporter.localinfo import LocalInfo


def main():
    remote = RemoteInfo("OK1PKR-REMOTE", 14095, "FREEDV", -3, "JO70FC")
    local = LocalInfo("OK1PKR-LOCAL", "JO70FC", "35.89421911 139.94637467", "PyPSKReporter", "0.0.1")

    print("Remote: ", remote)
    print("Local: ", local)


if __name__ == "__main__":
    main()

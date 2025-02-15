# Python PSKReporter

Library to send data to  PSKReporter


### IPFIX Header
`00 0A ll ll tt tt tt tt ss ss ss ss ii ii ii ii`

 - `00 0A` - Version 10
 - `ll ll` is the two byte length code that is the length of the entire datagram
 - `tt tt tt tt` is the transmission time in UNIX timestamp
 - `ss ss ss ss` is the sequence number.
 - `ii ii ii ii` is a random identifier


### Example record header data

```text
00 03 00 24 99 92 00 03 00 01
80 02 FF FF 00 00 76 8F
80 04 FF FF 00 00 76 8F
80 08 FF FF 00 00 76 8F
00 00
```

- `00 03 00 24` - Set header
  - `00 03` - Option template set
  - `00 24` - Length of set including in bytes
- `99 92 00 03 00 01` - Option record set
  - `99 92` - Template ID (ReceiverCallsign)
  - `00 03` - There are 3 fields
  - `00 01` - Scope 1

- `80 02 FF FF 00 00 76 8F` Field 1
  - `80 02` - Receiver callsign attribute with enterprise bit 0x80
  - `FF FF` - Field Length
  - `00 00 76 8F` - Enterprise ID 30351
- `80 04 FF FF 00 00 76 8F` Field 2
  - `80 04` - Receiver Location attribute with enterprise bit 0x80
  - `FF FF` - Field has variable Length
  - `00 00 76 8F` - Enterprise ID 30351
- `80 08 FF FF 00 00 76 8F` Field 3
  - `80 08` - decoder Software attribute with enterprise bit 0x80
  - `FF FF` - Field has variable Length
  - `00 00 76 8F` - Enterprise ID 30351
- `00 00` - padding


### Fields

| Field Name            | Code     | Type                  | Description |
|-----------------------|---------|-----------------------|-------------|
| senderCallsign       | 30351.1 | string                | The callsign of the sender of the transmission. |
| receiverCallsign     | 30351.2 | string                | The callsign of the receiver of the transmission. |
| senderLocator       | 30351.3 | string                | The locator of the sender of the transmission. |
| receiverLocator     | 30351.4 | string                | The locator of the receiver of the transmission. |
| frequency          | 30351.5 | unsignedInteger       | The frequency of the transmission in Hertz. |
| sNR               | 30351.6 | integer               | The signal-to-noise ratio of the transmission. Normally 1 byte. |
| iMD               | 30351.7 | integer               | The intermodulation distortion of the transmission. Normally 1 byte. |
| decoderSoftware   | 30351.8 | string                | The name and version of the decoding software. |
| antennaInformation | 30351.9 | string                | A freeform description of the receiving antenna. |
| mode              | 30351.10 | string                | The mode of the communication. One of the ADIF values for MODE or SUBMODE. |
| informationSource | 30351.11 | integer               | Identifies the source of the record. The bottom 2 bits have the following meaning: 1 = Automatically Extracted. 2 = From a Call Log (QSO). 3 = Other Manual Entry. The 0x80 bit indicates that this record is a test transmission. Normally 1 byte. |
| persistentIdentifier | 30351.12 | string                | Random string that identifies the sender. This may be used in the future as a primitive form of security. |
| flowStartSeconds  | 150      | dateTimeSeconds (Integer) | The time of the transmission (absolute seconds since 1/1/1970). |
| rigInformation    | 30351.13 | string                | A description of the Rig in use. Preferably include most significant information first so entries can be grouped automatically. |

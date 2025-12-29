---
applyTo: '**'
---
This file contains the markdown ONIX specification for Header.

# ONIX for Books Message header

## Header composite

A group of data elements which together constitute a message header giving information about the message itself. Mandatory in any ONIX for Books message to provide metadata about the message itself, and non-repeating.

| Field          | Value   |
|----------------|---------|
| Reference name | Header  |
| Short tag      | header  |
| Cardinality    | 1       |

## Sender composite

A group of data elements which together specify the sender of an ONIX for Books message. Mandatory in any ONIX for Books message, and non-repeating.

| Field          | Value  |
|----------------|--------|
| Reference name | Sender |
| Short tag      | sender |
| Cardinality    | 1      |

### Sender identifier composite

A group of data elements which together define an identifier of the sender. The composite is optional, and repeatable if more than one identifier of different types is sent; but either a `<SenderName>` or a `<SenderIdentifier>` must be included.

| Field          | Value            |
|----------------|------------------|
| Reference name | SenderIdentifier |
| Short tag      | senderidentifier |
| Cardinality    | 0…n              |

#### H.1 Sender identifier type

An ONIX code identifying a scheme from which an identifier in the `<IDValue>` element is taken. Mandatory in each occurrence of the `<SenderIdentifier>` composite, and non-repeating.

| Field          | Value                     |
|----------------|---------------------------|
| Format         | Fixed length, two digits  |
| Code list      | List 44                   |
| Reference name | SenderIDType              |
| Short tag      | m379                      |
| Cardinality    | 1                         |
| Example        | `<m379>01</m379>`         |

#### H.2 Identifier type name

A name which identifies a proprietary identifier scheme (ie a scheme which is not a standard and for which there is no individual ID type code). Must be used when, and only when, the code in the `<SenderIDType>` element indicates a proprietary scheme. Optional and non-repeating.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | Variable length text, suggested maximum 100 characters         |
| Reference name | IDTypeName                                                     |
| Short tag      | b233                                                           |
| Cardinality    | 0…1                                                            |
| Attributes     | language                                                       |

#### H.3 Identifier value

An identifier of the type specified in the `<SenderIDType>` element. Mandatory in each occurrence of the `<SenderIdentifier>` composite, and non-repeating.

| Field          | Value                                                      |
|----------------|------------------------------------------------------------|
| Format         | According to the identifier type specified in `<SenderIDType>` |
| Reference name | IDValue                                                    |
| Short tag      | b244                                                       |
| Cardinality    | 1                                                          |

#### H.4 Sender name

The name of the sender organization, which should always be stated in a standard form agreed with the addressee. Optional and non-repeating; but either a `<SenderName>` element or a `<SenderIdentifier>` composite must be included.

| Field          | Value                                                  |
|----------------|--------------------------------------------------------|
| Format         | Variable length text, suggested maximum 50 characters  |
| Reference name | SenderName                                             |
| Short tag      | x298                                                   |
| Cardinality    | 0…1                                                    |
| Example        | `<SenderName>HarperCollins London</SenderName>`        |

#### H.5 Sender contact name

Free text giving the name, department, etc for a contact person in the sender organization who is responsible for the content of the message. Optional and non-repeating.

| Field          | Value                                                    |
|----------------|----------------------------------------------------------|
| Format         | Variable length text, suggested maximum 300 characters   |
| Reference name | ContactName                                              |
| Short tag      | x299                                                     |
| Cardinality    | 0…1                                                      |
| Example        | `<x299>Jackie Brown</x299>`                              |

#### H.5a Sender telephone number

A telephone number of the contact person in the sender organization, wherever possible including the plus sign and the international dialing code. Optional, and non-repeating.

| Field          | Value                                                  |
|----------------|--------------------------------------------------------|
| Format         | Variable length text, suggested maximum 20 characters  |
| Reference name | TelephoneNumber                                        |
| Short tag      | j270                                                   |
| Cardinality    | 0…1                                                    |
| Example        | `<j270>+44 20 7946 0921</j270>`                        |

#### H.6 Sender contact e-mail address

A text field giving the e-mail address for a contact person in the sender organization who is responsible for the content of the message. Optional and non-repeating.

| Field          | Value                                                   |
|----------------|---------------------------------------------------------|
| Format         | Variable length text, suggested maximum 100 characters  |
| Reference name | EmailAddress                                            |
| Short tag      | j272                                                    |
| Cardinality    | 0…1                                                     |
| Example        | `<j272>jackie.brown@bigpublisher.co.uk</j272>`          |

## Addressee composite

A group of data elements which together specify the addressee of an ONIX for Books message. Optional, and repeatable if there are several addressees.

| Field          | Value     |
|----------------|-----------|
| Reference name | Addressee |
| Short tag      | addressee |
| Cardinality    | 0…n       |

### Addressee identifier composite

A group of data elements which together define an identifier of the addressee. The composite is optional, and repeatable if more than one identifier of different types for the same addressee is sent; but either an `<AddresseeName>` or an `<AddresseeIdentifier>` must be included.

| Field          | Value                 |
|----------------|-----------------------|
| Reference name | AddresseeIdentifier   |
| Short tag      | addresseeidentifier   |
| Cardinality    | 0…n                   |

#### H.7 Addressee identifier type

An ONIX code identifying a scheme from which an identifier in the `<IDValue>` element is taken. Mandatory in each occurrence of the `<AddresseeIdentifier>` composite, and non-repeating.

| Field          | Value                                         |
|----------------|-----------------------------------------------|
| Format         | Fixed length, two digits                      |
| Code list      | List 44                                       |
| Reference name | AddresseeIDType                               |
| Short tag      | m380                                          |
| Cardinality    | 1                                             |
| Example        | `<AddresseeIDType>02</AddresseeIDType>`       |

#### H.8 Identifier type name

A name which identifies a proprietary identifier scheme (ie a scheme which is not a standard and for which there is no individual ID type code). Must be used when, and only when, the code in the `<AddresseeIDType>` element indicates a proprietary scheme. Optional and non-repeating.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | Variable length text, suggested maximum 100 characters         |
| Reference name | IDTypeName                                                     |
| Short tag      | b233                                                           |
| Cardinality    | 0…1                                                            |
| Attributes     | language                                                       |
| Example        | `<b233>BigPublisher Customer ID</b233>`                        |

#### H.9 Identifier value

An identifier of the type specified in the `<AddresseeIDType>` element. Mandatory in each occurrence of the `<AddresseeIdentifier>` composite, and non-repeating.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | According to the identifier type specified in `<AddresseeIDType>` |
| Reference name | IDValue                                                        |
| Short tag      | b244                                                           |
| Cardinality    | 1                                                              |

#### H.10 Addressee name

The name of the addressee organization, which should always be stated in a standard form agreed with the addressee. Optional and non-repeating; but either a `<AddresseeName>` element or a `<AddresseeIdentifier>` composite must be included.

| Field          | Value                                                  |
|----------------|--------------------------------------------------------|
| Format         | Variable length text, suggested maximum 50 characters  |
| Reference name | AddresseeName                                          |
| Short tag      | x300                                                   |
| Cardinality    | 0…1                                                    |
| Example        | `<x300>BiblioAggregator Ltd</x300>`                    |

#### H.11 Addressee contact name

Free text giving the name, department etc for a contact person in the addressee organization to whom the message is to be directed. Optional and non-repeating.

| Field          | Value                                                    |
|----------------|----------------------------------------------------------|
| Format         | Variable length text, suggested maximum 300 characters   |
| Reference name | ContactName                                              |
| Short tag      | x299                                                     |
| Cardinality    | 0…1                                                      |
| Example        | `<ContactName>Mel Carter</ContactName>`                  |

#### H.11a Addressee telephone number

A telephone number of the contact person in the addressee organization, wherever possible including the plus sign and the international dialing code. Optional, and non-repeating.

| Field          | Value                                                  |
|----------------|--------------------------------------------------------|
| Format         | Variable length text, suggested maximum 20 characters  |
| Reference name | TelephoneNumber                                        |
| Short tag      | j270                                                   |
| Cardinality    | 0…1                                                    |
| Example        | `<TelephoneNumber>+44 1632 457890</TelephoneNumber>`   |

#### H.12 Addressee contact e-mail address

A text field giving the e-mail address for a contact person in the addressee organization. Optional and non-repeating.

| Field          | Value                                                   |
|----------------|---------------------------------------------------------|
| Format         | Variable length text, suggested maximum 100 characters  |
| Reference name | EmailAddress                                            |
| Short tag      | j272                                                    |
| Cardinality    | 0…1                                                     |
| Example        | `<j272>carterm@aggregator.co.uk</j272>`                 |

## H.13 Message sequence number

A monotonic sequence number of the messages in a series sent between trading partners, to enable the receiver to check against gaps and duplicates. Optional and non-repeating.

| Field          | Value                                                |
|----------------|------------------------------------------------------|
| Format         | Positive integer, suggested maximum length 8 digits  |
| Reference name | MessageNumber                                        |
| Short tag      | m180                                                 |
| Cardinality    | 0…1                                                  |
| Example        | `<m180>1234</m180>`                                  |

## H.14 Message repeat number

A number which distinguishes any repeat transmissions of a message. If this element is used, the original is numbered 1 and repeats are numbered 2, 3 etc. Optional and non-repeating.

| Field          | Value                                                |
|----------------|------------------------------------------------------|
| Format         | Positive integer, suggested maximum length 4 digits  |
| Reference name | MessageRepeat                                        |
| Short tag      | m181                                                 |
| Cardinality    | 0…1                                                  |
| Example        | `<m181>2</m181>`                                     |

## H.15 Message creation date/time

The date on which the message is sent. Optionally, the time may be added, using the 24-hour clock, with an explicit indication of the time zone if required, in a format based on ISO 8601. Mandatory and non-repeating.

| Field          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Format         | Permitted formats, where 'T' and 'Z' represent themselves (ie the letters T and Z), and where the symbol '±' represents either '+' or '-' to indicate a timezone offset from UTC:<br>• `YYYYMMDD` - Date only<br>• `YYYYMMDDThhmm` - Date and time (local time of sender)<br>• `YYYYMMDDThhmmZ` - Universal time (UTC) †<br>• `YYYYMMDDThhmm±hhmm` - With time zone offset from UTC †<br>• `YYYYMMDDThhmmss` - Date and time (with seconds)<br>• `YYYYMMDDThhmmssZ` - Universal time (with seconds)<br>• `YYYYMMDDThhmmss±hhmm` - With time zone offset from UTC (with seconds)<br>† indicates the preferred formats |
| Reference name | SentDateTime                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Short tag      | x307                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Cardinality    | 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Example        | `<x307>20100522T1230Z</x307>` (12.30pm UTC, 22 May 2010)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Notes          | The calendar date must use the Gregorian calendar, even if other dates within the message use a different calendar. For all practical purposes, UTC is the same as GMT.                                                                                                                                                                                                                                                                                                                                                                                                    |

## H.16 Message note

Free text giving additional information about the message. Optional, and repeatable in order to provide a note in multiple languages. The language attribute is optional for a single instance of `<MessageNote>`, but must be included in each instance if `<MessageNote>` is repeated.

| Field          | Value                                                                   |
|----------------|-------------------------------------------------------------------------|
| Format         | Variable length text, suggested maximum 500 characters                  |
| Reference name | MessageNote                                                             |
| Short tag      | m183                                                                    |
| Cardinality    | 0…n                                                                     |
| Attributes     | language                                                                |
| Example        | `<MessageNote>Updates for titles to be published September 2009</MessageNote>` |

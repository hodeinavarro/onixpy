# P.1 Record reference, type and source

Two mandatory data elements must be included at the beginning of every Product record or update. The first, `<RecordReference>`, is a string of text which uniquely identifies the record. The second, `<NotificationType>`, is a code which specifies the type of notification or update. If the record is sent as a deletion, the reason for deletion can optionally be indicated as plain text in `<DeletionText>`. The source of the record can optionally be indicated by one or more of the elements `<RecordSourceType>`, `<RecordSourceIdentifier>` and `<RecordSourceName>`.

## P.1.1 Record reference

For every product, you must choose a single record reference which will uniquely identify the Information record which you send out about that product, and which will remain as its permanent identifier every time you send an update. It doesn't matter what reference you choose, provided that it is unique and permanent. This record reference doesn't identify the product – even though you may choose to use the ISBN or another product identifier as a part of your record reference – it identifies your information record about the product, so that the person to whom you are sending an update can match it with what you have previously sent. It is not recommended to use a product identifier as the whole of the record reference. A good way of generating references which are not part of a recognized product identification scheme but which can be guaranteed to be unique is to prefix a product identifier or a meaningless row ID from your internal database with a reversed Internet domain name which is registered to your organization (reversal prevents the record reference appearing to be a resolvable URL). Alternatively, use a UUID.

| Field          | Value                                                                                                                   |
|----------------|-------------------------------------------------------------------------------------------------------------------------|
| Format         | Variable length alphanumeric, suggested maximum length 100 characters                                                   |
| Reference name | RecordReference                                                                                                         |
| Short tag      | a001                                                                                                                    |
| Cardinality    | 1                                                                                                                       |
| Example        | `<a001>com.xyzpublishers.onix.36036</a001>` (36036 is a row ID in an internal database that is the source of the data in the record) |
| Example        | `<RecordReference>72b32344-01c5-4af2-82aa-4d8d12b0df22</RecordReference>` (a UUID)                                      |

## P.1.2 Notification or update type code

An ONIX code which indicates the type of notification or update which you are sending. Mandatory and non-repeating.

| Field          | Value                                                       |
|----------------|-------------------------------------------------------------|
| Format         | Fixed length, two digits                                    |
| Code list      | List 1                                                      |
| Reference name | NotificationType                                            |
| Short tag      | a002                                                        |
| Cardinality    | 1                                                           |
| Example        | `<NotificationType>02</NotificationType>` (Advance notification) |

## P.1.3 Reason for deletion

Free text which indicates the reason why an ONIX record is being deleted. Optional and repeatable, and may occur only when the `<NotificationType>` element carries the code value 05. The language attribute is optional for a single instance of `<DeletionText>`, but must be included in each instance if `<DeletionText>` is repeated. Note that it refers to the reason why the record is being deleted, not the reason why a product has been 'deleted' (in industries which use this terminology when a product is withdrawn). A product cancellation or abandonment prior to publication, or a product becoming unavailable (eg as a result of being Out of print) are changes of `<PublishingStatus>` or of `<ProductAvailability>`, not reasons for deletion.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 100 characters  |
| Reference name | DeletionText                                                   |
| Short tag      | a199                                                           |
| Cardinality    | 0…n                                                            |
| Attributes     | language                                                       |
| Example        | `<a199>Issued in error</a199>`                                 |

## P.1.4 Record source type code

An ONIX code which indicates the type of source which has issued the ONIX record. Optional and non-repeating, independently of the occurrence of any other field.

| Field          | Value                        |
|----------------|------------------------------|
| Format         | Fixed length, two digits     |
| Code list      | List 3                       |
| Reference name | RecordSourceType             |
| Short tag      | a194                         |
| Cardinality    | 0…1                          |
| Example        | `<a194>01</a194>` (Publisher)|

## Record source identifier composite

A group of data elements which together define an identifier of the organization which is the source of the ONIX record. Optional, and repeatable in order to send multiple identifiers for the same organization.

| Field          | Value                    |
|----------------|--------------------------|
| Reference name | RecordSourceIdentifier   |
| Short tag      | recordsourceidentifier   |
| Cardinality    | 0…n                      |

### P.1.5 Record source identifier type code

An ONIX code identifying the scheme from which the identifier in the `<IDValue>` element is taken. Mandatory in each occurrence of the `<RecordSourceIdentifier>` composite, and non-repeating.

| Field          | Value                                                |
|----------------|------------------------------------------------------|
| Format         | Fixed length, two digits                             |
| Code list      | List 44                                              |
| Reference name | RecordSourceIDType                                   |
| Short tag      | x311                                                 |
| Cardinality    | 1                                                    |
| Example        | `<x311>03</x311>` (Deutsche Bibliothek publisher identifier) |

### P.1.6 Identifier type name

A name which identifies a proprietary identifier scheme (ie a scheme which is not a standard and for which there is no individual ID type code). Used when, and only when, the code in the `<RecordSourceIDType>` element indicates a proprietary scheme. Optional and non-repeating.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 100 characters  |
| Reference name | IDTypeName                                                     |
| Short tag      | b233                                                           |
| Cardinality    | 0…1                                                            |
| Attributes     | language                                                       |
| Example        | `<b233>KNV</b233>`                                             |

### P.1.7 Identifier value

An identifier of the type specified in the `<RecordSourceIDType>` element. Mandatory in each occurrence of the `<RecordSourceIdentifier>` composite, and non-repeating.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | According to the identifier type specified in `<RecordSourceIDType>` |
| Reference name | IDValue                                                        |
| Short tag      | b244                                                           |
| Cardinality    | 1                                                              |
| Example        | `<b244>8474339790</b244>`                                      |

## P.1.8 Record source name

The name of the party which issued the record, as free text. Optional and non-repeating, independently of the occurrence of any other field.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 100 characters  |
| Reference name | RecordSourceName                                               |
| Short tag      | a197                                                           |
| Cardinality    | 0…1                                                            |
| Example        | `<RecordSourceName>Cambridge University Press</RecordSourceName>` |
| Notes          | The record source need not be the same as the `<Sender>` specified in the message header: an aggregator may be the sender of a message containing records sourced from several different record suppliers. |

# P.2 Product identifiers

A valid product identifier must be included in every `<Product>` record. The GTIN-13 (formerly EAN-13) article number is the preferred identifier for international use across a range of product types. Other product numbers may be included where they exist. The XML Schema or DTD requires at least one number to be sent, but does not enforce or rule out any particular types or combinations. In ONIX 3.0, redundant elements have been deleted, so the `<ProductIdentifier>` composite must be used.

## Product identifier composite

A group of data elements which together specify an identifier of a product in accordance with a particular scheme. Mandatory within `<Product>`, and repeatable in order to provide multiple identifiers for the same product. As well as standard identifiers, the composite allows proprietary identifiers (for example SKUs assigned by wholesalers or vendors) to be sent as part of the ONIX record. ISBN-13 numbers in their unhyphenated form constitute a range of GTIN-13 numbers that has been reserved for the international book trade. Effective from 1 January 2007, it was agreed by ONIX national groups that it should be mandatory in an ONIX `<Product>` record for any item carrying an ISBN-13 to include the ISBN-13 labelled as a GTIN-13 number (ie as `<ProductIDType>` code 03), since this is how the ISBN-13 will be used in book trade transactions. For many ONIX applications this will also be sufficient. For some ONIX applications, however, particularly when data is to be supplied to the library sector, there may be reasons why the ISBN-13 must also be sent labelled distinctively as an ISBN-13 (ie as `<ProductIDType>` code 15). Users should consult 'good practice' guidelines and/or discuss with their trading partners. Note that for some identifiers such as ISBN, punctuation (typically hyphens or spaces for ISBNs) is used to enhance readability when printed, but the punctuation is dropped when carried in ONIX data. But for other identifiers – for example DOI – the punctuation is an integral part of the identifier and must always be included.

| Field          | Value              |
|----------------|--------------------|
| Reference name | ProductIdentifier  |
| Short tag      | productidentifier  |
| Cardinality    | 1…n                |

### P.2.1 Product identifier type code

An ONIX code identifying the scheme from which the identifier in the `<IDValue>` element is taken. Mandatory in each occurrence of the `<ProductIdentifier>` composite, and non-repeating.

| Field          | Value                                     |
|----------------|-------------------------------------------|
| Format         | Fixed length, two digits                  |
| Code list      | List 5                                    |
| Reference name | ProductIDType                             |
| Short tag      | b221                                      |
| Cardinality    | 1                                         |
| Example        | `<ProductIDType>03</ProductIDType>` (GTIN-13) |

### P.2.2 Identifier type name

A name which identifies a proprietary identifier scheme (ie a scheme which is not a standard and for which there is no individual ID type code). Must be used when, and only when, the code in the `<ProductIDType>` element indicates a proprietary scheme, eg a wholesaler's own code. Optional and non-repeating.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 100 characters  |
| Reference name | IDTypeName                                                     |
| Short tag      | b233                                                           |
| Cardinality    | 0…1                                                            |
| Attributes     | language                                                       |
| Example        | `<IDTypeName>KNV</IDTypeName>`                                 |

### P.2.3 Identifier value

An identifier of the type specified in the `<ProductIDType>` element. Mandatory in each occurrence of the `<ProductIdentifier>` composite, and non-repeating.

| Field          | Value                                                      |
|----------------|------------------------------------------------------------|
| Format         | According to the identifier type specified in `<ProductIDType>` |
| Reference name | IDValue                                                    |
| Short tag      | b244                                                       |
| Cardinality    | 1                                                          |
| Example        | `<b244>9780300117264</b244>`                               |

## Barcode composite

A group of data elements which together specify a barcode type and its position on a product. Optional: expected to be used only in North America. Repeatable if more than one type of barcode is carried on a single product. The absence of this composite does not mean that a product is not bar-coded.

| Field          | Value    |
|----------------|----------|
| Reference name | Barcode  |
| Short tag      | barcode  |
| Cardinality    | 0…n      |

### P.2.4 Barcode type

An ONIX code indicating whether, and in what form, a barcode is carried on a product. Mandatory in any instance of the `<Barcode>` composite, and non-repeating.

| Field          | Value                                                |
|----------------|------------------------------------------------------|
| Format         | Fixed length, two digits                             |
| Code list      | List 141                                             |
| Reference name | BarcodeType                                          |
| Short tag      | x312                                                 |
| Cardinality    | 1                                                    |
| Example        | `<x312>03</x312>` (GTIN-13+5 – US dollar price encoded) |

### P.2.5 Position on product

An ONIX code indicating a position on a product; in this case, the position in which a barcode appears. Required if the `<BarcodeType>` element indicates that the barcode appears on the product, even if the position is 'unknown'. Omitted if the `<BarcodeType>` element specifies that the product does not carry a barcode. Non-repeating.

| Field          | Value                                                   |
|----------------|---------------------------------------------------------|
| Format         | Fixed length, two digits                                |
| Code list      | List 142                                                |
| Reference name | PositionOnProduct                                       |
| Short tag      | x313                                                    |
| Cardinality    | 0…1                                                     |
| Example        | `<x313>01</x313>` (Cover 4 – the back cover of a book)  |

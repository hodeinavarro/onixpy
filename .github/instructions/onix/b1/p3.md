---
applyTo: '**'
---
This file contains the markdown ONIX specification for Block 1 Section 3.

# Block 1: Product description

## Descriptive detail composite

The descriptive detail block covers data Groups P.3 to P.13, all of which are essentially part of the factual description of the form and content of a product. The block as a whole is non-repeating. It is mandatory in any <Product> record unless the <NotificationType> in Group P.1 indicates that the record is an update notice which carries only those blocks in which changes have occurred.

| Field          | Value               |
|----------------|---------------------|
| Reference name | DescriptiveDetail   |
| Short tag      | descriptivedetail   |
| Cardinality    | 0…1                 |

### Descriptive detail composite > P.3 Product form

Group P.3 carries elements that describe the form of a product, its key content type (text, audio, etc) and, in the case of digital products, any usage constraints that are enforced through DRM protection or otherwise. Additional guidance on the description of digital products in ONIX 3.0 and later will be found in a separate document ONIX for Books Product Information Message: How to Describe Digital Products in ONIX 3 and in other Application notes available from EDItEUR.

#### P.3.1 Product composition

An ONIX code which indicates whether a product consists of a single item or multiple items or components. Mandatory in an occurrence of `<DescriptiveDetail>`, and non-repeating.

| Field          | Value                                   |
|----------------|-----------------------------------------|
| Format         | Fixed length, two digits                |
| Reference name | ProductComposition                      |
| Short tag      | x314                                    |
| Cardinality    | 1                                       |
| Example        | `<x314>00</x314>` (Single-item product) |

#### P.3.2 Product form code

An ONIX code which indicates the primary form of a product. Mandatory in an occurrence of `<DescriptiveDetail>`, and non-repeating. Note that in ONIX 3.0 and later, the handling of multiple-item and multi-component products requires that the form of the contained items or components is specified only in the `<ProductPart>` composite (equivalent to `<Contained Item>` in earlier releases of ONIX. `<ProductPart>` forms Group P.4, and must be included for full description of any multiple-item or multi-component product.

| Field          | Value                                              |
|----------------|-----------------------------------------------------|
| Format         | Fixed length, two letters (or the digits `00`)     |
| Code list      | List 150                                           |
| Reference name | ProductForm                                        |
| Short tag      | b012                                               |
| Cardinality    | 1                                                  |
| Example        | `<ProductForm>BB</ProductForm>` (Hardback book)    |

#### P.3.3 Product form detail

An ONIX code which provides added detail of the medium and/or format of the product. Optional, and repeatable in order to provide multiple additional details.

| Field          | Value                                                                 |
|----------------|-----------------------------------------------------------------------|
| Format         | Fixed length, four characters: one letter followed by three digits    |
| Code list      | List 175                                                              |
| Reference name | ProductFormDetail                                                     |
| Short tag      | b333                                                                  |
| Cardinality    | 0…n                                                                   |
| Example        | `<b333>B206</b333>` (Pop-up book)                                      |

#### Product form feature composite

An optional group of data elements which together describe an aspect of product form that is too specific to be covered in the `<ProductForm>` and `<ProductFormDetail>` elements. Repeatable in order to describe different aspects of the product form.

| Field          | Value               |
|----------------|---------------------|
| Reference name | ProductFormFeature  |
| Short tag      | productformfeature  |
| Cardinality    | 0…n                 |

##### P.3.4 Product form feature type

An ONIX code which specifies the feature described by an instance of the `<ProductFormFeature>` composite, eg binding color. Mandatory in each occurrence of the composite, and non-repeating.

| Field          | Value                                     |
|----------------|-------------------------------------------|
| Format         | Fixed length, two digits                  |
| Code list      | List 79                                   |
| Reference name | ProductFormFeatureType                    |
| Short tag      | b334                                      |
| Cardinality    | 1                                         |
| Example        | `<b334>02</b334>` (Page edge color)       |

##### P.3.5 Product form feature value

A controlled value that describes a product form feature. Presence or absence of this element depends on the `<ProductFormFeatureType>`, since some product form features (eg color of cover binding) require an accompanying value, while some (eg text font) require free text in `<ProductFormFeatureDescription>`. Others may have both code value and free text. Non-repeating.

| Field          | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Format         | Dependent on the scheme specified in `<ProductFormFeatureType>`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Code list      | Dependent on the scheme specified in `<ProductFormFeatureType>`:<br>• For cover binding color, see List 98<br>• For page edge color, see List 98<br>• For special cover material, see List 99<br>• For text font, use free text in `<ProductFormFeatureDescription>`, which should include a font name for the main body text. `<ProductFormFeatureValue>` may include the body text size in points<br>• For DVD region codes, see List 76<br>• For CPSIA choking hazard warning, see List 143<br>• For EU Toy Safety hazard warnings, see List 184<br>• For various paper certification schemes (FSC, PEFC etc), see List 79. `<ProductFormFeatureType>` identifies the certification scheme, and `<ProductFormFeatureValue>` may carry a Chain of Custody (COC) number<br>• For certified recycled paper, a separate repeat of the `<ProductFormFeature>` composite may carry the percent post-consumer waste used in a product<br>• For specific versions of common e-publication file formats (eg the IDPF's EPUB 2.0.1), use `<ProductFormFeatureType>` code 15 and a value from List 220<br>• For e-publication formats not covered in List 220, use `<ProductFormFeatureType>` code 10 and a period-separated list of numbers (eg '7', '1.5' or '3.10.7') in `<ProductFormFeatureValue>`<br>• For required operating system for a digital product, see List 176. You should in addition include operating system version information (major and minor version numbers as necessary, eg '10.6.4 or later' for Mac OS 10.6.4, '7 SP1 or later' for Windows 7 Service Pack 1) in `<ProductFormFeatureDescription>`<br>• For other system requirements for a digital product (eg specific memory, storage or other hardware requirements), use free text in `<ProductFormFeatureDescription>` within a separate repeat of the `<ProductFormFeature>` composite<br>• For e-publication accessibility features for print-impaired readers, see List 196<br>• Further features with corresponding code lists may be added from time to time without a re-issue of this document – see the latest release of List 79 |
| Reference name | ProductFormFeatureValue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Short tag      | b335                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Cardinality    | 0…1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Example        | `<b335>BLK</b335>` (Black color)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

##### P.3.6 Product form feature description

If the `<ProductFormFeatureType>` requires free text rather than a code value, or if the code in `<ProductFormFeatureValue>` does not adequately describe the feature, a short text description may be added. Optional, and repeatable to provide parallel descriptive text in multiple languages. The language attribute is optional for a single instance of `<ProductFormFeatureDescription>`, but must be included in each instance if `<ProductFormFeatureDescription>` is repeated.

| Field          | Value                                                              |
|----------------|--------------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 10,000 characters   |
| Reference name | ProductFormFeatureDescription                                      |
| Short tag      | b336                                                               |
| Cardinality    | 0…n                                                                |
| Attributes     | language                                                           |
| Example        | `<b336>11pt Helvetica</b336>`                                      |

#### P.3.7 Product packaging type code

An ONIX code which indicates the type of outer packaging used for the product. Optional and non-repeating.

| Field          | Value                                                   |
|----------------|---------------------------------------------------------|
| Format         | Fixed length, two digits                                |
| Code list      | List 80                                                 |
| Reference name | ProductPackaging                                        |
| Short tag      | b225                                                    |
| Cardinality    | 0…1                                                     |
| Example        | `<ProductPackaging>05</ProductPackaging>` (Jewel case)  |

#### P.3.8 Product form description

If product form codes do not adequately describe the product, a short text description may be added to give a more detailed specification of the product form. The field is optional, and repeatable to provide parallel descriptions in multiple languages. The language attribute is optional for a single instance of `<ProductFormDescription>`, but must be included in each instance if `<ProductFormDescription>` is repeated to provide parallel descriptions in multiple languages.

| Field          | Value                                                                                                                                                                      |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 200 characters                                                                                                              |
| Reference name | ProductFormDescription                                                                                                                                                     |
| Short tag      | b014                                                                                                                                                                       |
| Cardinality    | 0…n                                                                                                                                                                        |
| Attributes     | language                                                                                                                                                                   |
| Example        | `<ProductFormDescription language="eng">Hardback book die-cut into car shape, with wheels attached to front and back covers</ProductFormDescription>`                        |

#### P.3.9 Trade category code

An ONIX code which indicates a trade category which is somewhat related to, but not properly an attribute of, product form. Optional and non-repeating.

| Field          | Value                                                    |
|----------------|----------------------------------------------------------|
| Format         | Fixed length, two digits                                 |
| Code list      | List 12                                                  |
| Reference name | TradeCategory                                            |
| Short tag      | b384                                                     |
| Cardinality    | 0…1                                                      |
| Example        | `<TradeCategory>03</TradeCategory>` (Sonderausgabe – Germany) |

#### P.3.10 Primary content type code

An ONIX code which indicates the primary or only content type included in a product. The element is intended to be used in particular for digital products, when the sender wishes to make it clear that one of a number of content types (eg text, audio, video) is the primary type for the product. Other content types may be specified in the `<ProductContentType>`. Optional and non-repeating.

| Field          | Value                                                |
|----------------|------------------------------------------------------|
| Format         | Fixed length, two digits                             |
| Code list      | List 81                                              |
| Reference name | PrimaryContentType                                   |
| Short tag      | x416                                                 |
| Cardinality    | 0…1                                                  |
| Example        | `<x416>10</x416>` (Eye-readable text)                |

#### P.3.11 Product content type code

An ONIX code which indicates a content type included in a product. The element is intended to be used in particular for digital products, to specify content types other than the primary type, or to list content types when none is singled out as the primary type. Optional, and repeatable to list multiple content types.

| Field          | Value                                                      |
|----------------|-------------------------------------------------------------|
| Format         | Fixed length, two digits                                   |
| Code list      | List 81                                                    |
| Reference name | ProductContentType                                         |
| Short tag      | b385                                                       |
| Cardinality    | 0…n                                                        |
| Example        | `<ProductContentType>11</ProductContentType>` (Musical notation) |

#### Measure composite

An optional group of data elements which together identify a measurement and the units in which it is expressed; used to specify the overall dimensions of a physical product including its packaging (if any). Repeatable to provide multiple combinations of dimension and unit.

| Field          | Value   |
|----------------|---------|
| Reference name | Measure |
| Short tag      | measure |
| Cardinality    | 0…n     |

##### P.3.12 Measure type code

An ONIX code indicating the dimension which is specified by an occurrence of the measure composite. Mandatory in each occurrence of the `<Measure>` composite, and non-repeating.

| Field          | Value                           |
|----------------|---------------------------------|
| Format         | Fixed length, two digits        |
| Code list      | List 48                         |
| Reference name | MeasureType                     |
| Short tag      | x315                            |
| Cardinality    | 1                               |
| Example        | `<x315>01</x315>` (Height)      |

##### P.3.13 Measurement

The number which represents the dimension specified in `<MeasureType>` in the measure units specified in `<MeasureUnitCode>`. Mandatory in each occurrence of the `<Measure>` composite, and non-repeating.

| Field          | Value                                                                                                 |
|----------------|-------------------------------------------------------------------------------------------------------|
| Format         | Positive real number, with explicit decimal point when required, suggested maximum length 6 characters |
| Reference name | Measurement                                                                                           |
| Short tag      | c094                                                                                                  |
| Cardinality    | 1                                                                                                     |
| Example        | `<c094>8.25</c094>`                                                                                   |

##### P.3.14 Measure unit code

An ONIX code indicating the measure unit in which dimensions are given. Mandatory in each occurrence of the `<Measure>` composite, and non-repeating. This element must follow the dimension to which the measure unit applies. See example below.

| Field          | Value                         |
|----------------|-------------------------------|
| Format         | Fixed length, two letters     |
| Code list      | List 50                       |
| Reference name | MeasureUnitCode               |
| Short tag      | c095                          |
| Cardinality    | 1                             |
| Example        | `<c095>mm</c095>`             |

#### P.3.15 Country of manufacture

An ONIX code identifying the country of manufacture of a single-item product, or of a multiple-item product when all items are manufactured in the same country. This information is needed in some countries to meet regulatory requirements. Optional and non-repeating.

| Field          | Value                                                                                                                               |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Format         | Fixed length, two letters, based on ISO 3166-1. Note that ISO 3166-1 specifies that country codes shall be sent as upper case only |
| Code list      | List 91                                                                                                                             |
| Reference name | CountryOfManufacture                                                                                                                |
| Short tag      | x316                                                                                                                                |
| Cardinality    | 0…1                                                                                                                                 |
| Example        | `<x316>US</x316>`                                                                                                                   |

#### P.3.16 Digital product technical protection

An ONIX code specifying whether a digital product has DRM or other technical protection features. Optional, and repeatable if a product has two or more kinds of protection (ie different parts of a product are protected in different ways).

| Field          | Value                                            |
|----------------|--------------------------------------------------|
| Format         | Fixed length, two digits                         |
| Code list      | List 144                                         |
| Reference name | EpubTechnicalProtection                          |
| Short tag      | x317                                             |
| Cardinality    | 0…n                                              |
| Example        | `<x317>03</x317>` (Has digital watermarking)     |
| Notes          | 'Epub' ('e-publication') here and in other element names below refers to any digital product, and has no necessary link with the .epub file format developed by the IDPF |

#### Usage constraint composite (digital products)

An optional group of data elements which together describe a usage constraint on a digital product (or the absence of such a constraint), whether enforced by DRM technical protection, inherent in the platform used, or specified by license agreement. Repeatable in order to describe multiple constraints on usage.

| Field          | Value               |
|----------------|---------------------|
| Reference name | EpubUsageConstraint |
| Short tag      | epubusageconstraint |
| Cardinality    | 0…n                 |

##### P.3.17 Usage type (digital products)

An ONIX code specifying a usage of a digital product. Mandatory in each occurrence of the `<EpubUsageConstraint>` composite, and non-repeating.

| Field          | Value                                     |
|----------------|-------------------------------------------|
| Format         | Fixed length, two digits                  |
| Code list      | List 145                                  |
| Reference name | EpubUsageType                             |
| Short tag      | x318                                      |
| Cardinality    | 1                                         |
| Example        | `<x318>05</x318>` (Text-to-speech)        |

##### P.3.18 Usage status (digital products)

An ONIX code specifying the status of a usage of a digital product, eg permitted without limit, permitted with limit, prohibited. Mandatory in each occurrence of the `<EpubUsageConstraint>` composite, and non-repeating.

| Field          | Value                             |
|----------------|-----------------------------------|
| Format         | Fixed length, two digits          |
| Code list      | List 146                          |
| Reference name | EpubUsageStatus                   |
| Short tag      | x319                              |
| Cardinality    | 1                                 |
| Example        | `<x319>03</x319>` (Prohibited)    |

##### Usage limit composite (digital products)

An optional group of data elements which together specify a quantitative limit on a particular type of usage of a digital product. Repeatable in order to specify two or more limits on the usage type.

| Field          | Value            |
|----------------|------------------|
| Reference name | EpubUsageLimit   |
| Short tag      | epubusagelimit   |
| Cardinality    | 0…n              |

###### P.3.19 Usage quantity (digital products)

A numeric value representing the maximum permitted quantity of a particular type of usage. Mandatory in each occurrence of the `<EpubUsageLimit>` composite, and non-repeating.

| Field          | Value                                                                                                                                  |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Format         | Positive real number, with explicit decimal point when required, or zero, as appropriate for the units specified in `<EpubUsageUnit>` |
| Reference name | Quantity                                                                                                                               |
| Short tag      | x320                                                                                                                                   |
| Cardinality    | 1                                                                                                                                      |
| Example        | `<Quantity>10</Quantity>`                                                                                                              |

###### P.3.20 Usage unit (digital products)

An ONIX code for a unit in which a permitted usage quantity is stated. Mandatory in each occurrence of the `<EpubUsageLimit>` composite, and non-repeating.

| Field          | Value                                                                 |
|----------------|-----------------------------------------------------------------------|
| Format         | Fixed length, two digits                                              |
| Code list      | List 147                                                              |
| Reference name | EpubUsageUnit                                                         |
| Short tag      | x321                                                                  |
| Cardinality    | 1                                                                     |
| Example        | `<EpubUsageUnit>07</EpubUsageUnit>` (Maximum number of concurrent users) |

#### Digital product license composite (new in 3.0.2)

An optional composite carrying the name or title of the license governing use of the product, a link to the license terms in eye-readable or machine-readable form, and optional dates when the license is valid. Repeatable in order to specify multiple licenses with differing periods of validity. Note that in the case of multiple Digital product license composites, any Usage constraints (above) apply to the current license.

| Field          | Value        |
|----------------|--------------|
| Reference name | EpubLicense  |
| Short tag      | epublicense  |
| Cardinality    | 0…n          |

##### P.3.20a Digital product license name (new in 3.0.2)

The name or title of the license. Mandatory in any `<EpubLicense>` composite, and repeatable to provide the license name in multiple languages. The language attribute is optional for a single instance of `<EpubLicenseName>`, but must be included in each instance if `<EpubLicenseName>` is repeated.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 100 characters  |
| Reference name | EpubLicenseName                                                |
| Short tag      | x511                                                           |
| Cardinality    | 1…n                                                            |
| Attributes     | language                                                       |
| Example        | `<x511>Elsevier e-book EULA v5</x511>`                         |

##### Digital product license expression composite (new in 3.0.2)

An optional composite that carries details of a link to an expression of the license terms, which may be in human-readable or machine-readable form. Repeatable when there is more than one expression of the license.

| Field          | Value                     |
|----------------|---------------------------|
| Reference name | EpubLicenseExpression     |
| Short tag      | epublicenseexpression     |
| Cardinality    | 0…n                       |

###### P.3.20b License expression type (new in 3.0.2)

An ONIX code identifying the nature or format of the license expression specified in the `<EpubLicenseExpressionLink>` element. Mandatory within the `<EpubLicenseExpression>` composite, and non-repeating.

| Field          | Value                                                        |
|----------------|--------------------------------------------------------------|
| Format         | Fixed length, two digits                                     |
| Code list      | List 218                                                     |
| Reference name | EpubLicenseExpressionType                                    |
| Short tag      | x508                                                         |
| Cardinality    | 1                                                            |
| Example        | `<x508>10</x508>` (ONIX-PL license expression)               |

###### P.3.20c License expression type name (new in 3.0.2)

A short free-text name for a license expression type, when the code in `<EpubLicenseExpressionType>` provides insufficient detail – for example when a machine-readable license is expressed using a particular proprietary encoding scheme. Optional and non-repeating, and must be included when (and only when) the `<EpubLicenseExpressionType>` element indicates the expression is encoded in a proprietary way.

| Field          | Value                                                         |
|----------------|---------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 50 characters  |
| Reference name | EpubLicenseExpressionTypeName                                 |
| Short tag      | x509                                                          |
| Cardinality    | 0…1                                                           |
| Attributes     | language                                                      |
| Example        | `<x509>ABC-XML</x509>`                                        |

###### P.3.20d License expression link (new in 3.0.2)

The URI for the license expression. Mandatory in each instance of the `<EpubLicenseExpression>` composite, and non-repeating.

| Field          | Value                                                          |
|----------------|----------------------------------------------------------------|
| Format         | Variable length text, suggested maximum length 300 characters |
| Reference name | EpubLicenseExpressionLink                                      |
| Short tag      | x510                                                           |
| Cardinality    | 1                                                              |

##### Digital product license date composite (new in 3.1)

An optional group of date elements which together specify a date associated with the license in an occurrence of the `<EpubLicense>` composite, eg a date when a license expires. Repeatable to specify different dates with their various roles. Note that if no dates are specified, the license is effective at the time the ONIX message is sent.

| Field          | Value              |
|----------------|--------------------|
| Reference name | EpubLicenseDate    |
| Short tag      | epublicensedate    |
| Cardinality    | 0…n                |

###### P.3.20e Digital product license date role code (new in 3.1)

An ONIX code indicating the significance of the date in relation to the license. Mandatory in each occurrence of the `<EpubLicenseDate>` composite, and non-repeating.

| Field          | Value                                                                     |
|----------------|---------------------------------------------------------------------------|
| Format         | Fixed length, two digits                                                  |
| Code list      | List 260                                                                  |
| Reference name | EpubLicenseDateRole                                                       |
| Short tag      | x585                                                                      |
| Cardinality    | 1                                                                         |
| Example        | `<EpubLicenseDateRole>14</EpubLicenseDateRole>` (license becomes effective) |

###### P.3.20f Date (new in 3.1)

The date specified in the `<EpubLicenseDateRole>` field. Mandatory in each occurrence of the `<EpubLicenseDate>` composite, and non-repeating. `<Date>` may carry a dateformat attribute: if the attribute is missing, then the default format is YYYYMMDD.

| Field          | Value                                                                                                                  |
|----------------|------------------------------------------------------------------------------------------------------------------------|
| Format         | As specified by the value in the dateformat attribute, or the default YYYYMMDD                                          |
| Reference name | Date                                                                                                                   |
| Short tag      | b306                                                                                                                   |
| Cardinality    | 1                                                                                                                      |
| Attributes     | dateformat                                                                                                             |
| Example        | `<Date>20221028</Date>`                                                                                                |
| Notes          | Note that all dates are inclusive, so 'Valid from' is the first date on which the license is effective, and 'Valid until' is the last date on which it is effective. |

#### P.3.21 Map scale

The scale of a map, expressed as a ratio 1:nnnnn; only the number nnnnn is carried in the data element, without spaces or punctuation. Optional, and repeatable if a product comprises maps with two or more different scales.

| Field          | Value                                                      |
|----------------|-------------------------------------------------------------|
| Format         | Positive integer, suggested maximum length 8 digits        |
| Reference name | MapScale                                                   |
| Short tag      | b063                                                       |
| Cardinality    | 0…n                                                        |
| Example        | `<b063>50000</b063>` (One to 50,000, 2cm = 1km)            |

#### Product classification composite

An optional group of data elements which together define a product classification (not to be confused with a subject classification). The intended use is to enable national or international trade classifications (also known as commodity codes) to be carried in an ONIX record. The composite is repeatable if parts of the product are classified differently within a single product classification scheme, or to provide classification codes from multiple classification schemes.

| Field          | Value                    |
|----------------|--------------------------|
| Reference name | ProductClassification    |
| Short tag      | productclassification    |
| Cardinality    | 0…n                      |

##### P.3.22 Product classification type code

An ONIX code identifying the scheme from which the identifier in `<ProductClassificationCode>` is taken. Mandatory in each occurrence of the `<ProductClassification>` composite, and non-repeating.

| Field          | Value                           |
|----------------|---------------------------------|
| Format         | Fixed length, two digits        |
| Code list      | List 9                          |
| Reference name | ProductClassificationType       |
| Short tag      | b274                            |
| Cardinality    | 1                               |
| Example        | `<b274>02</b274>` (UNSPSC)      |

##### P.3.22a Product classification type name (new in 3.0.7)

A name which identifies a proprietary classification scheme (ie a scheme which is not a standard and for which there is no individual scheme type code). Should be included when, and only when, the code in the `<ProductClassificationType>` element indicates a proprietary scheme, ie the sender's own category scheme. Optional and non-repeating.

| Field          | Value                               |
|----------------|-------------------------------------|
| Format         | Variable length text, suggested maximum length 50 characters |
| Reference name | ProductClassificationTypeName       |
| Short tag      | x555                                |
| Cardinality    | 0…1                                 |
| Attributes     | language                            |
| Example        | `<x555>PublishipGoodsCode</x555>`   |

##### P.3.23 Product classification code

A classification code from the scheme specified in `<ProductClassificationType>`. Mandatory in each occurrence of the `<ProductClassification>` composite, and non-repeating.

| Field          | Value                                                                            |
|----------------|----------------------------------------------------------------------------------|
| Format         | According to the identifier type specified in `<ProductClassificationType>`     |
| Reference name | ProductClassificationCode                                                        |
| Short tag      | b275                                                                             |
| Cardinality    | 1                                                                                |
| Example        | `<b275>55101514</b275>` (Sheet music in UNSPSC classification scheme)            |

##### P.3.24 Percentage

The percentage of the unit value of the product that is assignable to a designated product classification. Optional and non-repeating. Used when a mixed product (eg book and CD) belongs partly to two or more product classes within a particular classification scheme. If omitted, the product classification code applies to 100% of the product.

| Field          | Value                                                                                                                          |
|----------------|--------------------------------------------------------------------------------------------------------------------------------|
| Format         | Real number between zero and 100 (inclusive), with explicit decimal point when required, suggested maximum length 7 characters |
| Reference name | Percent                                                                                                                        |
| Short tag      | b337                                                                                                                           |
| Cardinality    | 0…1                                                                                                                            |
| Example        | `<Percent>66.67</Percent>`                                                                                                     |

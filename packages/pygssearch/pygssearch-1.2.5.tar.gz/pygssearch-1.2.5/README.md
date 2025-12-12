# PyGSSearch

This python module implements the OData protocol access following the 
Copernicus Space Component schema to allow the user to:
 - search products thanks to its filter helper.
 - download the filtered products.
 - report GeoJSON result of the filtered products.

This module implements a command line called `pygssearch` described here after.

# Installation
## Command-line Installation
The module comes with its command line, it can be simply installed via
standard pip command.
It is recommended to use python dedicated virtual environment to avoid any 
confusions between system or other projects libraries. 

Linux package python3-venv shall be installed (```sudo apt install python3-venv``` on ubuntu)

The command line to prepare the virtual environment:
```commandline
python3 -m venv venv
source venv/bin/activate
```

The pip command to install the module follow the syntax:
````commandline
pip install pygssearch
````

## Validation of the Installation
To ensure the module is well installed, it shall be possible to run
following commands:

```bash
pygssearch --help
```

```bash
pygssearch --version
```

# Command line Interface
`pygssearch` comes with many option detailed in these synopsys, accessible 
with `--help` command.

```synopsys
Usage: pygssearch [OPTIONS]

  This library PyGSSearch aims to support query and download product from the
  GSS catalogue, the download can be start with command line and also in
  python script. It authorize limiting the connections to respect the services
  quota policies.

Options:
  -s, --service TEXT           The OData CSC root Service URL to requests data
  -f, --filter TEXT            The OData filter to query Products in the
                               remote service.
  --footprint TEXT             Create a GeoJSON file at the provided path with
                               footprints and metadata of the returned
                               products. Set to ‘-’ for stdout. The GeoJSON
                               property fields can be configured with '--
                               attributes', '--format' and '--exclude'
                               parameters
  -u, --username TEXT          Service connection username.
  -p, --password TEXT          Service connection password.
  --token_url TEXT             Url to retrieve the token.
  --client_id TEXT             The client identifier.
  --client_secret TEXT         The client secret.
  --proxy TEXT                 Proxy URL or dict configuration.
  -t, --thread_number INTEGER  Number of parallel download threads
                               (default:2).
  -l, --limit INTEGER          Limit the number matching products (default:
                               10)
  --skip INTEGER               Skip a number matching products (default: 0)
  -o, --output TEXT            The directory to store the downloaded files.
  -S, --start TEXT             start date of the query in  the format YYYY-MM-
                               DD or an expression like NOW-1DAY.
  -E, --end TEXT               End date of the query
  -g, --geometry TEXT          Path to a GeoJson file containing a search area
                               ora series of entries of tuple of coordinates
                               separated by a coma
  --uuid TEXT                  Select a specific product UUID. Can be set more
                               than once.
  -n, --name TEXT              Select specific product(s) by filename. Can be
                               set more than once.
  -m, --mission [1|2|3|5]      Limit search to a Sentinel satellite
                               (constellation).
  -I, --instrument TEXT        Limit search to a specific instrument on a
                               Sentinel satellite (i.e. MSI, SAR, OLCI ...).
  -P, --product_type TEXT      Limit search to a Sentinel product type.
  --cloud INTEGER              Maximum cloud cover (in percent).
  -d, --download               Download all the results of the query.
  -O, --order_by TEXT          Specify the keyword to order the result.Prefix
                               ‘-’ for descending order, '+' for ascending.
                               Default ascending.
  -v, --verify                 Check the file integrity using his hash, use
                               with the download option.
  -C, --config TEXT            Give the path to a configuration file to the
                               .ini format
  -q, --quiet                  Silent mode: only errors are reported,use with
                               the download option.
  --version                    Show version number and exit.
  -F, --format TEXT            Define the response of the query by default
                               show the name and id, of each matching product
                               of the query. To show all information use '_'.
                               Current existing fixed properties in OData CSC
                               products are Id, Name, ContentType,
                               ContentLength, OriginDate, PublicationDate,
                               ModificationDate, Online, EvictionDate,
                               Checksum, ContentDate, Footprint, GeoFootprint.
  --attributes                 Includes the extended attributes of the product
                               into the GeoJSON properties.
  --exclude TEXT               The list of attributes to be excluded from the
                               output.
  --logs                       Print debug log message and no progress bar,use
                               with the download option.
  --debug                      Print debug log message.
  --show_url                   Print URL used to request OData service to
                               perform the given parameters. The service in
                               not contacted.
  --count                      returns the number of products returned by the
                               given parameters.
  --check_service              Controls if the Odata service is accessible.
  --help                       Show this message and exit.
```

## Service Connection
The OData service shall be up and running. To ensure service is available 
the following command can be used:

```commandline
$> pygssearch --service http://my.avail-service.com --check-service
OData service `http://my.avail-service.com` is accessible.
$> echo $?
0
```

```commandline
$> pygssearch --service http://my.not-avail-service.com --check-service
Cannot access OData service `http://my.not-avail-service.com`.
$> echo $?
2
```

The connection to the service is possible thanks to both possible kind of authentications protocols: Basic authentication with single login and password, OAuth2.0 authentication requiring an authentication service to retrieve or refresh authentication token:

### Basic authentication
The application command line can connect Basic Authentication service with parameters:
```commandline
pygssearch --service http://my.service.com --username username --password password
```
When not set, application looks into the environment variables `GSS_SERVICE`, `GSS_USERNAME`, `GSS_PASSWORD` to configure the missing set of information. 

Alternatively, it is possible to configure the credentials into a separate configuration file. The file format is [.ini](https://en.wikipedia.org/wiki/INI_file):
```ini
[pygssearch]
service=http://my.service.com
username=username
password=password
```
The configuration file can be loaded 
```commandline
$> pygssearch --config /path/to/config.ini
```
When config file is not provided, application automatically looks for the presence of `$HOME/.pygssearch.ini`. When it is present, its content is used to define information not present in the command line.

### OAuth2.0 authentication
```commandline
pygssearch --service http://my.service.com --username username --password password --token_url https://auth.com/token --client_id service --client_secret secret
```
As well as the basic authentication these parameters can be stored into a 
separate [.ini](https://en.wikipedia.org/wiki/INI_file) file:
```ini
[pygssearch]
service=http://my.service.com
username=username
password=password
token_url = https://auth.com/token
client_id = service
client_secret = secret
```

## No authentication
When service does not requires authentication, the simple following command 
can be used:
```commandline
pygssearch --service http://my.service.com
```

## Querying the CSC OData Service
### Products filtering
The application is able to return a list of product matching a large set of the following information:

| parameter        | description                                                                                                   | example                                                             |
|------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `--filter`       | [OData](https://www.odata.org/getting-started/basic-tutorial/#queryData) syntax filter                        | `ContentLength lt 10000000`                                         |
| `--start`        | The minimum sensing date of the queried products in  the format `YYYY-MM-DD` or an expression like `NOW-1DAY` | `2024-07-05`                                                        |
| `--end`          | The maximum sensing date of the queried products in  the format `YYYY-MM-DD` or an expression like `NOW-1DAY` | `2024-07-31`                                                        |
| `--geometry`     | A path to a GeoJSON shape file or a list of coordinates separated by a coma                                   | `'((1.0,1.0),(0.0,1.0),(0.0,0.0),(1.0,0.0),(1.0,1.0))'`             |
| `--uuid`         | Select a specific product UUID. Can be set more than once.                                                    | `285cdd67-713d-436a-ae92-df26e376f4d0`                              |
| `--name`         | Search products by their names.                                                                               | `S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE` |
| `--mission`      | Search products by their Sentinel mission number (1: Sentinel-1, 2: Sentinel-2...)                            | `2`                                                                 |
| `--instrument`   | Search products by their instrument name (SAR, MSI ..)                                                        | `MSI`                                                               |
| `--product_type` | Search product by their product type.                                                                         | `S2MSI2A`                                                           |
| `--cloud`        | Select product that have maximum cloud cover percentage.                                                      | `80`                                                                |

These parameters allows the selection of a set of product. The command line 
default displays the results:

```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0 \
    --uuid 2bd44957-44ef-45e5-af57-db7f35fde289

[{'Name': 'S2B_MSIL2A_20230920T005649_N0509_R088_T58WFB_20230920T011658.zip', 'Id': '2bd44957-44ef-45e5-af57-db7f35fde289'}, {'Name': 'S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip', 'Id': '285cdd67-713d-436a-ae92-df26e376f4d0'}]
```

### Output controls
The main objective of the command line is to download the filtered products.
A set of additional parameters as been included to optimize the service response:

#### Count results
A basic optimized count command is implemented in `--count` parameter:
```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0  \
    --uuid 2bd44957-44ef-45e5-af57-db7f35fde289  \
    --cloud 80 --product_type S2MSI2A            \     
    --count
2
```
The returned value is the number of products matching the configured query.
If paging parameter are set, they are ignored.
#### Paging management
When many products matches the configured filter, it is possible to navigated the results amond pages using `--skip` and `--limit` parameters. i.e.

```commandline
$> pygssearch --service https://my-service.com/odata/v1  --count
7334
$> 
$> pygssearch --service https://my-service.com/odata/v1 --skip 0 --limit 10
[{'Name': 'S3B_OL_1_ERR____20230913T222158_20230913T230611_20230915T025603_2653_084_058______MAR_O_NT_002.SEN3.zip', 'Id': '3e51abee-26cf-3c48-b24d-acf383fae29c'}, {'Name': 'S3A_OL_1_ERR____20230913T211956_20230913T220409_20230915T024223_2653_103_200______MAR_O_NT_002.SEN3.zip', 'Id': '6e9c32e4-be11-3d59-a767-cb75a47e8313'}, {'Name': 'S3B_OL_1_ERR____20230914T215554_20230914T224007_20230915T001718_2653_084_072______MAR_O_NR_002.SEN3.zip', 'Id': ' ...
$> pygssearch --service https://my-service.com/odata/v1 --skip 10 --limit 20
[{'Name': 'S2B_MSIL2A_20230920T005649_N0509_R088_T58WFB_20230920T011658.zip', 'Id': '2bd44957-44ef-45e5-af57-db7f35fde289'}, {'Name': 'S2B_MSIL2A_20230920T005649_N0509_R088_T58WFE_20230920T011658.zip', 'Id': 'e49efc8b-7d50-4553-ac98-e5d720dcb03d'}, {'Name': 'S2B_MSIL2A_20230920T005649_N0509_R088_T59WNU_20230920T011658.zip', 'Id': '08d5e6ec-3502-4a5d-b0e7-fea901cb27d9'}, {'Name': 'S2B_MSIL2A_20230920T005649_N0509_R088_T57WXT_20230920T011658.zip', 'Id': ...
```
#### Download
The application is able to manage download of filtered products. To activate the download process `--download` parameter is required.

The download behavior can be optimized with `--thread_number` to define the number of parallels downloads. This parameter could be set according the quota policy defines by the CSC remote service.

```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0  \
    --uuid 2bd44957-44ef-45e5-af57-db7f35fde289  \
    --cloud 80 --product_type S2MSI2A            \
    --thread_number 2                            \
    --download

S2B_MSIL2A_20230920T005649_N0509_R088_T58WFB_20230920T011658.zip:   7%|████▎                                                         | 25169920/360673883 [00:51<10:26, 535823.17Bytes/s]
S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip:   6%|███▌                                                     | 20975616/332981845 [00:49<10:54, 476359.34Bytes/s]
```
The `--quiet` parameter removes the progress information when required.

#### Origin JSON output
The call of the application without any parameter default returns a compatible JSON list configured with properties defined in '--format' parameter. Default configuration for format is (Name, Id) as followed:
```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 2bd44957-44ef-45e5-af57-db7f35fde289
[{'Name': 'S2B_MSIL2A_20230920T005649_N0509_R088_T58WFB_20230920T011658.zip', 'Id': '2bd44957-44ef-45e5-af57-db7f35fde289'}]
```

All the properies could be display using `--format  _`:
```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0  \
    --format _

[{'@odata.mediaContentType': 'application/octet-stream', 'Id': '285cdd67-713d-436a-ae92-df26e376f4d0', 'Name': 'S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip', 'ContentType': 'application/zip', 'ContentLength': 332981845, 'OriginDate': '2023-07-04T15:45:16.893Z', 'PublicationDate': '2023-12-14T02:08:58.964Z', 'ModificationDate': '2023-12-14T02:08:58.964Z', 'Online': True, 'EvictionDate': None, 'Checksum': [{'Algorithm': 'MD5', 'Value': '6e3aba9de3f17e5ab923ebda0a5e8067', 'ChecksumDate': '2023-12-14T02:08:59.385Z'}], 'ContentDate': {'Start': '2023-07-04T09:55:59.024Z', 'End': '2023-07-04T09:55:59.024Z'}, 'Footprint': "geography'SRID=4326;Polygon((8.654280647838144 33.34955671479698,9.104896746103945 33.35131707782119,9.106114026436753 34.34161747897296,8.921864856563118 34.34087902149685,8.885643289081308 34.20774629866525,8.8453106510589 34.06025011187324,8.8053907009052 33.912650453045245,8.76564162306296 33.76505833947785,8.72594925457459 33.61746169180876,8.686384096889565 33.46980822870747,8.654280647838144 33.34955671479698))'", 'GeoFootprint': {"coordinates": [[[8.654281, 33.349557], [9.104897, 33.351317], [9.106114, 34.341617], [8.921865, 34.340879], [8.885643, 34.207746], [8.845311, 34.06025], [8.805391, 33.91265], [8.765642, 33.765058], [8.725949, 33.617462], [8.686384, 33.469808], [8.654281, 33.349557]]], "type": "Polygon"}}]
```
Or the set of information can be explicitly defined:

```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0  \
    --format Name \
    --format Id \
    --format Checksum

[{'Name': 'S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip', 'Id': '285cdd67-713d-436a-ae92-df26e376f4d0', 'Checksum': [{'Algorithm': 'MD5', 'Value': '6e3aba9de3f17e5ab923ebda0a5e8067', 'ChecksumDate': '2023-12-14T02:08:59.385Z'}]}]
```
#### GeoJSON outputs
The JSON output has been improved with the "--footprint" parameter to generate GeoJSON output. The footprint parameter is the file destination for the GeoJSON. When '-' is provided, output is generate in the standard output:  
```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 2bd44957-44ef-45e5-af57-db7f35fde289 --footprint -

{"type":"FeatureCollection", "features": [{"properties": {"Name": "S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip", "Id": "285cdd67-713d-436a-ae92-df26e376f4d0"}, "type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[8.654281, 33.349557], [9.104897, 33.351317], [9.106114, 34.341617], [8.921865, 34.340879], [8.885643, 34.207746], [8.845311, 34.06025], [8.805391, 33.91265], [8.765642, 33.765058], [8.725949, 33.617462], [8.686384, 33.469808], [8.654281, 33.349557]]]}}]}
```
The properties are filled with the elements defined in the `--format` parameter and could be extended. The following example includes the `Checksum` into the properties:
```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0  \
    --format Name \
    --format Id \
    --format Checksum \
    --footprint -
 
 {"type":"FeatureCollection", "features": [{"properties": {"Name": "S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip", "Id": "285cdd67-713d-436a-ae92-df26e376f4d0", "Checksum": [{"Algorithm": "MD5", "Value": "6e3aba9de3f17e5ab923ebda0a5e8067", "ChecksumDate": "2023-12-14T02:08:59.385Z"}]}, "type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[8.654281, 33.349557], [9.104897, 33.351317], [9.106114, 34.341617], [8.921865, 34.340879], [8.885643, 34.207746], [8.845311, 34.06025], [8.805391, 33.91265], [8.765642, 33.765058], [8.725949, 33.617462], [8.686384, 33.469808], [8.654281, 33.349557]]]}}]}
```

In OData CSC product, the properties are freely accessible inside de `Products` entity. But a set of advanced attributes are also available via `Product/Attributes` Link. The `--attributes` flag allows the inclusion of these attributes into the GeoJSON properties:
```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0  \
    --footprint - \
    --format _    \
    --attributes
  
{"type":"FeatureCollection", "features": [{"properties": {"@odata.mediaContentType": "application/octet-stream", "Id": "285cdd67-713d-436a-ae92-df26e376f4d0", "Name": "S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip", "ContentType": "application/zip", "ContentLength": 332981845, "OriginDate": "2023-07-04T15:45:16.893Z", "PublicationDate": "2023-12-14T02:08:58.964Z", "ModificationDate": "2023-12-14T02:08:58.964Z", "Online": true, "EvictionDate": null, "Checksum": [{"Algorithm": "MD5", "Value": "6e3aba9de3f17e5ab923ebda0a5e8067", "ChecksumDate": "2023-12-14T02:08:59.385Z"}], "ContentDate": {"Start": "2023-07-04T09:55:59.024Z", "End": "2023-07-04T09:55:59.024Z"}, "lineage": "Not evaluated", "instrumentShortName": "MSI", "tileId": "T32SMC", "degradedAncillaryDataPercentage": 0.0, "productGroupId": "GS2B_20230704T095559_033038_N05.09", "processingLevel": "Level-2A", "resourceLanguage": "eng", "temporalExtentBeginPosition": "2023-07-04T09:55:59.024Z", "geometricQualityFlag": "PASSED", "beginningDateTime": "2023-07-04T09:55:59.024Z", "sensorType": "OPTICAL", "platformShortName": "SENTINEL-2", "metadataLanguage": "eng", "geographicBoundingBoxWestBoundLongitude": 8.654280647838144, "saturatedDefectivePixelPercentage": 0.0, "cloudShadowPercentage": 0.0, "radiativeTransferAccuracy": 0.0, "snowIcePercentage": 0.0, "noDataPixelPercentage": 73.59255, "waterPercentage": 0.070019, "cloudCover": 0.746881, "highProbaCloudsPercentage": 0.181249, "degree": "Not evaluated", "resourceTitle": "Sentinel-2 End-User Product Level-2A (short name: EUP L2A)", "processorVersion": "05.09", "topicCategory": "imageryBaseMapsEarthCover", "endingDateTime": "2023-07-04T09:55:59.024Z", "operationalMode": "INS-NOBS", "darkFeaturesPercentage": 0.0, "specificationDateType": "revision", "uniqueResourceIdentifierCode": "s2:eup:l2a:{PRODUCTUUID}", "keywordValue": "opticalEarthObservation\nSatellite\nSentinel-2\nS2\nMSI\nEUP\nL2A", "temporalExtentEndPosition": "2023-07-04T09:55:59.024Z", "radiometricQualityFlag": "PASSED", "thinCirrusPercentage": 0.0, "geographicBoundingBoxNorthBoundLatitude": 34.34161747897296, "sensorQualityFlag": "PASSED", "processingDate": "2023-07-04T12:54:25.000Z", "aotRetrievalAccuracy": 0.0, "orbitNumber": 33038, "waterVapourRetrievalAccuracy": 0.0, "degradedMSIDataPercentage": 0.0, "specificationTitle": "INSPIRE Metadata Implementing Rules: Technical Guidelines based on EN ISO 19115 and EN ISO 19119 V 1.3", "generalQualityFlag": "PASSED", "resourceAbstract": "The End-User Level-2A product provides Bottom Of Atmosphere (BOA) reflectance images derived from the associated Level-1C products. Each Level-2A product is composed of 100x100 km2 tiles in cartographic geometry (UTM/WGS84 projection).\n\n                     Level-2A products are systematically generated at the ground segment over Europe since March 2018, and the production was extended to global in December 2018. Level-2A generation can also be performed by the user through the Sentinel-2 Toolbox using as input the associated Level-1C product.", "productType": "S2MSI2A", "formatCorrectnessFlag": "PASSED", "vegetationPercentage": 0.431926, "relativeOrbitNumber": 122, "coordinates": "<gml:Polygon srsName=\"http://www.opengis.net/gml/srs/epsg.xml#4326\" xmlns:gml=\"http://www.opengis.net/gml\">\n   <gml:outerBoundaryIs>\n      <gml:LinearRing>\n         <gml:coordinates>33.34955671479698,8.654280647838144 33.46980822870747,8.686384096889565 33.61746169180876,8.72594925457459 33.76505833947785,8.76564162306296 33.912650453045245,8.8053907009052 34.06025011187324,8.8453106510589 34.20774629866525,8.885643289081308 34.34087902149685,8.921864856563118 34.34161747897296,9.106114026436753 33.35131707782119,9.104896746103945 33.34955671479698,8.654280647838144 </gml:coordinates>\n      </gml:LinearRing>\n   </gml:outerBoundaryIs>\n</gml:Polygon>", "geographicBoundingBoxSouthBoundLatitude": 33.34955671479698, "resourceTitleDatasetSeries": "Sentinel-2 EUP Level-2A", "notVegetatedPercentage": 98.709685, "dateOfCreation": "2023-07-04T12:54:25.000Z", "platformSerialIdentifier": "B", "mediumProbaCloudsPercentage": 0.565632, "unclassifiedPercentage": 0.041486, "geographicBoundingBoxEastBoundLongitude": 9.106114026436753, "specificationDate": "2013-10-29", "orbitDirection": "DESCENDING", "resourceType": "dataset"}, "type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[8.654281, 33.349557], [9.104897, 33.351317], [9.106114, 34.341617], [8.921865, 34.340879], [8.885643, 34.207746], [8.845311, 34.06025], [8.805391, 33.91265], [8.765642, 33.765058], [8.725949, 33.617462], [8.686384, 33.469808], [8.654281, 33.349557]]]}}]}
```
The usage of `--format xx` is still possible among both product properties and its attributes. In this case only identified items will be displayed.

```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0  \
    --footprint -  \
    --format  Name \
    --format  Id \
    --format  cloudCover \
    --format  noDataPixelPercentage \
    --attributes
{"type":"FeatureCollection", "features": [{"properties": {"Name": "S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip", "Id": "285cdd67-713d-436a-ae92-df26e376f4d0", "noDataPixelPercentage": 73.59255, "cloudCover": 0.746881}, "type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[8.654281, 33.349557], [9.104897, 33.351317], [9.106114, 34.341617], [8.921865, 34.340879], [8.885643, 34.207746], [8.845311, 34.06025], [8.805391, 33.91265], [8.765642, 33.765058], [8.725949, 33.617462], [8.686384, 33.469808], [8.654281, 33.349557]]]}}]}
```

The exclude parameter allows to remove items from the list:

```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    -uuid 285cdd67-713d-436a-ae92-df26e376f4d0  \
    --format _                           \
    --attributes                         \
    --footprint -                        \
    --exclude keywordValue               \
    --exclude coordinates                \
    --exclude specificationTitle         \
    --exclude resourceAbstract           \
    --exclude resourceTitleDatasetSeries \
    --exclude EvictionDate
{"type":"FeatureCollection", "features": [{"properties": {"@odata.mediaContentType": "application/octet-stream", "Id": "285cdd67-713d-436a-ae92-df26e376f4d0", "Name": "S2B_MSIL2A_20230704T095559_N0509_R122_T32SMC_20230704T125425.SAFE.zip", "ContentType": "application/zip", "ContentLength": 332981845, "OriginDate": "2023-07-04T15:45:16.893Z", "PublicationDate": "2023-12-14T02:08:58.964Z", "ModificationDate": "2023-12-14T02:08:58.964Z", "Online": true, "Checksum": [{"Algorithm": "MD5", "Value": "6e3aba9de3f17e5ab923ebda0a5e8067", "ChecksumDate": "2023-12-14T02:08:59.385Z"}], "ContentDate": {"Start": "2023-07-04T09:55:59.024Z", "End": "2023-07-04T09:55:59.024Z"}, "lineage": "Not evaluated", "instrumentShortName": "MSI", "tileId": "T32SMC", "degradedAncillaryDataPercentage": 0.0, "productGroupId": "GS2B_20230704T095559_033038_N05.09", "processingLevel": "Level-2A", "resourceLanguage": "eng", "temporalExtentBeginPosition": "2023-07-04T09:55:59.024Z", "geometricQualityFlag": "PASSED", "beginningDateTime": "2023-07-04T09:55:59.024Z", "sensorType": "OPTICAL", "platformShortName": "SENTINEL-2", "metadataLanguage": "eng", "geographicBoundingBoxWestBoundLongitude": 8.654280647838144, "saturatedDefectivePixelPercentage": 0.0, "cloudShadowPercentage": 0.0, "radiativeTransferAccuracy": 0.0, "snowIcePercentage": 0.0, "noDataPixelPercentage": 73.59255, "waterPercentage": 0.070019, "cloudCover": 0.746881, "highProbaCloudsPercentage": 0.181249, "degree": "Not evaluated", "resourceTitle": "Sentinel-2 End-User Product Level-2A (short name: EUP L2A)", "processorVersion": "05.09", "topicCategory": "imageryBaseMapsEarthCover", "endingDateTime": "2023-07-04T09:55:59.024Z", "operationalMode": "INS-NOBS", "darkFeaturesPercentage": 0.0, "specificationDateType": "revision", "uniqueResourceIdentifierCode": "s2:eup:l2a:{PRODUCTUUID}", "temporalExtentEndPosition": "2023-07-04T09:55:59.024Z", "radiometricQualityFlag": "PASSED", "thinCirrusPercentage": 0.0, "geographicBoundingBoxNorthBoundLatitude": 34.34161747897296, "sensorQualityFlag": "PASSED", "processingDate": "2023-07-04T12:54:25.000Z", "aotRetrievalAccuracy": 0.0, "orbitNumber": 33038, "waterVapourRetrievalAccuracy": 0.0, "degradedMSIDataPercentage": 0.0, "generalQualityFlag": "PASSED", "productType": "S2MSI2A", "formatCorrectnessFlag": "PASSED", "vegetationPercentage": 0.431926, "relativeOrbitNumber": 122, "geographicBoundingBoxSouthBoundLatitude": 33.34955671479698, "notVegetatedPercentage": 98.709685, "dateOfCreation": "2023-07-04T12:54:25.000Z", "platformSerialIdentifier": "B", "mediumProbaCloudsPercentage": 0.565632, "unclassifiedPercentage": 0.041486, "geographicBoundingBoxEastBoundLongitude": 9.106114026436753, "specificationDate": "2013-10-29", "orbitDirection": "DESCENDING", "resourceType": "dataset"}, "type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[8.654281, 33.349557], [9.104897, 33.351317], [9.106114, 34.341617], [8.921865, 34.340879], [8.885643, 34.207746], [8.845311, 34.06025], [8.805391, 33.91265], [8.765642, 33.765058], [8.725949, 33.617462], [8.686384, 33.469808], [8.654281, 33.349557]]]}}]}
```

The GeoJSON output contains a FeatureCollection the gather the list or results. The generated output follows the standard and can be use in others tools:

![img.png](img.png)


#### Debugging features
When many filter parameter are used in the pygssearch interface, the query to request remote OData service may become extremely complex. The `--show_url` parameter has been introduced to display the final Odata url.

```commandline
$> pygssearch --service https://my-service.com/odata/v1  \
    --uuid 285cdd67-713d-436a-ae92-df26e376f4d0 \
    --uuid 2bd44957-44ef-45e5-af57-db7f35fde289 \
    --cloud 80 \
    --product_type S2MSI2A \
    --show_url
https://my-service.com/odata/v1/Products?$filter=StringAttributes/any(d:d/Name eq 'productType' and d/Value eq 'S2MSI2A') and Attributes/OData.CSC.DoubleAttribute/any(d:d/Name eq 'cloudCover' and d/OData.CSC.DoubleAttribute/Value lt 80) and (Id eq 285cdd67-713d-436a-ae92-df26e376f4d0 or Id eq 2bd44957-44ef-45e5-af57-db7f35fde289)&$top=10&$skip=0&$format=json

```


# Developer Corner
## Build environment
The sources comes with a `Makefile` able to run locally to set up and prepare python environment to run tests and coverage.It also provides target to deploy new release manually.
Otherwise, sources contains gitlab pipeline configurations that ensure the code quality at each developer git commit commands. It also automatically deploy source when new tag is push into git service, when service is properly configured.

```commandline
make clean
```
Clean-up the environment from cache and lightweight components. It does not removed downloaded dependencies (from venv directory), nor distributions.

```commandline
make dist-clean
```
The `dist-clean` command full cleans the repository as it has been cloned first.
Following the call of `dist-clean` the virtual environment and all the caches will be removed.

```commandline
make test
```
Run the unitary tests.

```commandline
make lint
```
Check if the source code properly follows the pep8 directives. This test is also used in gitlab piplines to accept pushed sources.

```commandline
make coverage
```
Run the test coverage and generates a html report into `htmlcov` directory.

```commandline
make dist
```
Prepare a distribution locally into `dist` directory. When no tag is present on the current commit, or modified files are present into the local directory, the distribution process creates a dirty version to be safety deploy to the repository.

```commandline
make dist-deploy
```
Prepare and deploy a distribution into the gael's remote Pypi.org repository.
This command is run automatically when pushing a new tag. 

# Frequently Ask Questions
## How to use a proxy for a connection ?
pyGssSearch command supports the connections to a proxy in 3 differents ways:
### Use variable environment
It is possible to define the proxy information setting environment 
variables `HTTP_PROXY`, `HTTPS_PROXY`, `HTTPS_PROXY`, before running python 
script. Each variable is dedicated to the protocol of the target request.

Following codes shows examples to defines these variables.
```bash
# Linux bash script
export HTTP_PROXY=http://user:pass@151.91.23.207:3128
export HTTPS_PROXY=http://user:pass@51.91.23.207:3128
export FTP_PROXY=http://user:pass@51.91.23.207:3128
```
Optionally, the proxy credentials can be inserted as part of the URL has 
shown is the previous samples.

### Use ```--proxy <proxy_parameter>``` pyGssSearch parameter
When --proxy parameter is provided as a single string, the given address is 
considered as the multi-protocol url:

```bash 
pygsssearch --proxy 'user:pass@151.91.23.207:3128' ...
```

Is equivalent to the environment variables setting defined here before.

### Details the proxy protocols url
When url to proxy differs wrt their protocol, it is possible to give 
detailed configuration to the script according to a dict form as followed:

```bash 
pygsssearch --proxy "{'http': 'http://51.91.23.207:3128', 'https': 'https://51.91.23.208:3128', 'ftp': 'http://51.91.23.209:3128'}" ...
```

This string will be properly interpreted and use as proxy for each of these various protocols.

### Proxy Errors
The proxy could be the origin of the connections failures. it does not happen
at the proxy configuration time, but during the first request to the target.  

When the proxy is not available and cannot respond the requests, 
a `ConnectionTimeout` exception is raised.  
When the proxy fails with because of bad request, the `ProxyError` exception 
is raised.  
If the proxy parameter dict or URL is malformed, a `InvalidURL` exception is 
raised.

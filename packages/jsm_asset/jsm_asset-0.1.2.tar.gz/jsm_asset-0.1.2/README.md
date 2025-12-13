# jsm_asset

A Python library for managing and processing Jira Service Management (JSM) Asset objects

## Features

- Browse and query JSM via Assets Query Language (AQL) and get results as python objects
- Read and update attributes of JSM Objects

## Installation

```bash
pip install jsm_asset
```

## Usage

```python
import jsm_asset

# Create a session with the JSM Asset API
auth = BasicAuth('jira_user_email@domain.com',"my_api_key")
jsm_asset = AssetSession('jira_user_email@domain.com',"my_api_key","https://<jira_site_id>.atlassian.net")

# Query for objects using AQL
query = 'objectType = Service'
qr = jsm_asset.aql_query(query)

# AQLQuery.results is a generator! Make a quick list with list(qr.results) if you need it
my_assets = list(qr.result)

# Or just print the results
for r in qr.results:
    print(r)

# List all Asset schemas in the JSM session
jsm_asset.schemas
# Access a specific schema by ID
jsm_asset.schemas['1']
# Get all objects in a schema (Don't really recommend this for large schema)
# Convenience property creates an AQLQuery for you
schema_query = jsm_asset.schemas['1'].objects
all_schema_objects = list(schema_query.results)

# Working with an individual asset record
my_asset = all_schema_objects[4]
my_asset.type
-> Software Services
my_asset.name
-> VMware
my_asset.id
-> '2623267'
my_asset.attributes
-> {'1': <AssetDefaultAttribute[Text]> Key -> SVC-1556412,
 '2': <AssetDefaultAttribute[Text]> Name -> VMware,
 '3': <AssetDefaultAttribute[DateTime]> Created -> 13/Mar/23 9:38 PM,
 '4': <AssetDefaultAttribute[DateTime]> Updated -> 05/Nov/24 11:07 PM,
 '5': <AssetDefaultAttribute[Textarea]> Description -> https://brown.atlassian.net/jira/servicedesk/assets/object/509893
 accessing server environments for Windows and Linux servers,
 '6': <AssetDefaultAttribute[Select]> Tier -> Tier 1,
 '8': <AssetDefaultAttribute[Text]> Service ID -> ari:cloud:graph::service/050251f9-8e95-40fb-b1d7-b0a972e0a243/58ec78ea-c1e7-11ed-90dd-128b42819424,
 '9': <AssetDefaultAttribute[Text]> Revision -> 1652,
 '2548': <AssetAttribute[]> Project -> ,
 '2549': <AssetAttribute[]> Bitbucket Repo -> ,
 '2550': <AssetAttribute[]> Stakeholders -> ,
 '2551': <AssetAttribute[]> Responders -> ,
 '2556': <AssetAttribute[]> Service Owners -> fbc38639-b0c4-4c4e-bc25-2557cbe9cffb,
 '2557': <AssetAttribute[]> Responder Teams -> ,
 '3377': <AssetObjectAttribute[Object]> Service relationships for Applications -> ,
 '3378': <AssetObjectAttribute[Object]> Service relationships for Business services -> ,
 '3379': <AssetObjectAttribute[Object]> Service relationships for Capabilities -> ,
 '3380': <AssetObjectAttribute[Object]> Service relationships for Software services -> }
```

## Documentation

See the [docs](docs/) directory for detailed API documentation and examples.

## Contributing

Contributions are welcome! Please open issues or submit pull requests on GitHub.

## License

This project is licensed under the MIT License.
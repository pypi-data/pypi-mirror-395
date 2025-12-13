# Zenodo API Client

## Introduction

The Zenodo API Client is a simplistic wrapper around the [Zenodo REST API](https://developers.zenodo.org/).

It supports creation, file upload, metadata annotation, deletion and publication of depositions.

## Limitations

Currently it is limited to depostions of type `Dataset`.

## Installation

```bash
pip install zenodo-api-client
```

## Example

```python
from zenodo_client import *

client = ZenodoClient(
    host='sandbox.zenodo.org',  # for real: zenodo.org
    access_token=access_token  # personal access token from Zenodo
)

# create a deposition on zenodo
depo = client.new_deposition()

# add metadata
metadata = MetaData(
    title='some title', 
    description='some description',
    notes='some notes',
    creators=[Creator(name='some creator', affiliation='some affiliation')],
    license='CC-BY-4.0'  # one of the identifiers from https://spdx.org/licenses/
)
client.set_metadata(deposition_id=depo['id'], metadata=metadata)

# upload a file
client.file_upload(deposition_id=depo['id'], path=Path('some/file'))

# publish the deposition
client.publish(deposition_id=depo['id'])
```

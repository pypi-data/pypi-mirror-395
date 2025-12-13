# ReqDB PyClient

The ReqDB PyClient is the official client for the [ReqDB](https://github.com/dcfSec/ReqDB) API.
The PyClient contains the needed functions to interact with the API

## Installation

Use pip to install the client:

```bash
pip install reqdb
```

## Usage

First you need to get a valid OAuth access token for the ReqDB server (e.g. with [msal](https://learn.microsoft.com/en-us/entra/msal/python/)).
After you acquired your token you can connect to the API:

```python
client = ReqDB("<ReqDB FQDN>", "<Access Token>")
```

With the initialized client you can now perform actions (according to your roles) for each model ( `Tags`, `Topics`, `Requirements`, `ExtraTypes`, `ExtraEntries`, `Catalogues`, `Comment`): `get`, `all`, `update`, `delete`, `add`

Example for a tags:

```python
# Get tag with id: 1
tag1 = client.Tags.add(id=1)

# Get all tags
allTags = client.Tags.all()

# Update a tag:
tag = client.Tags.update(id=1, models.Tag(name="Tag 1"))

# Delete a tag:
ok = client.Tags.delete(id=1)

# Add a tag
tag = client.Tags.add(models.Tag(name="Tag 2"))
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/dcfSec/ReqDB/tags). 

## Authors

 * [dcfSec](https://github.com/dcfSec) - *Initial work*

See also the list of [contributors](https://github.com/dcfSec/ReqDB-PyClient/contributors) who participated in this project.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details
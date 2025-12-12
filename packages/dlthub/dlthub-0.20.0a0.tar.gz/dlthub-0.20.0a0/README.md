<h1 align="center">
    <strong>dlthub</strong>
</h1>

<div align="center">
  <a target="_blank" href="https://dlthub.com/community" style="background:none">
    <img src="https://img.shields.io/badge/slack-join-dlt.svg?labelColor=191937&color=6F6FF7&logo=slack" style="width: 260px;"  />
  </a>
</div>
<div align="center">
  <a target="_blank" href="https://pypi.org/project/dlthub/" style="background:none">
    <img src="https://img.shields.io/pypi/v/dlthub?labelColor=191937&color=6F6FF7">
  </a>
  <a target="_blank" href="https://pypi.org/project/dlthub/" style="background:none">
    <img src="https://img.shields.io/pypi/pyversions/dlthub?labelColor=191937&color=6F6FF7">
  </a>
</div>

dlthub is the a commercial extension to the open source data load tool ([dlt]((https://dlthub.com/docs/))). Features include:
* define data transformations in Python and SQL
* generate dbt packages from dlt pipelines
* dlthub projects: empower any team members to define sources, destinations and pipelines in a declarative yaml interface
* Iceberg support


## Installation

`dlthub` supports Python 3.10 and above and is a plugin (based on [pluggy](https://github.com/pytest-dev/pluggy)) Use `hub` extra on `dlt` to pick the matching plugin version:

```sh
pip install "dlt[hub]"
```


## Documentation

Learn more in the [dlthub docs](https://dlthub.com/docs/hub/intro).

## License

dlthub requires a license to be used, please join our [waiting list](https://info.dlthub.com/waiting-list) to get one.
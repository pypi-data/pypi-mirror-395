<h1 align="center">
    <strong>dlthub</strong>
</h1>

<div align="center">
  <a target="_blank" href="https://dlthub.com/community" style="background:none">
    <img src="https://img.shields.io/badge/slack-join-dlt.svg?labelColor=191937&color=6F6FF7&logo=slack" style="width: 260px;"  />
  </a>
</div>
<div align="center">
  <a target="_blank" href="https://pypi.org/project/dlt-runtime/" style="background:none">
    <img src="https://img.shields.io/pypi/v/dlt-runtime?labelColor=191937&color=6F6FF7">
  </a>
  <a target="_blank" href="https://pypi.org/project/dlt-runtime/" style="background:none">
    <img src="https://img.shields.io/pypi/pyversions/dlt-runtime?labelColor=191937&color=6F6FF7">
  </a>
</div>

`dlt-runtime` is an extension to the open source data load tool ([dlt]((https://dlthub.com/docs/))) that implements
**dltHub Runtime** API Client and extends the `dlt` command line with `dlt runtime` command. Overall it enables `dlt` users
to quickly deploy and run their pipelines, datasets, notebooks and mcp servers.


## Installation

`dlt-runtime` supports Python 3.10 and above and is a plugin (based on [pluggy](https://github.com/pytest-dev/pluggy)) Use `hub` extra on `dlt` to pick the matching plugin version:

```sh
pip install "dlt[hub]"
```


## Documentation

Learn more in the [dlthub docs](https://dlthub.com/docs/hub/intro).
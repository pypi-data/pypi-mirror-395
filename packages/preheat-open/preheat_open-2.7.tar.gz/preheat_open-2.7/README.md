# PreHEAT Open Python Package

This is the open Python package designed to wrap [Neogrid's REST API](https://neogrid-technologies.gitlab.io/neogrid-api/).

For a quick introduction on how to use the package, see the [quick start guide](https://gitlab.com/neogrid-technologies-public/preheat-open-python/-/blob/master/docs/source/tutorials/quick_start.ipynb).

## Installation and configuration

### Simple installation:
Install the package directly from [PyPi](https://pypi.org/project/preheat-open/) using:

    pip install preheat_open

### Configuring the toolbox
First, make sure that you have created an API key for your user. This can be done on your [user profile page in the PreHEAT App](https://app.neogrid.dk/v2/#!/app/user/profile).

Your API key may be set within the code code itself. We do however recommend to use a YAML configuration file. This user configuration file should be located in the following directories:

| OS      | User level (recommended)                  | Machine level                  |  
|---------|-------------------------------------------|--------------------------------|
| Windows | C:/Users/[your user]/.preheat/config.yaml | (unsupported)                  |
| Linux   | ~/.preheat/config.yaml                    | /etc[/opt]/preheat/config.yaml |


The default content of a YAML configuration file is given here. The API key can be pasted under neogrid_api -> token.

```
cache:
  directory: null
  size_limit: null
  time_to_live: null
  type: null
logging:
  format: '%(asctime)-23s  %(levelname)-8s  %(name)-32s  %(message)-80s'
  level: 20
neogrid_api:
  token: ''
  url: https://api.neogrid.dk/public/api/v1
personal:
  email: ''
  name: ''
  runtime_mode: 10
  timezone: Europe/Copenhagen
```

For information about the additional fields, please check the [quick start guide](https://gitlab.com/neogrid-technologies-public/preheat-open-python/-/blob/master/docs/source/tutorials/quick_start.ipynb).

## Additional Information
You can find additional information about the [PreHeat REST API here](https://neogrid-technologies.gitlab.io/neogrid-api/).
[Neogrid Technologies company homepage](https://neogrid.dk/)

## Contributions

We encourage pull requests if you have developed new interesting features.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

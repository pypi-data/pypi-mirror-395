This site contains the project documentation for the
`datafarm-pyclient` library that is a functioning python client
for interacting with DIMS.FARM

## Requirements

* Windows or Linux operating system
* Python 3.8 - 3.12

## Installation

```
$ pip install datafarmclient
```

## Getting started
To get started you need a valid Datafarm api_url and an api_key

```python
>>>  from datafarmclient import DatafarmClient
>>>  client = DatafarmClient(api_url=api_url)
>>>  client.login(api_key=api_key)
```
See more in [Getting started](getting_started.md), look through the [Tutorials](tutorials.md) or read in detail in the [API reference](reference.md).

# Quick Start

### Installing 

QuickZip can be installed with pip. As to not pollute your system python, it is recommended to install this in a virtual environment or with a tool like pipx 

<div class="termy">

```console
$ pip install quick-zip

---> 100%
```

</div>

### Setup

Before you get started there are a few things you might want to do

#### Optional
**Specify a default config.toml file.** This is specified with the full-path to the config.toml file on our file system using the `QUICKZIP_CONFIG` env variable. Note that if this is not set, you must pass the path to the config.toml file when call `quick-zip run`. See the Config File page for a template and more details on the configuration template.


### Running

<div class="termy">

```console

--8<-- "docs_src/help.sh"

```

</div>

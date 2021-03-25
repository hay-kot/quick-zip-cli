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


## Commands

* `quickzip run` - Run all the jobs in the default configuration file



<div class="termy">

```console
$ qz run
───────────── QuickZip: 'Dev Backup 3' ─────────────
Creating: Dev Backup 3_2021.03.19_23.36.37

            Audit Report `Dev Backup 3`
╭────── Dev Backup 3_2021.03.19_23.35.44.zip ──────╮
│ 100.03 MB                                        │
│ Parent: Dev Backup 3                             │
│ Days Old 0                                       │
╰──────────────────────────────────────────────────╯

               🗑  Cleanup 'data/dest'
╭─ Dev Backup 3_2021.03.19.zip ─╮
│ Deleted                       │
│ Parent: Dev Backup 3          │
│ From Source                   │
╰───────────────────────────────╯

```

</div>
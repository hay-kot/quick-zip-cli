
# Configuration File

The QuickZip configuration file is a .json file that is used to set the app configuration, job defaults, and job store. 

### `config`

The main configuration for QuickZip. 

`enable_webhooks`
:   Default: `False` · When enabled, a webhook is posted to the `webhook_address` containing information about the backups that were ran

`webhook_address`
:   Default: `''` · A single web address/url where the backup reports will be posted

```json
"config": {
    "enable_webhooks": false,
    "webhook_address": "https://webhooks.com/webhook",
},
```

### `default`

The default values for jobs when values are not specified. 

`name`
:   Default: `'None'` · The name of the backup, this will be used to generate the destination file name

`source`
:   Default: `'None'` · The source directory or file to be zipped

`destination`
:   Default: `None'` · The destination directory where the zip files will be moved to. Must be a directory

`clean_up`
:   Default: `'false | User Set'` · When enabled, QuickZip will clean up the destination directory and only keep the newest `keep` number of files

`clean_up_source`
:   Default: `'false | User Set'` · When enabled, QuickZip will clean up the source directory and only keep the newest `keep` number of files

`keep`
:   Default: `'4 | User Set'` · The number of files to keep when using `clean_up` and `clean_up_source`.

```json
"defaults": {
    "name": "",
    "source": "",
    "destination": "./nas/backups",
    "clean_up": false,
    "clean_up_source": false,
    "keep": 4
},
```

### `jobs`
The Jobs key is a list of jobs that are defined the same as the "defaults" refer to the defaults for key/value descriptions. A Full example is listed below to reference for formatting.


### Full Example
```json
{
    "config": {
        "enable_webhooks": false,
        "webhook_address": "https://webhooks.com/webhook",
    },
    "defaults": {
        "name": "ENTRY",
        "source": "",
        "destination": "./nas/backups",
        "clean_up": false,
        "clean_up_source": false,
        "keep": 4
    },
    "jobs": [
        {
            "name": "Home Assistant",
            "source": "/Users/hayden/desktop/Home Assistant/src",
            "destination": "/Users/hayden/desktop/Home Assistant/dest",
            "clean_up": true,
            "clean_up_source": true
        }
    ]
}
```

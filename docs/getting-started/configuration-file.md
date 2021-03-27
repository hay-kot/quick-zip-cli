
# Configuration File

The QuickZip configuration file is a .toml file that is used to set the app configuration, job defaults, and job store. 

## `config`

The main configuration for QuickZip. 

`enable_webhooks`
:   Default: `False` · When enabled, a webhook is posted to the `webhook_address` containing information about the backups that were ran

`webhook_address`
:   Default: `''` · A single web address/url where the backup reports will be posted

`verbose`
:   Default `False`. Set the terminal output to verbose. Can also be done with --verbose

`zip_types`
:   Default `[ ".tar.gz", ".bz2", ".zip" ]`. Currently doesn't do anything.


## `vars`

The vars key is an object of key/value pairs that are used can be used as variables within the `jobs` key. 

## `default`

The default values for jobs when values are not specified. 

`name`
:   Default: `'None'` · The name of the backup, this will be used to generate the destination file name

`source`
:   Default: `'None'` · The source directory or file to be zipped

`destination`
:   Default: `None | User Set'` · The destination directory where the zip files will be moved to. Must be a directory

`clean_up`
:   Default: `'false | User Set'` · When enabled, QuickZip will clean up the destination directory and only keep the newest `keep` number of files


`keep`
:   Default: `'4 | User Set'` · The number of files to keep when using `clean_up`.

`audit`
:   Default: `'true | User Set'` · Whether or not to audit the files in the backup directory

`oldest`
:   Default: `'7 | User Set'` · The oldest the newest backup in the audit directory can be


## `jobs`
The Jobs key is a list of jobs that are defined the same as the "defaults" refer to the defaults for key/value descriptions. A Full example is listed below to reference for formatting.


## Full Example
```toml
--8<-- 'docs_src/config.toml'
```

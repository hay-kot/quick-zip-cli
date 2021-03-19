# Usage Examples
Here are some examples of how I've been using Quick-Zip to manage small backup jobs on my systems. Have a cool use case? Submit a PR! 

## Backing Up Your Backups! 
Home Assistant uses it's automation tool to automatically create backups. While there are automatic solutions for uploading these to Google drive, there are not other options. As such I've adopted QuickZip to use as a way to grab the backups and store them in an off-site location. 

When called, QuickZip will pull the most recent .tar file from the folder, zip it, and copy it to the destination location on my NAS. It will then `audit` the destination directory and verify that the most recent file is within the specified date range. Once all of that's done, the payload with all the information gathered by QuickZip is then sent via `POST` request to my Home Assistant for display and notification purposes.

### Job Config
```json
{
    "name": "Home Assistant",
    "source": "${HOME_ASSISTANT}/backups",
    "destination": "${NAS_DIR}/auto-backups",
    "clean_up": true,
    "clean_up_source": true
},
```
!!! tip
    This examples what my primary use case for developing QuickZip.

## Backup Local Files
// TODO

## Backup Github Repo
// TODO

## Backup from Web API
// TODO
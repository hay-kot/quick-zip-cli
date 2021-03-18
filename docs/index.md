# About the Project

#### What QuickZip Is
QuickZip is a small utility I developed to solve a backup problem on my machines. I wanted a way to quickly backup up small sets of configuration files and data without deploying a massive, hard to maintain tool with too much front-end configuration. QuickZip uses a config.json file to build tiny list of backups that are conducted when called (typically via cron). 

#### What QuickZip Isn't
QuickZip is NOT a replacement for a robust backup or imaging software. It's primary use case is to collect configuration files on system other similar types of files, zip them up, and stick them somewhere else on your file system. 

## Commands

* `quickzip run` - Run the config file is the base directory. 
* `quickzip run "/path/to/config"` - Run a config file passed as an argument

## Not Yet Implemented Commands
* `quickzip audit` - Audits the destination directories and generates a report
* `quickzip html` - Same as above, but generates an HTML report. 


## Roadmap
- [ ] Pass list of files to zip in config file.
- [ ] CLI implementation
- [ ] Poetry Package
- [ ] Read config path from .env
- [ ] Encrypted Zip Files
[![Github All Releases](https://img.shields.io/github/downloads/hay-kot/quick_zip/total.svg)]()
[![GitHub Release](https://img.shields.io/github/release/hay-kot/quick_zip.svg?style=flat)]()
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

# About the Project

[Documentation](https://hay-kot.github.io/quick-zip-cli/)

## What QuickZip Is
QuickZip is a CLI utility I developed to solve a backup problem on my machines. I wanted a way to quickly backup up small sets of configuration files and data without deploying a massive, hard to maintain tool with too much front-end configuration. QuickZip uses a config.toml file to build tiny list of backups that are conducted when called (typically via cron). 

### Key Features
 - Create jobs with configuration file, including support for variables and defaults
 - Beautiful CLI
 - Backup Audits
 - Webhook Support


```console

$ quick-zip --help

Usage: qz [OPTIONS] COMMAND [ARGS]...

Options:
  --verbose / --no-verbose        [default: False]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  audit   🧐 Performs ONLY the audits for configured jobs
  config  📄 displays the configuration file
  docs    💬 Opens quickZip documentation in browser
  jobs
  run     ✨ The main entrypoint for the application.

```


## What QuickZip Isn't
QuickZip is NOT a replacement for a robust backup or imaging software. It's primary use case is to collect configuration files on system other similar types of files, zip them up, and stick them somewhere else on your file system. 

## Why not *x*???
I can't comment on every backup utility but I can mention the few that I looked at. **Borg** was a strong contender and I will likely use it for other things down the line, however I felt like there was too much upfront configuration before being able to use. **Rsync** / **Rclone** were both great options but I felt there were too confusing/robust for what I was trying to do. On top of that, I was looking for a few features that I hadn't seen. 

- Backup Audits: The ability to "audit" backups and specify how old the newest backup should be 
- Webhook Support: Send backup data to Home Assistant for notifications and dashboards. 

Also, I just like building stuff. 👍


## To Do's
- [x] Fix animated terminals for docs
- [x] Only run some jobs
- [x] Read config path from .env
- [x] CLI implementation
- [x] Auditor Commands
- [ ] Update Documentation
- [ ] Job Configuration
    - [x] Set default values
    - [x] Use variables in config file
    - [x] Add property for glob style matching
    - [x] Pass list of files to zip in config file.
    - [ ] Git Repo Backup
    - [ ] Web Download Backup
- [x] Tests
    - [x] Reading .toml file
    - [x] Find/Replace Vars
    - [x] Validate Input/Output
- [ ] Release v0.1.0
    - [ ] Poetry Package
- [ ] Encrypted Zip Files
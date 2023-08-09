# Disclaimer
Originally I use MacOS for developing and write all scripts for Mac. Ispite of this there isn't any reason for not working on Linux systems but could get some difficulties on Windows.

# VS Code and miniconda intergration
## Mac OS
### Install the miniconda distro if it's needed 
```
# curl -o /tmp/m.sh -s https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-MacOSX-arm64.sh && bash /tmp/m.sh -b -p $HOME/miniconda
```
### Prepare a separate env
```
# ~/miniconda/bin/conda env create -f ./develop/miniconda-environment.yml
# ~/miniconda/envs/clickhouse_table_exporter/bin/pip list local | grep click
```
## vs code config
A workspace configuration into ./.vscode/settings.json. It contains the path for the miniconda env for syntax and methods highlighting.

# How to run 
## a test env
```
./develop/compose.sh
```
You need to run this command from root directory of the git repository. It uses docker and docker compose.

## tests
```
./tests/run.sh
```
The test env is needed!

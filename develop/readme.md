<!-- TOC -->

- [Disclaimer](#disclaimer)
- [VS Code and miniconda intergration](#vs-code-and-miniconda-intergration)
    - [Mac OS](#mac-os)
        - [Install the miniconda distro if it's needed](#install-the-miniconda-distro-if-its-needed)
        - [Prepare a separate env](#prepare-a-separate-env)
    - [vs code config](#vs-code-config)
    - [Pip install test a built release](#pip-install-test-a-built-release)
- [How to run](#how-to-run)
    - [a test env](#a-test-env)
    - [tests](#tests)
    - [app](#app)
- [How to build](#how-to-build)
    - [Upload to test pypi](#upload-to-test-pypi)
    - [Upload to pypi](#upload-to-pypi)

<!-- /TOC -->

# Disclaimer
Originally I use MacOS for developing and write all scripts for Mac. Ispite of this there isn't any reason for not working on Linux systems but could get some difficulties on Windows.

# VS Code and miniconda intergration

## Mac OS

### Install the miniconda distro if it's needed 
```
# curl -o /tmp/m.sh -s https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-MacOSX-arm64.sh && bash /tmp/m.sh -b -p $HOME/miniconda
```

### Prepare a separate env
Create 
```
$ ~/miniconda/bin/conda env create -f ./develop/miniconda-environment.yml
```

Update
```
$ ~/miniconda/bin/conda env update -f ./develop/miniconda-environment.yml
```

Check
```
$ ~/miniconda/envs/clickhouse_table_exporter/bin/pip list local | egrep 'click|prom'
```

## vs code config
A workspace configuration into ./.vscode/settings.json. It contains the path for the miniconda env for syntax and methods highlighting.

## Pip install test a built release
```
$ ~/miniconda/bin/conda env create -f ./develop/miniconda-environment-pypi-test.yml
$ ~/miniconda/envs/clickhouse_table_exporter_pypi_test/bin/python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ clickhouse-table-exporter
$ ~/miniconda/envs/clickhouse_table_exporter_pypi_test/bin/python3 ~/miniconda/envs/clickhouse_table_exporter_pypi_test//lib/python3.9/site-packages/exporter.py
$ ~/miniconda/bin/conda env remove -n clickhouse_table_exporter_pypi_test
```

# How to run 

## a test env
```
$ ./develop/compose.sh
```
You need to run this command from root directory of the git repository. It uses docker and docker compose.

## tests
```
$ ./tests/run.sh
```
The test env is needed!

## app
```
$ ./develop/run.sh
```
The test env is needed!

# How to build
You need a config file based on the root dir with name ./.pypirc.ini with your pypi tokens:
```
[testpypi]
  username = __token__
  password = pypi-...
[pypi]
  username = __token__
  password = pypi-...
```

## Upload to test pypi
Next run the following script:
```
$ ./develop/upload-test.sh
```

## Upload to pypi
```
$ ./develop/upload-prod.sh
```

## Build a docker container
```
$ ./develop/docker-build.sh
```
<!-- TOC -->

- [Clickhouse table exporter](#clickhouse-table-exporter)
- [Provided metrics](#provided-metrics)
- [Example output](#example-output)
- [How to install](#how-to-install)
    - [Docker](#docker)
    - [Python module from pypi](#python-module-from-pypi)
- [How to run](#how-to-run)
    - [Docker](#docker)
    - [Bare python](#bare-python)
    - [What is next?](#what-is-next)
    - [Dev env](#dev-env)
- [How to setup](#how-to-setup)
- [Dependencies](#dependencies)
- [Roadmap](#roadmap)
- [Credits](#credits)

<!-- /TOC -->

# Clickhouse table exporter
A Python exporter for collecting clickhouse tables sizes.

# Provided metrics

All metrics have two default labes: database and table.

- clickhouse_table_exporter_table_size - size in bytes
- clickhouse_table_exporter_table_rows - rows in table
- clickhouse_table_exporter_table_days - difference between max_time and min_time of a table
- clickhouse_table_exporter_table_avg_day_size - size / the difference

# Example output
```
$  curl -s 127.0.0.1:9001/ | egrep '^clickhouse_table_exporter_table.*foo'
clickhouse_table_exporter_table_size{database="foo",table="t1"} 71394.0
clickhouse_table_exporter_table_size{database="foo",table="t2"} 23827.0
clickhouse_table_exporter_table_rows{database="foo",table="t1"} 300.0
clickhouse_table_exporter_table_rows{database="foo",table="t2"} 100.0
clickhouse_table_exporter_table_days{database="foo",table="t1"} 11.0
clickhouse_table_exporter_table_days{database="foo",table="t2"} 11.0
clickhouse_table_exporter_table_avg_day_size{database="foo",table="t1"} 6237.17527149184
clickhouse_table_exporter_table_avg_day_size{database="foo",table="t2"} 2072.2592542634943
```

# How to install
## Docker
```
$ docker pull alexeyantropov/clickhouse-table-exporter
```
## Python module from pypi
```
$ python3 -m pip install clickhouse-table-exporter
```

# How to run
## Docker
```
$ docker run -t -i -p 9001:9001 \
    --env CLICKHOUSE_HOST=192.168.50.120 --env CLICKHOUSE_PORT=8123 \
    --env CLICKHOUSE_USER=my_exporter --env CLICKHOUSE_PASS=your_exporter \
    clickhouse-table-exporter
```
## Bare python
E.g. for rpm packages
```
$ python3 /.../site-packages/exporter.py
```
## What is next?
Now the exporter is ready to scrape by Promethus.

## Dev env 
```
$ CH_TE_DEBUG=1 ./develop/run.sh
```

# How to setup
All configuration is provided by environment variables

- CH_TE_POLL_INTERVAL - polling interval in seconds (default: 10)
- CH_TE_PORT - exporter port (default: 9001)
- CH_TE_DEBUG - enable debug logging
- CLICKHOUSE_HOST - a clickhouse instence host  
- CLICKHOUSE_PORT - a clickhouse instence port, http port
- CLICKHOUSE_USER - user (is optionable)
- CLICKHOUSE_PASS - password (is optionable)

# Dependencies
- clickhouse_connect
- prometheus_client

# Roadmap
- Github releases

# Credits
- Thx for all cool guys and gals in this thread https://gist.github.com/sanchezzzhak/511fd140e8809857f8f1d84ddb937015
- How to write an exporter on Python https://trstringer.com/quick-and-easy-prometheus-exporter/
- Clickhouse connector https://clickhouse.com/docs/en/integrations/python
- How to deploy a Python package https://packaging.python.org/en/latest/tutorials/packaging-projects/
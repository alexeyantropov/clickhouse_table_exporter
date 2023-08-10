'''
A little convention about test names: test_(1)___(2), where:
1 - Name of a functionality or a method;
2 - A clarification or a detail describes the test.
'''

import sys
import os

import clickhouse_connect

sys.path.append('.')
import src as clickhouse_table_exporter

ch_host = os.getenv('CLICKHOUSE_HOST', None)
ch_port = os.getenv('CLICKHOUSE_PORT', None)
ch_user = os.getenv('CLICKHOUSE_USER', '')
ch_pass = os.getenv('CLICKHOUSE_PASS', '')
 
ex = clickhouse_table_exporter.Exporter(host=ch_host, port=ch_port, user='aaa', password='bbb')

# Broken exporter
def test_client_setup___fail_1():
    ex._Exporter__client_setup()
    assert ex._Exporter__client_setup() is None

def test_self_check___fail_1():
    assert ex.self_check() == False

def test_query___fail_1():
    res = ex._Exporter__query()
    assert len(res) == 0

def test_fetch___fail_1():
    assert ex._Exporter__fetch() == False

# Now it's fixed
def test_update_creds():
    ex._Exporter__update_creds(user=ch_user, password=ch_pass)

def test_self_check___1():
    assert ex.self_check() == True

def test_client_setup___1():
    assert ex._Exporter__client_setup() is not None

def test_query___1():
    res = ex._Exporter__query()
    assert len(res) == 7

def test_fetch___1():
    assert ex._Exporter__fetch() == True

def test_run_metrics_loop___1():
    steps = 3
    assert ex.run_metrics_loop(1, steps) == steps

def test_run_metrics_loop___2():
    steps = 1
    assert ex.run_metrics_loop("1", steps) == 1
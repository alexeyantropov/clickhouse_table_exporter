import datetime
import logging
import os
import time

import clickhouse_connect
from prometheus_client import Gauge, start_http_server

if __name__ == '__main__':
    logging.basicConfig(format = '%(asctime)s %(message)s', level=20)

class Exporter:
    def __init__(self, *, host: str, port: int, user='', password='', debug=False):
        # Clickhouse credentials
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.client_additional_kwargs = {}
        if user != '':
            self.client_additional_kwargs['username'] = user
        if password != '':
            self.client_additional_kwargs['password'] = password
        self.clickhouse_client = None
        # Prometheus setup
        labels = ['database', 'table']
        self.table_size = Gauge('clickhouse_table_exporter_table_size', 'Table size, bytes.', labels)
        self.table_rows = Gauge('clickhouse_table_exporter_table_rows', 'Table rows, count.', labels)
        self.table_days = Gauge('clickhouse_table_exporter_table_days', 'Table days, count.', labels)
        self.table_avg_day_size = Gauge('clickhouse_table_exporter_table_avg_day_size', 'Average size per day, bytes.', labels)

    # A helper for better tests coverage.
    def __update_creds(self, *, user='', password=''):
        if user != '':
            self.client_additional_kwargs['username'] = user
        if password != '':
            self.client_additional_kwargs['password'] = password

    def __client_setup(self) -> clickhouse_connect:
        c = None
        is_initialized = 'is initialized'
        try:
            c = clickhouse_connect.get_client(host=self.host, port=self.port, **self.client_additional_kwargs)
        except Exception as err:
            is_initialized = 'is NOT initialized'
            logging.critical('An error occurred during the initialization the clickhouse client:\n---\n{}\n---\n'.format(err))
        logging.info('The clickhouse client {}, host: {}, port: {}.'.format(is_initialized, self.host, self.port))
        return(c)
    
    def __query(self) -> list():
        q = '''
SELECT database, table, size, rows, days, avgDaySize FROM (
    SELECT
        database,
        table,
        sum(bytes) AS size,
        sum(rows) AS rows,
        min(min_time) AS min_time,
        max(max_time) AS max_time,
        toUInt32((max_time - min_time) / 86400) AS days,
        size / ((max_time - min_time) / 86400) AS avgDaySize
    FROM system.parts
    WHERE active
    GROUP BY database, table
)
'''
        if self.clickhouse_client is None:
            self.clickhouse_client = self.__client_setup()

        if self.clickhouse_client is None:
            logging.critical('Query: smth wrong with the clickhouse client.')
            return(list())

        r = self.clickhouse_client.query(q)
        return(r.result_rows)

    def __fetch(self):
        #     database, table,      size,  rows, days, avgDaySize
        # [ ('foo',    't1',        71427, 300,  11,   6201.612483431497),
        #   ('system', 'query_log', 26498, 117,   0,   inf) ]
        data = self.__query()
        if len(data) > 0:
            logging.info('Data collected from the clickhouse, rows: {}'.format(len(data)))
        else:
            logging.warn('The clickhouse server ({}:{}) has returned an empyty data!')
            return(False)
        
        for i in range(len(data)):
            logging.debug('Clickhouse responce (row):\n---\n{}\n---\n'.format(data[i]))
            labels = [data[i][0], data[i][1]]
            self.table_size.labels(*labels).set(data[i][2])
            self.table_rows.labels(*labels).set(data[i][3])
            self.table_days.labels(*labels).set(data[i][4])
            if data[i][5] == float('inf'):
                avg_day_size = 0
            else:
                avg_day_size = data[i][5]
            self.table_avg_day_size.labels(*labels).set(avg_day_size)
        return(True)

    def run_metrics_loop(self, interval, steps=float('inf')):
        if type(interval) == str and interval.isdigit():
            self.interval = int(interval)
        else:
            self.interval = interval

        i = 0
        while True and i < steps:
            self.__fetch()
            i += 1
            time.sleep(self.interval)
        return(i)
    
    def self_check(self) -> bool:
        q = 'SELECT NOW()'
        if self.clickhouse_client is None:
            self.clickhouse_client = self.__client_setup()
        try:
            r = self.clickhouse_client.query(q)
            # r.result_rows = [(datetime.datetime(2023, 8, 10, 13, 12, 49, tzinfo=<UTC>),)]
            if len(r.result_rows) > 0 and r.result_rows[0][0].year == datetime.date.today().year: 
                return(True)
        except Exception as err:
            logging.critical('An error occurred during the self cheking:\n---\n{}\n---\n'.format(err))
        return(False)
           
def main():
    poll_interval = int(os.getenv('CH_TE_POLL_INTERVAL', 10))
    exporter_port = int(os.getenv('CH_TE_PORT', 9001))
    debug_enable = os.getenv('CH_TE_DEBUG', '')
    ch_host = os.getenv('CLICKHOUSE_HOST', None)
    ch_port = os.getenv('CLICKHOUSE_PORT', None)
    ch_user = os.getenv('CLICKHOUSE_USER', '')
    ch_pass = os.getenv('CLICKHOUSE_PASS', '')

    if debug_enable != '':
        logging.getLogger().setLevel(logging.DEBUG)
    if ch_host is None:
        logging.critical('The env variable CLICKHOUSE_HOST is not set!')
        return(None)
    if ch_port is None:
        logging.critical('The env var CLICKHOUSE_PORT is not set!')
        return(None)

    logging.debug('debug is enable')
    logging.info('clickhouse_table_exporter started! ')
    logging.info('poll interval: {}, listen port: {}, clickhouse host: {}, port: {}, user is set: "{}", password is set: "{}".'.
                 format(poll_interval, exporter_port, ch_host, ch_port, ch_user!='', ch_pass!=''))
    
    logging.info('Setting up a clickhouse client.')
    ex = Exporter(host=ch_host, port=ch_port, user=ch_user, password=ch_pass)

    logging.info('Doing a self check...')
    if not ex.self_check():
        logging.info('Self check DID NON passed!')
        return(False)

    logging.info('Self check passed, staring the web-server and the main loop.')
    start_http_server(int(exporter_port))
    ex.run_metrics_loop(poll_interval)

if __name__ == '__main__':
    main()
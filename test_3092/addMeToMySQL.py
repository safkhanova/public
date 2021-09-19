import sys
import csv
from config import DB_SETTINGS
from datetime import date, datetime
from contextlib import contextmanager
import pymysql

file_path=sys.argv[1]
@contextmanager
def get_connection(DB_SETTINGS):
    db_user = DB_SETTINGS['user']
    db_pass = DB_SETTINGS['password']
    db_name = DB_SETTINGS['db']
    db_host = DB_SETTINGS['host']
    connection = pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name)
    try:
        yield connection
    finally:
        connection.close()

with get_connection(DB_SETTINGS) as conn:
    with conn.cursor() as cursor:
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            output_data = ""
            line_count = 0
            real_lines = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    try:
                        if row[0]=="":
                            pass
                        else:
                            d = date.strftime(datetime.strptime(row[0], "%d/%m/%y"), "%Y-%m-%d")
                            adUnitId = int(row[2])
                            typetag = int(row[3])
                            queries = int(row[6].replace(",", ""))
                            clicks = int(row[7])
                            impressions = int(row[8].replace(",", ""))
                            pageRpm = float(row[9])
                            impressionsRPM = float(row[10])
                            trueRevenue = float(row[11][1:])
                            coverage = float(row[12][:-1])
                            ctr = float(row[13])
                            cursor.execute(f'INSERT INTO {DB_SETTINGS["table_name"]} (date, adUnitName, adUnitId,typetag, revenueSource, '
                                           'market, queries, clicks, impressions, pageRpm, impressionRpm, trueRevenue, coverage, ctr) values '
                                           f'("{d}", "{row[1]}", {adUnitId}, {typetag}, "{row[4]}", "{row[5]}",{queries},{clicks},'
                                           f'{impressions},{pageRpm},{impressionsRPM}, {trueRevenue},{coverage},{ctr});')
                            conn.commit()
                            real_lines += 1
                    except IndexError:
                        pass
                    line_count += 1
            print(f"Total amount of lines: {line_count}")
            print(f"Processed: {real_lines} lines")
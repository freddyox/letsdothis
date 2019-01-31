#!/usr/bin/python3

import MySQLdb

db = MySQLdb.connect(host='localhost',
                     user='freddy',
                     passwd='N@c1remaLane88',
                     db='app')
cur = db.cursor()

sql_select_query = """select * from race_info where race_type = %s"""
cur.execute(sql_select_query, ('10K', ))
record = cur.fetchall()

for row in record:
    print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

db.close()

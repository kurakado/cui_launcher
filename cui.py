# -*- coding: utf-8
import sys,os
from subprocess import check_call
import sqlite3

#DB準備
dbname = 'launcher.db'

conn = sqlite3.connect(dbname)
c = conn.cursor()
sql="SELECT * FROM sqlite_master WHERE type=\'table\' and name=\'{}\'".format("shortcuts")
c.execute(sql)
if c.fetchone() == None:
    sql='create table shortcuts (id int, name varchar(64), path varchar(128))'
    c.execute(sql)

#sql='insert into shortcuts  '
sql="select max(id) from shortcuts"
c.execute(sql)
ret=c.fetchone()
if ret[0] == None:
    max_id=-1
else:
    max_id=ret[0]


while True:
    input_data=raw_input(">> ")
    if input_data in ["exit","quit","bye"]:
        break
    args=[]
    args=input_data.split()
    if len(args)==0:
        continue
    elif len(args)>=2 and args[0] == "add" :
        max_id=max_id+1
        name=os.path.basename(args[1])
        path=args[1]
        sql="insert into shortcuts values ({},'{}','{}')".format(max_id,name,path)
        print sql
        c.execute(sql)
    elif args[0] == "show":
        sql="select * from shortcuts"
        c.execute(sql)
        for raw in c.fetchall():
                print raw
    elif args[0] == "do" and len(args)>=1 and args[1].isdigit():
        sql="select path from shortcuts where id = {}".format(args[1])
        c.execute(sql)
        file_path=c.fetchone()[0]
        check_call(file_path)
    elif args[0] == "delete" and len(args)>=1 and args[1].isdigit():
        sql="delete from shortcuts where id = {}".format(args[1])
        c.execute(sql)
    elif args[0] =="save":
        conn.commit()
conn.close()

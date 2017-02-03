# -*- coding: utf-8

import sys,os
from subprocess import check_call,Popen
import sqlite3



#DB準備
dbname = 'launcher.db'

conn = sqlite3.connect(dbname)
conn.text_factory = str
c = conn.cursor()
sql="SELECT * FROM sqlite_master WHERE type=\'table\' and name=\'{}\'".format("shortcuts")
c.execute(sql)
if c.fetchone() == None:
    sql='create table shortcuts (id int, name varchar(64), path varchar(128), type varshce(16))'
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
    try:
        input_data=raw_input(">> ")
        if input_data in ["exit","quit","bye"]:
            break
        args=[]
        args=input_data.split()
        if len(args)==0:
            continue
            
        elif len(args)>=2 and args[0] == "add" :
            max_id=max_id+1
            args[1]=args[1].replace("@"," ")
            if os.path.isdir(args[1]):
                type="directory"
            elif os.path.isfile(args[1]):
                type="file"
            name=os.path.basename(args[1])
            path=args[1]
            sql="insert into shortcuts values ({},'{}','{}','{}')".format(max_id,name,path,type)
            c.execute(sql)
            
        elif args[0] == "show":
            if len(args) >= 2:
                if args[1] in ["d","dir","directory"]:
                    type="directory"
                elif args[1] in ["f","file"]:
                    type="file"
                sql="select * from shortcuts where type = \"{}\"".format(type)
            else:
                sql="select * from shortcuts"
            sql=sql+" order by id"
            c.execute(sql)
            for raw_data in c.fetchall():
                    print "{}{}{}".format(str(raw_data[0]).ljust(4," "),raw_data[1].ljust(32," "),raw_data[3])
        
        elif args[0].isdigit():
            sql="select * from shortcuts where id = {}".format(args[0])
            c.execute(sql)
            raw_data=c.fetchone()
            file_path=raw_data[2]
            if len(args)==1:
                if raw_data[3]=="file":
                    Popen(file_path)
                elif raw_data[3]=="directory":
                    os.popen("explorer {}".format(file_path))
            elif len(args)>=2:
                sql="select path from shortcuts where id = {}".format(args[1])
                c.execute(sql)
                file_path2=c.fetchone()[0]
                Popen([file_path,file_path2])
                
        elif args[0] == "do" and len(args)>=2 and args[1].isdigit():
            sql="select * from shortcuts where id = {}".format(args[1])
            c.execute(sql)
            raw_data=c.fetchone()
            file_path=raw_data[2]
            if len(args)==2:
                if raw_data[3]=="file":
                    Popen(file_path)
                elif raw_data[3]=="directory":
                    os.popen("explorer {}".format(file_path))
            elif len(args)>=3:
                sql="select path from shortcuts where id = {}".format(args[2])
                c.execute(sql)
                file_path2=c.fetchone()[0]
                Popen([file_path,file_path2])
                
        elif args[0] == "delete" and len(args)>=2 and args[1].isdigit():
            sql="delete from shortcuts where id = {}".format(args[1])
            c.execute(sql)
            
        elif args[0] =="save":
            conn.commit()
            
        elif args[0] == "info" and len(args)>=2 and args[1].isdigit():
            sql="select path from shortcuts where id = {}".format(args[1])
            c.execute(sql)
            print c.fetchone()[0]
            
        elif args[0] == "rename" and len(args)>=3 and args[1].isdigit():
            sql="update shortcuts set name = \"{name}\" where id = \"{id}\"".format(name=args[2],id=args[1])
            c.execute(sql)
            
        elif args[0] == "change" and len(args)>=3 and args[1].isdigit() and args[2].isdigit():
            before_num=args[1]
            after_num=args[2]
            #変更後番号を現在使用しているレコードが存在するか確認
            sql="select * from shortcuts where id={}".format(after_num)
            c.execute(sql)
            ret=c.fetchone()
            #変更後番号が使われていない番号なら、単に番号変更
            if ret==None:
                print "a"
                sql="update shortcuts set id = \"{after}\" where id =\"{before}\"".format(after=after_num,before=before_num)
                print sql
                c.execute(sql)
            #変更後番号が使われている番号なら、番号入れ替え
            else:
                sql="update shortcuts set id = \"{after}\" where id =\"{before}\"".format(after=37564,before=after_num)
                c.execute(sql)
                sql="update shortcuts set id = \"{after}\" where id =\"{before}\"".format(after=after_num,before=before_num)
                c.execute(sql)
                sql="update shortcuts set id = \"{after}\" where id =\"{before}\"".format(after=before_num,before=37564)
                c.execute(sql)

        
        
        elif args[0] == "help":
            print """add path (don't save)
delete number (don't save)
show
info number
do number
rename number after_name
change before_number after_number
save
help"""
    except Exception as e:
        print "error:{}".format(e.message)
conn.close()


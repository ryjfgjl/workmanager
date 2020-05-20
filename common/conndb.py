# connect to mysql

import pymysql
import os
from common.handleconfig import HandleConfig

class ConnDB():

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.server = self.HandleConfig.handle_config("g", "global", "use_server")
        self.host = self.HandleConfig.handle_config('g', self.server, 'host')
        self.user = self.HandleConfig.handle_config('g', self.server, 'user')
        self.passwd = self.HandleConfig.handle_config('g', self.server, 'password')
        self.port = int(self.HandleConfig.handle_config('g', self.server, 'port'))

    def conndb(self, db=None, charset='utf8'):
        self.db = db
        conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port, charset=charset, database=db)

        return conn

        # execute sql
    def exec(self, conn, sql):
        cur = conn.cursor()
        for s in sql.split(";"):
            if s != "":
                cur.execute(s)

        conn.commit()
        cur.close()
        return cur

    # exec cmd
    def cmd(self, dbname, op, sqlfile):
        if op == "mysql":
            cmd_statement = "{0} -u{1} -p{2} -h{3} -P{4} {5} --default-character-set=utf8 < \"{6}\"".format(op,self.user,self.passwd,self.host,self.port,dbname,sqlfile)
        elif op == "mysqldump":
            cmd_statement = "{0} -u{1} -p{2} -h{3} -P{4} {5} -R > \"{6}\"".format(op,self.user,self.passwd,self.host,self.port,dbname,sqlfile)
        elif op == "mysqldump-no-r":
            cmd_statement = "mysqldump -u{0} -p{1} -h{2} -P{3} {4} > \"{5}\"".format(self.user,self.passwd,self.host,self.port,dbname,sqlfile)

        print(cmd_statement)
        ret = os.system(cmd_statement)

        return ret
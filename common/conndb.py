# connect to mysql

import pymysql
import os
from common.handleconfig import HandleConfig


class ConnDB:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.server = self.HandleConfig.handle_config("g", "global", "server")
        self.host = self.HandleConfig.handle_config('g', self.server, 'host')
        self.user = self.HandleConfig.handle_config('g', self.server, 'user')
        self.passwd = self.HandleConfig.handle_config('g', self.server, 'password')
        self.port = int(self.HandleConfig.handle_config('g', self.server, 'port'))

    # return a connection
    def conndb(self, db=None, server=None, charset='utf8'):
        if server:
            host = self.HandleConfig.handle_config('g', server, 'host')
            user = self.HandleConfig.handle_config('g', server, 'user')
            passwd = self.HandleConfig.handle_config('g', server, 'password')
            port = int(self.HandleConfig.handle_config('g', server, 'port'))
        else:
            host = self.host
            user = self.user
            passwd = self.passwd
            port = self.port
        conn = pymysql.connect(host=host, user=user, passwd=passwd, port=port, charset=charset, database=db)

        return conn

    # execute sql
    def exec(self, conn, sql, kill=True, datalist=[]):
        cur = conn.cursor()
        host = conn.host
        # kill db process first
        if host == '192.168.1.188':
            pid = conn.thread_id()
            #currentwork = self.HandleConfig.handle_config("g", "global", "currentwork")
            database = conn.db

            if database:
                database = database.decode('utf8')
                killsql = "SELECT CONCAT('kill ',id) FROM information_schema.`PROCESSLIST` WHERE DB = '{0}' and id <> {1}".format(database, pid)
                cur.execute(killsql)
                killids = cur.fetchall()
                killids = list(killids)

                idx = 0
                for killid in killids:
                    killids[idx] = (list(killid))[0]
                    killidsql = killids[idx]
                    try:
                    	cur.execute(killidsql)
                    except:
                    	continue
                    idx = idx + 1
        
        if datalist:
            cur.executemany(sql, datalist)
        else:
            for s in sql.split(";"):
                if s != "":
                    cur.execute(s)

        conn.commit()
        cur.close()

        return cur

    # execute cmd
    # return 0 if success else 1
    def cmd(self, dbname, op, sqlfile, tablename=''):
        cmd_statement = ''
        if op == "mysql":
            cmd_statement = "{0} -u{1} -p{2} -h{3} -P{4} {5} --default-character-set=utf8 < \"{6}\"".format(op, self.user, self.passwd, self.host, self.port, dbname, sqlfile)
        elif op == "mysqldump":
            cmd_statement = "{0} -u{1} -p{2} -h{3} -P{4} {5} -R > \"{6}\"".format(op, self.user, self.passwd, self.host, self.port, dbname, sqlfile)
        elif op == "mysqldump-no-r":
            cmd_statement = "mysqldump -u{0} -p{1} -h{2} -P{3} {4} {5} > \"{6}\"".format(self.user, self.passwd, self.host, self.port, dbname, tablename, sqlfile)

        print('\n\n'+cmd_statement)
        ret = os.system(cmd_statement)

        return ret
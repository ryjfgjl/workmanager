
from common.handleconfig import HandleConfig
import PySimpleGUI as sg
from common.conndb import ConnDB
import pymysql
from datetime import date


class DbToDownload:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    def main(self, currentwork):
        dbname = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        sql = "insert into db_to_download.db_list_to_download(instanceName,department) select '{0}','data' from dual where '{0}' not in(select instanceName from db_to_download.db_list_to_download where importFlag is null and department = 'data')".format(dbname)
        conn_db = self.ConnDB.conndb(server='awshost')
        try:
            try:
                self.ConnDB.exec(conn_db, sql)
                sg.Popup('\n DB to download   Complete!         \n', title=currentwork)
            except pymysql.err.IntegrityError:
                sql = "select * from db_to_download.db_download_log where instanceName = '{0}' and DATE(completeTime) = '{1}'".format(dbname, date.today())
                ret = self.ConnDB.exec(conn_db, sql)
                result = ret.fetchall()
                if len(result) == 0:
                    sql = "update db_to_download.db_list_to_download set deleteTime = now(), downloadTime = now(), importFlag = null, department = 'data' where instanceName = '{0}'".format(dbname)
                    self.ConnDB.exec(conn_db, sql)
                else:
                    sg.Popup('\n  {0} downloaded, you can go to mysqldump   \n'.format(dbname), title=currentwork)
                    return
                sg.Popup('\n  DB to download  Complete!         \n', title=currentwork)
            except:
                sg.popup_error('\n  DB to download  Error!         \n', title=currentwork)

        finally:
            conn_db.close()

    def check(self):
        pass


if '__name__' == '__main__':
    DbToDownload = DbToDownload()
    DbToDownload.main('')
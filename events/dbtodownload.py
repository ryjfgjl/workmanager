
from common.handleconfig import HandleConfig
import PySimpleGUI as sg
from common.conndb import ConnDB

sg.ChangeLookAndFeel('GreenTan')

class DbToDownload:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    def main(self, currentwork):

        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")
        sql = "insert into db_to_download.db_list_to_download(instanceName,department) select '{0}','data' from dual where '{0}' not in(select instanceName from db_to_download.db_list_to_download where importFlag is null and department = 'data')".format(
            dbname)
        conn_db = self.ConnDB.conndb(server='aws201')
        try:
            self.ConnDB.exec(conn_db, sql)
            sg.Popup('\n    Complete!         \n', )
        except:
            sg.Popup('\n    Error!         \n', )
        finally:
            conn_db.close()











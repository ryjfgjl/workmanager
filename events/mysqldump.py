"""
Dump mysql
"""

import PySimpleGUI as sg
import shutil
from datetime import datetime
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import gzip,os

sg.ChangeLookAndFeel('GreenTan')

class MysqlDump:

    def __init__(self):

        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.imgpath = self.HandleConfig.handle_config("g", "referencefile", "img")
        self.use_server = self.HandleConfig.handle_config("g", "global", "use_server")

    def main(self, currentwork):

        jirapath = self.HandleConfig.handle_config("g", currentwork, "jirapath")
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")

        layout = [
            [sg.Text('Database Name')],
            [sg.InputText('{0}'.format(dbname), key='dbname')],
            [sg.Text('Gzip?')],
            [sg.Radio('Yes', 'R0', key='y'), sg.Radio('No', 'R0', default=True, key='n')],
            [sg.Text('filename'), sg.Combo(['{0}.sql'.format(dbname), '{0}_bakup.sql'.format(dbname)], default_value='{0}.sql'.format(dbname), key='f')],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]
        ]
        window = sg.Window('', layout=layout, )
        event, values = window.read()
        window.close()

        if event in (None, 'Cancel'):
            return
        dbname = values['dbname'].strip().lower()

        if values['y']:
            gz = True
        else:
            gz = False

        sqlfile = values['f']

        if gz:
            sqlfile = jirapath + "fulldata\\" + sqlfile
            sqlfile_gzip = jirapath + "\\fulldata\\{0}.sql.gz".format(dbname)
            ret = self.ConnDB.cmd(dbname, "mysqldump", sqlfile)
            if ret == 0:
                with open(sqlfile, 'rb') as f_in, gzip.open(sqlfile_gzip, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                os.remove(sqlfile)
                sg.Popup('Complete!')
        else:
            if sqlfile.endswith("_bakup"):
                op = "mysqldump"
            else:
                op = "mysqldump-no-r"
            sqlfile = jirapath + "scripts\\" + sqlfile
            ret = self.ConnDB.cmd(dbname, op, sqlfile)
            if ret == 0:
                with open(sqlfile, "a") as fa:
                    fa.write("COMMIT;")
                now = datetime.now().strftime('%b-%d-%Y %H:%M:%S').replace(' ', '').replace(':', '')
                newfile = jirapath + "\\scripts_bak\\{0}".format(dbname) + "_" + now + "_bak.sql"
                shutil.copy(sqlfile, newfile)
                sg.Popup('Complete!')
            else:
                sg.Popup('Failed!')
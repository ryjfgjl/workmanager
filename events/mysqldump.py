
"""
Dump mysql
"""

import shutil
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import gzip
import os
import PySimpleGUI as sg


class MysqlDump:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    def main(self, currentwork, advanced=0, gz=False, after=0, op='mysqldump-no-r'):
        jirapath = self.HandleConfig.handle_config('g', currentwork, 'jirapath')
        dbname = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        sqlname = '{0}.sql'.format(dbname)
        sqlfile = jirapath + 'script\\' + sqlname
        if after:
            sqlfile = jirapath + 'script\\' + '{0}_after.sql'.format(dbname)
        if not op:
            op = 'mysqldump-no-r'
        tablesname = ''

        if advanced:
            layout = [
                [sg.Text('Database Name: {0}'.format(dbname))],
                [sg.Text('Tables Name:'), sg.InputText(key='tablesname')],
                [sg.Text('File Name:'), sg.InputText(key='filename')],
                [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]
            ]
            window = sg.Window('', layout=layout)
            event, values = window.read()
            window.close()
            if event in (None, 'Cancel'):
                return
            tablesname = values['tablesname']
            filename = values['filename']
            if filename:
                sqlfile = jirapath + 'script\\' + filename

        if gz:
            sqlfile = jirapath + 'db_backup\\' + sqlname
            sqlfile_gzip = jirapath + '\\db_backup\\{0}.sql.gz'.format(dbname)
            op = 'mysqldump'
            ret = self.ConnDB.cmd(dbname, op, sqlfile)
            if ret == 0:
                with open(sqlfile, 'rb') as (f_in):
                    with gzip.open(sqlfile_gzip, 'wb') as (f_out):
                        shutil.copyfileobj(f_in, f_out)
                os.remove(sqlfile)
        else:
            ret = self.ConnDB.cmd(dbname, op, sqlfile, tablesname)
            if ret == 0:
                with open(sqlfile, 'a') as (fa):
                    fa.write('COMMIT;')
            if advanced:
                sg.Popup('Complete!')


if '__name__' == '__main__':
    MysqlDump = MysqlDump()
    MysqlDump.main('')
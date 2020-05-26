"""
Restore mysql database
"""

from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg
import os

#print = sg.Print

sg.ChangeLookAndFeel('GreenTan')

class MysqlRestore:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()

    def main(self, currentwork, sqlfiles=None):
        jirapath = self.HandleConfig.handle_config("g", currentwork, "jirapath")
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")
        git_repo_path = self.HandleConfig.handle_config("g", "defaultpath", "git_repo_path")
        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'
        scriptspath = jirapath + "scripts\\"
        if not sqlfiles:
            sqlfiles = [
                scriptspath + '{0}_bakup.sql'.format(dbname),
                scriptspath + '{0}.sql'.format(dbname),
                scriptspath + 'configration.sql',
                gitscriptpath + 'functionAndProcedure.sql'
            ]

        sql = "drop database if exists `{}`;create database `{}`;".format(dbname, dbname)
        self.ConnDB.exec(self.conn, sql)

        for sqlfile in sqlfiles:
            if not os.path.exists(sqlfile):
                continue
            ret = self.ConnDB.cmd(dbname, "mysql", sqlfile)
            if ret == 0:
                print("Success: {}\n".format(sqlfile))
            else:
                print("Failed: {}\n".format(sqlfile))
                sg.Popup('Error!')
                return

        sg.Popup('Complete!')
        return 1

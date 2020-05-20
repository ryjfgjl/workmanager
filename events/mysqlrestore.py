"""
Restore mysql database
"""

from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')

class MysqlRestore:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()
        self.imgpath = self.HandleConfig.handle_config("g", "referencefile", "img")

    def main(self, currentwork, sqlfiles=None):
        jirapath = self.HandleConfig.handle_config("g", currentwork, "jirapath")
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")


        scriptspath = jirapath + "scripts\\"
        if not sqlfiles:
            sqlfiles = [
                scriptspath + '\\{0}_bakup.sql'.format(dbname),
                scriptspath + '\\{0}.sql'.format(dbname),
            ]

        sql = "drop database if exists `{}`;create database `{}`;".format(dbname, dbname)
        self.ConnDB.exec(self.conn, sql)

        for sqlfile in sqlfiles:
            ret = self.ConnDB.cmd(dbname, "mysql", sqlfile)
            if ret == 0:
                print("Success: {}\n".format(sqlfile))
            else:
                sg.Popup('')
                return
        sg.Popup('Complete!')
        return 1

from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg
from events.mysqlrestore import MysqlRestore

sg.ChangeLookAndFeel('GreenTan')

class RunScript:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()
        self.MysqlRestore = MysqlRestore()
        self.imgpath = self.HandleConfig.handle_config("g", "referencefile", "img")

    def main(self, currentwork):
        jirapath = self.HandleConfig.handle_config("g", currentwork, "jirapath")
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")
        scriptspath = jirapath + "scripts\\"
        git_repo_path = self.HandleConfig.handle_config("g", "global", "git_repo_path")
        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'

        sqlfiles = [
            scriptspath + '\\{0}_bakup.sql'.format(dbname),
            scriptspath + '\\{0}.txt'.format(dbname),
            gitscriptpath + '\\accountMerge.sql',
            gitscriptpath + '\\fullDataClean.sql',
            gitscriptpath + '\\somke_test_after.sql'
        ]
        self.MysqlRestore.main(currentwork, sqlfiles)

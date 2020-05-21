from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg
from events.mysqlrestore import MysqlRestore
from events.mysqldump import MysqlDump

sg.ChangeLookAndFeel('GreenTan')

class RunScript:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()
        self.MysqlRestore = MysqlRestore()
        self.MysqlDump = MysqlDump()
        self.imgpath = self.HandleConfig.handle_config("g", "referencefile", "img")

    def main(self, currentwork):
        jirapath = self.HandleConfig.handle_config("g", currentwork, "jirapath")
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")
        scriptspath = jirapath + "scripts\\"
        git_repo_path = self.HandleConfig.handle_config("g", "global", "git_repo_path")
        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'
        navicat_script_path = self.HandleConfig.handle_config("g", "global", "navicat_script_path")
        script = navicat_script_path + dbname + '\\{}.sql'.format(currentwork)
        lines = []
        files = [
            scriptspath + 'configuration.sql',
            gitscriptpath + 'functionAndProcedure.sql',
            script,
            gitscriptpath + 'accountMerge.sql',
            gitscriptpath + 'fullDataClean.sql'
        ]
        for f in files:
            with open(f, 'r') as fa:
                flines = fa.readlines()
                lines.append(flines)
                lines.append('\n')
        with open(scriptspath + '{0}.txt'.format(dbname), 'w') as fw:
            fw.writelines(lines)


        sqlfiles = [
            scriptspath + '{0}_bakup.sql'.format(dbname),
            gitscriptpath + 'somke_test_b4.sql',
            scriptspath + '{0}.sql'.format(dbname),
            scriptspath + '{0}.txt'.format(dbname),
            gitscriptpath + 'somke_test_after.sql'
        ]
        self.MysqlRestore.main(currentwork, sqlfiles)
        sg.Popup('Complete!')



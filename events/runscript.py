from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg
from events.mysqlrestore import MysqlRestore
import shutil

sg.ChangeLookAndFeel('GreenTan')

class RunScript:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()
        self.MysqlRestore = MysqlRestore()

    def main(self, currentwork):
        jirapath = self.HandleConfig.handle_config("g", currentwork, "jirapath")
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")
        merge = self.HandleConfig.handle_config("g", currentwork, "merge")
        scriptspath = jirapath + "scripts\\"
        git_repo_path = self.HandleConfig.handle_config("g", "defaultpath", "git_repo_path")
        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'
        navicat_script_path = self.HandleConfig.handle_config("g", "defaultpath", "navicat_script_path")
        script = navicat_script_path + dbname + '\\{}.sql'.format(currentwork)
        lines = []
        files = [
            scriptspath + 'configration.sql',
            gitscriptpath + 'functionAndProcedure.sql',
            script,
            gitscriptpath + 'accountMerge.sql',
            gitscriptpath + 'fullDataClean.sql'
        ]
        if merge == 'False':
            files.remove(gitscriptpath + 'accountMerge.sql')
        with open(scriptspath + '{0}.txt'.format(dbname), 'w', encoding='utf8') as fw:
            fw.truncate()
        for f in files:
            with open(f, 'r', encoding='utf8') as fa:
                with open(scriptspath + '{0}.txt'.format(dbname), 'a+', encoding='utf8') as fw:
                    shutil.copyfileobj(fa, fw)
                    #fw.write('\n####################\n')

        sqlfiles = [
            scriptspath + '{0}_bakup.sql'.format(dbname),
            gitscriptpath + 'smokeTest.sql',
            scriptspath + '{0}.sql'.format(dbname),
            scriptspath + '{0}.txt'.format(dbname),
            gitscriptpath + 'smokeTest.sql'
        ]
        self.MysqlRestore.main(currentwork, sqlfiles)



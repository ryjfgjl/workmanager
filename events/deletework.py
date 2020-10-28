
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg
import shutil
import zipfile
import os
import pyperclip
from datetime import date


class DeleteWork:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    def main(self, currentwork):
        layout = [
            [sg.Text('Warnning!\n\nThis option will remove the work from the tool.\nDo you want to continue?')],
            [sg.OK(), sg.Button('Just Zip')]

        ]
        window = sg.Window(title=currentwork, layout=layout)
        event, values = window.read()
        window.close()
        if event is None:
            return 0
        
        navicat_script_path = self.HandleConfig.handle_config('g', 'defaultpath', 'navicat_script_path')
        jirapath = self.HandleConfig.handle_config('g', currentwork, 'jirapath')
        scriptspath = jirapath + 'script\\'
        git_repo_path = self.HandleConfig.handle_config('g', 'defaultpath', 'git_repo_path')
        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'
        dbname = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        sqlfile = scriptspath + '{0}.sql'.format(dbname)
        txtfile = scriptspath + '{0}.txt'.format(dbname)
        merge = self.HandleConfig.handle_config('g', currentwork, 'merge')

        script = navicat_script_path + dbname + '\\{}.sql'.format(dbname)
        script_after_merge = navicat_script_path + dbname + '\\{}_after_merge.sql'.format(dbname)
        script_after_template = navicat_script_path + dbname + '\\{}_after_template.sql'.format(dbname)
        files = [
             scriptspath + 'configration.sql',
             gitscriptpath + 'functionAndProcedure.sql',
             script,
             navicat_script_path + dbname + '\\{}_after_template.sql'.format(dbname),
             gitscriptpath + 'accountMerge.sql',
             script_after_merge,
             gitscriptpath + 'fullDataClean.sql',
             gitscriptpath + 'clear.sql'
        ]
        if merge == 'False':
            files.remove(gitscriptpath + 'accountMerge.sql')
        with open(txtfile, 'w', encoding='utf8') as (fw):
            fw.truncate()
        for f in files:
            with open(f, 'r', encoding='utf8') as (fa):
                with open(txtfile, 'a+', encoding='utf8') as (fw):
                    shutil.copyfileobj(fa, fw)

        # generate zipfile
        sqlfile_zip = scriptspath + '{0}.zip'.format(currentwork)
        if os.path.isfile(sqlfile_zip):
            os.remove(sqlfile_zip)
        zfile = zipfile.ZipFile(sqlfile_zip, 'w', zipfile.ZIP_DEFLATED)
        if os.path.isfile(sqlfile):
            zfile.write(sqlfile, '{0}.sql'.format(dbname))
        zfile.write(txtfile, '{0}.txt'.format(dbname))
        zfile.close()

        # upload zipfile
        winscppath = self.HandleConfig.handle_config('g', 'defaultpath', 'winscppath')
        cmd = '{0}WinSCP.com /command "open aws188" "put {1} /home/neon/leiwu/dataimport/script/" "exit"'.format(winscppath, sqlfile_zip)
        os.system(cmd)

        if event == 'Just Zip':
            return 0
        # remove work
        script_temp = jirapath + 'temp\\{}.sql'.format(dbname)
        script_after_merge_temp = jirapath + 'temp\\{}_after_merge.sql'.format(dbname)
        script_after_template_temp = jirapath + 'temp\\{}_after_template.sql'.format(dbname)
        if (not os.path.isfile(script_temp)) and os.path.isfile(script):
            shutil.move(script, script_temp)
        if (not os.path.isfile(script_after_merge_temp)) and os.path.isfile(script_after_merge):
            shutil.move(script_after_merge, script_after_merge_temp)
        if (not os.path.isfile(script_after_template_temp)) and os.path.isfile(script_after_template):
            shutil.move(script_after_template, script_after_template_temp)

        conn_db = self.ConnDB.conndb(server='awshost')
        sql = "update db_to_download.data_import_tracking set releaseDate = '{0}' where jiraId = '{1}' and releaseDate is null".format(date.today(),currentwork)
        self.ConnDB.exec(conn_db, sql)
        conn_db.close()

        self.HandleConfig.handle_config('rs', self.HandleConfig.handle_config('g', 'worklist', currentwork))
        self.HandleConfig.handle_config('ro', 'worklist', key=currentwork)
        works = [work for work in self.HandleConfig.handle_config()['worklist'].values()]
        currentwork = ''
        if works:
            currentwork = works[-1]
        self.HandleConfig.handle_config('s', 'global', 'currentwork', currentwork)
        cmd = '/home/neon/leiwu/bin/dataImportRunScript.sh {0}_test {0}'.format(dbname)
        sg.Popup('Complete!\n\n{0} has been copied.'.format(cmd), title=currentwork)
        pyperclip.copy(cmd)
        

if '__name__' == '__main__':
    DeleteWork = DeleteWork()
    DeleteWork.main('')
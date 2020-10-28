# create a new work
# 1) Make directory E:/work/YYYY/MM/DD/importType/jiraId/{excel,script,db_backup_temp}
# 2) Copy config.sql from git repository to ~/script
# 3) Create database
# 4) Add instance to db_list_to_download;
# 5) Add all import information to data_import_tracking
# 6) Create INSTANCE.sql, INSTANCE_AFTER_TEMPLATE.sql, INSTANCE_AFTER_MERGE.sql in navicat IF NOT EXISTS


from datetime import date, datetime
import os
import re
import shutil
import PySimpleGUI as sg
import pythoncom
from win32com.shell import shell
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
from events.dbtodownload import DbToDownload


class NewWork:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.DbToDownload = DbToDownload()
        self.ConnDB = ConnDB()

    def main(self):
        workpath = self.HandleConfig.handle_config('g', 'defaultpath', 'workpath')
        nickname = self.HandleConfig.handle_config('g', 'excelimporter', 'nickname')
        emptytxt = self.HandleConfig.handle_config('g', 'referencefile', 'emptytxt')
        git_repo_path = self.HandleConfig.handle_config('g', 'defaultpath', 'git_repo_path')
        navicat_script_path = self.HandleConfig.handle_config('g', 'defaultpath', 'navicat_script_path')
        desktoppath = self.HandleConfig.handle_config('g', 'defaultpath', 'desktoppath')

        # user input
        jiraname, dbname, worktype, cost, duedate = self.input_workinfo(workpath)
        if not worktype:
            return 0

        # create dictionary
        year = str(date.today().year)
        month = str(date.today().month)
        day = str(date.today().day)
        yearpath = workpath + year + '\\'
        monthpath = yearpath + month + '\\'
        daypath = monthpath + day + '\\'
        worktypepath = daypath + worktype.replace(' ', '_') + '\\'
        jirapath = worktypepath + jiraname + '\\'
        if not os.path.exists(yearpath):
            os.makedirs(yearpath)
        if not os.path.exists(monthpath):
            os.makedirs(monthpath)
        if not os.path.exists(daypath):
            os.makedirs(daypath)
        if not os.path.exists(worktypepath):
            os.makedirs(worktypepath)
        if not os.path.exists(jirapath):
            os.makedirs(jirapath)
        scriptspath = jirapath + 'script\\'
        scriptsbakpath = jirapath + 'db_backup\\'
        xlspath = jirapath + 'excel\\'
        queriespath = jirapath + 'temp\\'
        if not os.path.exists(scriptspath):
            os.makedirs(scriptspath)
        if not os.path.exists(scriptsbakpath):
            os.makedirs(scriptsbakpath)
        if not os.path.exists(xlspath):
            os.makedirs(xlspath)
        if not os.path.exists(queriespath):
            os.makedirs(queriespath)
        script = scriptspath + '{}.txt'.format(dbname)
        if not os.path.isfile(script):
            shutil.copyfile(emptytxt, script)
        tmpscript = scriptspath + 'tmp.txt'
        if not os.path.isfile(tmpscript):
            shutil.copyfile(emptytxt, tmpscript)

        # copy configration.sql from git repo
        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'
        configration_sql = gitscriptpath + 'configration.sql'
        configration_sql_new = jirapath + 'script\\configration.sql'
        if not os.path.isfile(configration_sql_new):
            shutil.copy(configration_sql, configration_sql_new)

        # write into config.ini
        # set as current work
        self.HandleConfig.handle_config('a', jiraname)
        self.HandleConfig.handle_config('s', jiraname, 'dbname', dbname)
        self.HandleConfig.handle_config('s', jiraname, 'jiraname', jiraname)
        self.HandleConfig.handle_config('s', jiraname, 'jirapath', jirapath)
        self.HandleConfig.handle_config('s', jiraname, 'worktype', worktype)
        self.HandleConfig.handle_config('s', jiraname, 'merge', 'True')
        self.HandleConfig.handle_config('s', 'worklist', jiraname, jiraname)
        self.HandleConfig.handle_config('s', 'global', 'currentwork', jiraname)

        # create database
        sql = 'drop database if exists `{0}`;create database `{0}`'.format(dbname, dbname)
        conn_db = self.ConnDB.conndb()
        self.ConnDB.exec(conn_db, sql)
        conn_db.close()

        navicat_db_path = navicat_script_path + dbname + '\\'
        if not os.path.exists(navicat_db_path):
            os.makedirs(navicat_db_path)
        navicatscript = navicat_db_path + '{}.sql'.format(dbname)
        if not os.path.isfile(navicatscript):
            shutil.copyfile(emptytxt, navicatscript)
        after_template_script = navicat_db_path + '{}_after_template.sql'.format(dbname)
        if not os.path.isfile(after_template_script):
            shutil.copyfile(emptytxt, after_template_script)
        after_merge_script = navicat_db_path + '{}_after_merge.sql'.format(dbname)
        if not os.path.isfile(after_merge_script):
            shutil.copyfile(emptytxt, after_merge_script)

        # create shortcut
        self.set_shortcut(jirapath, desktoppath, jiraname)

        # insert into data_import_tracking
        sql = "insert into db_to_download.data_import_tracking(jiraId,dataImportType,dataImportCost,productionInstance,developer,startDate,dueDate) " \
              "select '{0}','{1}','{2}','{3}','{4}','{5}','{6}' from dual"\
            .format(jiraname, worktype, cost, dbname, nickname, date.today(), duedate)
        conn_db = self.ConnDB.conndb(server='awshost')
        self.ConnDB.exec(conn_db, sql)
        conn_db.close()

        # Add instance to db_list_to_download
        currentwork = self.HandleConfig.handle_config("g", "global", "currentwork")
        self.DbToDownload.main(currentwork)

        sg.Popup('\n  New Work  Complete!         \n', title=currentwork)

    def input_workinfo(self, workpath):
        year = str(date.today().year)
        workpath = workpath + year + '\\'
        layout = [
         [
          sg.Frame(layout=[
           [
            sg.Radio('First Import', 'R0', default=True, key='first'),
            sg.Radio('Second Import', 'R0', key='second'),
            sg.Radio('Fix Import', 'R0', key='fix')]
          ],
            title='Work Type',
            title_color='red')
         ],
         [sg.Text('Jira Name:')],
         [sg.InputText(key='jiraname')],
         [sg.Text('Database Name:')],
         [sg.InputText(key='dbname')],
         [sg.Text('Cost:'), sg.Text(' '*20), sg.Text('Due Date:')],
         [sg.InputText(key='cost', size=(10,1)), sg.Text(' ' * 10), sg.InputText(key='duedate', size=(10,1))],
         [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]]
        window = sg.Window('', layout=layout)
        event, values = window.read()
        window.close()
        if event in (None, 'Cancel'):
            return None, None, None, None, None

        jiraname = values['jiraname'].strip().upper()
        if '/' in jiraname:
            jiraname = jiraname.split('/')[-1]
        dbname = values['dbname'].strip().lower()
        cost = values['cost'].strip()
        duedate = values['duedate'].strip()
        worktype = 'First Import'
        if values['second']:
            worktype = 'Second Import'
        elif values['fix']:
            worktype = 'Fix Import'

        # jiraname and dbname can not be blank
        if dbname == '' or jiraname == '':
            sg.Popup('Jira Name or Database Name can not be blank!')
            self.input_workinfo(workpath)
            return None, None, None, None, None

        if re.match('[^0-9a-z]', dbname):
            sg.Popup('Database Name only can be 0-9a-z')
            self.input_workinfo(workpath)
            return None, None, None, None, None

        return jiraname, dbname, worktype, cost, duedate

    def set_shortcut(self, jirapath, desktop_path, jiraname):
        filename = jirapath.strip('\\')
        lnkname = desktop_path + jiraname + r".lnk"
        shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
        shortcut.SetPath(filename)
        if os.path.splitext(lnkname)[-1] != '.lnk':
            lnkname += ".lnk"
        shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)


if __name__ == '__main__':
    run = NewWork()
    run.main()
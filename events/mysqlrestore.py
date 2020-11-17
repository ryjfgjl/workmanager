
"""
Restore mysql database
"""
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
from events.mysqldump import MysqlDump
import PySimpleGUI as sg
import os
import gzip
import shutil
import pyperclip


class MysqlRestore:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.MysqlDump = MysqlDump()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()

    def main(self, currentwork, advanced=1):
        jirapath = self.HandleConfig.handle_config('g', currentwork, 'jirapath')
        dbname = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        git_repo_path = self.HandleConfig.handle_config('g', 'defaultpath', 'git_repo_path')
        merge = self.HandleConfig.handle_config('g', currentwork, 'merge')
        navicat_script_path = self.HandleConfig.handle_config('g', 'defaultpath', 'navicat_script_path')

        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'
        gittemplatepath = git_repo_path + 'templates\\'
        scriptspath = jirapath + 'script\\'
        scripts_bak_path = jirapath + 'db_backup\\'
        tmpscript = scriptspath + 'tmp.txt'
        script = navicat_script_path + dbname + '\\{}.sql'.format(dbname)
        backupsql = scriptspath + '{0}_after.sql'.format(dbname)
        excel_sql_file = scriptspath + '{0}.sql'.format(dbname)

        # truncate tmp.txt first
        with open(tmpscript, 'w', encoding='utf8') as (fw):
            fw.truncate()

        files = []
        drop = 1
        backup_files = [backupsql]
        msg = ''

        if not advanced:
            # restore database in config
            backupgz = scripts_bak_path + '{}_backup.sql.gz'.format(dbname)
            backupsql = scripts_bak_path + '{0}_backup.sql'.format(dbname)
            with gzip.open(backupgz, 'rb') as (f_in):
                with open(backupsql, 'wb') as (f_out):
                    shutil.copyfileobj(f_in, f_out)
            backup_files = [backupsql, scriptspath + '{0}.sql'.format(dbname)]
            files = [
                scriptspath + 'configration.sql',
                gitscriptpath + 'functionAndProcedure.sql',
                gitscriptpath + 'smokeTestV2.sql'
            ]

        elif advanced == 1:
            # restore database
            msg = 'Restore Database Complete!'
            layout = [
                [sg.Button('RestoreToLocalHost')],
                [sg.Button('RestoreToAWSHotfix')]
            ]

            window = sg.Window(title=currentwork, layout=layout)
            event, values = window.read()
            window.close()

            if event is None:
                return

            elif event == 'RestoreToLocalHost':
                pass

            elif event == 'RestoreToAWSHotfix':
                self.MysqlDump.main(currentwork, gz=True)
                winscppath = self.HandleConfig.handle_config('g', 'defaultpath', 'winscppath')
                db_backup = self.HandleConfig.handle_config('g', currentwork,'jirapath') + 'db_backup\\{0}.sql.gz'.format(dbname)
                cmd = '{0}WinSCP.com /command "open aws188" "put {1} /home/neon/leiwu/dataimport/fulldata/" "exit"'.format(winscppath, db_backup)
                os.system(cmd)
                sg.popup('Restore To AWS Hotfix Complete')
                return

        elif advanced == 2:
            # restore database in run script
            msg = 'Runscript Database Complete!'

            layout = [

                 [sg.Checkbox('AllScriptWithoutSmokeTest', key='AllScriptWithoutSmokeTest')],

                 [sg.Checkbox('ExcelSqlFile', key=excel_sql_file)],
                 [sg.Checkbox('TemplateScript', key=script)],
                 [sg.Checkbox('TemplateSmokeTest', key='TemplateSmokeTest')],
                 [sg.Checkbox('TemplateScriptAfter', key=navicat_script_path + dbname + '\\{}_after_template.sql'.format(dbname))],
                 [sg.Checkbox('AccountMerge', key=gitscriptpath + 'accountMerge.sql')],
                 [sg.Checkbox('AccountMergeAfter', key=navicat_script_path + dbname + '\\{}_after_merge.sql'.format(dbname))],
                 [sg.Checkbox('dataClean', key=gitscriptpath + 'fullDataClean.sql')],
                 [sg.Checkbox('SmokeTest', key=gitscriptpath + 'smokeTestV2.sql')],

                 [sg.Checkbox('All Script and Restore To AWS Hotfix'.format(dbname), key='AllScript', default=True,text_color='blue')],
                 [sg.Checkbox('Drop database if exists {}'.format(dbname), key='drop', default=True, text_color='blue')],

                 [sg.Submit(), sg.Cancel()]
            ]
            window = sg.Window(title=currentwork, layout=layout)
            event, values = window.read()
            window.close()

            if event in (None, 'Cancel'):
                return

            
            if values['drop']:
                drop = 1
            else:
                drop = 0
                backup_files = []

            if values['AllScript'] or values['AllScriptWithoutSmokeTest']:
                files = [
                     script,
                     navicat_script_path + dbname + '\\{}_after_template.sql'.format(dbname),
                     gitscriptpath + 'accountMerge.sql',
                     navicat_script_path + dbname + '\\{}_after_merge.sql'.format(dbname),
                     gitscriptpath + 'fullDataClean.sql',
                     gitscriptpath + 'smokeTestV2.sql',
                     gitscriptpath + 'clear.sql'
                ]
                if merge == 'False':
                    files.remove(gitscriptpath + 'accountMerge.sql')
                if values['AllScriptWithoutSmokeTest']:
                    files.remove(gitscriptpath + 'smokeTestV2.sql')


            else:
                backup_files = []
                for k, v in values.items():
                    if v:
                        if k == 'TemplateSmokeTest':
                            files = files + [gittemplatepath+'template_smoke_test\\smoke_test_for_account.sql',
                            gittemplatepath+'template_smoke_test\\smoke_test_for_custom_field.sql',
                            gittemplatepath+'template_smoke_test\\smoke_test_for_gais.sql',
                            gittemplatepath+'template_smoke_test\\smoke_test_for_transaction.sql']
                        elif k == 'drop':
                            continue
                        else:
                            files.append(k)

        sqlfiles = backup_files
        if len(files) > 0:
            for f in files:
                with open(f, 'r', encoding='utf8') as (fa):
                    with open(tmpscript, 'a+', encoding='utf8') as (fw):
                        fw.writelines(['\n'])
                        shutil.copyfileobj(fa, fw)
            sqlfiles = sqlfiles + [tmpscript]
            #sqlfiles = sqlfiles + files


        if drop:
            sql = 'drop database if exists `{}`;\ncreate database `{}`;'.format(dbname, dbname)
            self.ConnDB.exec(self.conn, sql)
            print('\n\n{}'.format(sql))

        for sqlfile in sqlfiles:
            if not os.path.exists(sqlfile):
                continue
            ret = self.ConnDB.cmd(dbname, 'mysql', sqlfile)
            if ret == 0:
                continue
            else:
                sg.popup_error('Error!')
                return 0

        if advanced == 2 and values['AllScript']:
            conn = self.ConnDB.conndb(dbname)
            sql = 'SELECT * FROM smoke;'
            ret = self.ConnDB.exec(conn, sql)
            result = ret.fetchall()
            if len(result) > 0:
                layout = [[sg.Text('Somke Test Result is not empty! Check it first!\n\n Press OK to continue to dump database and upload to winscp.')],
                    [sg.OK(),sg.Cancel(), sg.Button('Check Out')]
                ]
                window = sg.Window(title=currentwork, layout=layout)
                event, values = window.read()
                window.close()

                if event in ('Cancel', None):
                    return

                if event == 'Check Out':
                    layout = [
                    [sg.Table(result,
                        ['errorMsg', 'Error Count After', 'Error Count Pre', 'Pass Flag'], col_widths=[100,15,15,15], auto_size_columns=False, justification="left")
                    ],
                        [sg.Text('Press OK to continue to dump database and upload to winscp.')],
                        [sg.OK(),sg.Cancel()]
                    ]
                    window1 = sg.Window(title=currentwork, layout=layout)
                    event1, values = window1.read()
                    window1.close()
                    if event1 in ('Cancel', None):
                        return
            self.MysqlDump.main(currentwork, gz=True)
            winscppath = self.HandleConfig.handle_config('g', 'defaultpath', 'winscppath')
            db_backup = self.HandleConfig.handle_config('g', currentwork, 'jirapath') + 'db_backup\\{0}.sql.gz'.format(dbname)
            cmd = '{0}WinSCP.com /command "open aws188" "put {1} /home/neon/leiwu/dataimport/fulldata/" "exit"'.format(winscppath, db_backup)
            os.system(cmd)
        elif advanced == 2 and values['TemplateSmokeTest']:
            conn = self.ConnDB.conndb(dbname)
            sql = 'SELECT templateTableName, errorMsg, errorCount, passFlag FROM smoke_test_report_for_template WHERE passFlag<>"Pass" ORDER BY passFlag;'
            ret = self.ConnDB.exec(conn, sql)
            result = ret.fetchall()
            if len(result) > 0:
                layout = [
                [sg.Table(result,
                    ['templateTableName', 'errorMsg', 'Error Count', 'Pass Flag'], col_widths=[30,100,15,15], auto_size_columns=False, justification="left")
                ],
                    [sg.Text('SELECT * FROM smoke_test_report_for_template WHERE passFlag<>"Pass" ORDER BY passFlag;'), sg.Button('Copy')]
                ]
                window1 = sg.Window(title=currentwork, layout=layout)
                event1, values1 = window1.read()
                window1.close()
                if event1 is None:
                    return
                if event1 == 'Copy':
                    pyperclip.copy('SELECT * FROM smoke_test_report_for_template WHERE passFlag<>"Pass" ORDER BY passFlag;')
        elif advanced == 2 and values[gitscriptpath + 'smokeTestV2.sql']:
            conn = self.ConnDB.conndb(dbname)
            sql = 'SELECT * FROM smoke;'
            ret = self.ConnDB.exec(conn, sql)
            result = ret.fetchall()
            if len(result) > 0:
                layout = [
                    [sg.Table(result,
                              ['errorMsg', 'Error Count After', 'Error Count Pre', 'Pass Flag'],
                              col_widths=[100, 15, 15, 15], auto_size_columns=False, justification="left")
                     ],
                ]
                window1 = sg.Window(title=currentwork, layout=layout)
                event1, values = window1.read()
                window1.close()

        if advanced:
            sg.Popup(msg, title=currentwork)


if '__name__' == '__main__':
    MysqlRestore = MysqlRestore()
    MysqlRestore.main('')
"""
A work manager

authorL zxb
date:2020-05-19
"""

Version = '1.0.1'

# -------------------------- Program Interface -------------------------- #

import PySimpleGUI as sg
from common.handleconfig import HandleConfig
import traceback
import sys

HandleConfig = HandleConfig()
sg.ChangeLookAndFeel('GreenTan')

def exception_format():
    """
    Convert exception info into a string suitable for display.
    """
    return "".join(traceback.format_exception(
        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    ))


while True:
    try:
        currentwork = HandleConfig.handle_config("g", "global", "currentwork")

        menu_def = [['&Setting', ['&Edit Config', '&Load Config', '&Check Update']]]
        layout = [
            [sg.Menu(menu_def, tearoff=True)],
            [sg.Text('{0}Curent Work: {1}'.format(' '*50,currentwork), text_color='blue', font=15)],
            [sg.Text(' ' * 160)],
            [sg.Button(button_text='New Work', size=(15, 3)),
             sg.Button(button_text='Import Excel', size=(15, 3), ), sg.Text(' ' * 40),
             ],

            [sg.Button(button_text='Dump Mysql', size=(15, 3)),
             sg.Button(button_text='Restore Mysql', size=(15, 3)), sg.Text(' ' * 20),
             sg.Button(button_text='Delete Work', size=(15, 3)),
             sg.Button(button_text='db_to_download', size=(15, 3))],

            [sg.Button(button_text='Configure Script', size=(15, 3)),
             sg.Button(button_text='Run Script', size=(15, 3)), sg.Text(' ' * 20),
             sg.Button(button_text='Refresh Git', size=(15, 3)), sg.Button(button_text='Generate Command', size=(15, 3))],
            [sg.Text('-' * 160)],
            [
             sg.Button(button_text='Change Work', size=(15, 5)), sg.Text(' ' * 90),
             sg.Button(button_text='Quit', size=(10, 5))],

        ]
        window = sg.Window('Work Manger {0}'.format(Version),
                           layout,
                           location=(1000, 100)
                           )
        event, values = window.read()

        if event in (None, 'Quit'):
            break

        if event == 'New Work':
            from events.newwork import NewWork
            NewWork = NewWork()
            NewWork.main()
        elif event == 'Import Excel':
            from events.excelimporter import ImportExcel
            ImportExcel = ImportExcel()
            ImportExcel.main(currentwork)
        elif event == 'Dump Mysql':
            from events.mysqldump import MysqlDump
            MysqlDump = MysqlDump()
            MysqlDump.main(currentwork)
        elif event == 'Restore Mysql':
            from events.mysqlrestore import MysqlRestore
            MysqlRestore = MysqlRestore()
            MysqlRestore.main(currentwork)
        elif event == 'Configure Script':
            from events.configurescript import ConfigScript
            ConfigScript = ConfigScript()
            ConfigScript.main(currentwork)
        elif event == 'Run Script':
            from events.runscript import RunScript
            RunScript = RunScript()
            RunScript.main(currentwork)
        elif event == 'db_to_download':
            from events.dbtodownload import DbToDownload
            DbToDownload = DbToDownload()
            DbToDownload.main(currentwork)
        elif event == 'Change Work':
            from events.changework import ChangeWork
            ChangeWork = ChangeWork()
            ChangeWork.main()
        elif event == 'Delete Work':
            from events.deletework import DeleteWork
            DeleteWork = DeleteWork()
            DeleteWork.main(currentwork)
        elif event == 'Refresh Git':
            from events.refreshgit import RefreshGit
            RefreshGit = RefreshGit()
            RefreshGit.main()
        elif event == 'Generate Command':
            from events.generatecmd import GenerateCMD
            GenerateCMD = GenerateCMD()
            GenerateCMD.main(currentwork)
        elif event == 'Edit Config':
            from events.config import Config
            Config = Config()
            Config.edit_config()
        elif event == 'Load Config':
            from events.config import Config
            Config = Config()
            Config.load_config()
        elif event == 'Check Update':
            from events.checkupdate import CheckUpdate
            CheckUpdate = CheckUpdate()
            CheckUpdate.main(Version)

    except:
        sg.PopupError(exception_format())

    finally:
        window.close()



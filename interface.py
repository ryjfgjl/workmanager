"""
A work manager

authorL zxb
date:2020-05-19
"""

Version = '2.1'

import PySimpleGUI as sg
from common.handleconfig import HandleConfig
import traceback, sys, os
import re

HandleConfig = HandleConfig()
sg.ChangeLookAndFeel('GreenTan')


def exception_format():
    """
    Convert exception info into a string suitable for display.
    """
    return "".join(traceback.format_exception(
        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    ))

def generate_layout():
    # get the work that the program is working on
    works = [work for work in HandleConfig.handle_config()['worklist'].values()]

    # the setting of tool
    # addvanced options
    menu_def = [
                ['&File', ['&Open Work Dir', '&Open Git Dir', '&Open tmp.txt']],
                ['&Setting', ['&Edit Config', '&Load Config']],
                ['&Tools', ['&Clean Sql', '&Custom Field']],
                ['&Advanced', ['&Import Specific Excel','&Add Comment']],
                ]

    # the templete layout
    tab_layouts = []
    for work in works:
        try:
            dbname = HandleConfig.handle_config("g", work, "dbname")
        except:
            dbname = ''
        tab_layout = [
            #[sg.Text('',size=(12,1))],
            [
             sg.B(button_text='Import Excel', size=(15, 3), ),
             sg.B(button_text='Config Import', size=(15, 3)),
             sg.B(button_text='Restore Database', size=(15, 3)),
             sg.B(button_text='Run Script', size=(15, 3)),
             sg.B(button_text='Complete', size=(15, 3)),

             ],
            [sg.B(button_text='DB To Download', size=(15, 3)),
             sg.B(button_text='AWS Command List', size=(15, 3))],
            [
                sg.Frame('Work Information',
                         [
                             [sg.Text('Database: '), sg.Input('{}'.format(dbname), disabled=True)],
                             [sg.Text('Jira url: '), sg.Input('https://neoncrm.atlassian.net/browse/{}'.format(work), disabled=True)],
                             [sg.Text('Test url: '), sg.Input('https://neonuat.com:8443/np/clients/{}_test/login.jsp'.format(dbname), disabled=True, size=(80, 1))],
                         ], size=(1000, 5000))
            ]
        ]
        tab_layouts.append(sg.Tab(work, tab_layout))

    layout = [

        [sg.Menu(menu_def)],
        [sg.Button('New Work'), sg.Button('Git Pull'), sg.Text(' '*118), sg.Button('{}'.format(HandleConfig.handle_config('g', 'global', 'server')))],
        [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
    ]
    return layout


window = sg.Window('Work Manager {0}'.format(Version), generate_layout(), location=(700, 100))
window.Finalize()
currentwork = HandleConfig.handle_config('g','global','currentwork')
if currentwork:
    window[currentwork].Select()

# A loop program until press X
while True:
    #currentwork = None
    try:

        event, values = window.read()

        # when press X, quit the program
        if event is None:
            break
        elif event != 'cd188':
            event = re.sub(r'\d+$', '', event)
            currentwork = [value for value in values.values()][-1]

        if event == 'New Work':
            from events.newwork import NewWork
            NewWork = NewWork()
            ret = 1
            try:
                ret = NewWork.main()
            except:
                raise
            finally:
                if ret != 0:
                    window.close()
                    window = sg.Window('Work Manager {0}'.format(Version), generate_layout(), location=(700, 100))
                    window.Finalize()
                    currentwork = HandleConfig.handle_config('g', 'global', 'currentwork')
                    window[currentwork].Select()

        elif event == 'Import Excel':
            os.system('cls')
            print('{:-^60}'.format(event))
            from events.excelimporter import ImportExcel
            ImportExcel = ImportExcel()
            ImportExcel.main(currentwork)
        elif event == 'Import Specific Excel':
            os.system('cls')
            print('{:-^60}'.format(event))
            from events.excelimporter import ImportExcel
            ImportExcel = ImportExcel()
            ImportExcel.main(currentwork, advanced=1)
        elif event == 'Config Import':
            os.system('cls')
            print('{:-^60}'.format(event))
            from events.configurescript import ConfigScript
            ConfigScript = ConfigScript()
            ConfigScript.main(currentwork)
        elif event == 'Restore Database':
            os.system('cls')
            print('{:-^60}'.format(event))
            from events.mysqlrestore import MysqlRestore
            MysqlRestore = MysqlRestore()
            MysqlRestore.main(currentwork)
        elif event == 'Run Script':
            os.system('cls')
            print('{:-^60}'.format(event))
            from events.runscript import RunScript
            RunScript = RunScript()
            RunScript.main(currentwork)
        elif event == 'DB To Download':
            from events.dbtodownload import DbToDownload
            DbToDownload = DbToDownload()
            DbToDownload.main(currentwork)
        elif event == 'Complete':
            os.system('cls')
            print('{:-^60}'.format(event))
            from events.deletework import DeleteWork
            DeleteWork = DeleteWork()
            ret = 1
            try:
                ret = DeleteWork.main(currentwork)
            except:
                raise
            finally:
                if ret != 0:
                    window.close()
                    window = sg.Window('Work Manager {0}'.format(Version), generate_layout(), location=(700, 100))
                    window.Finalize()
                    currentwork = HandleConfig.handle_config('g', 'global', 'currentwork')
                    window[currentwork].Select()

        elif event == 'AWS Command List':
            from events.generatecmd import GenerateCMD
            GenerateCMD = GenerateCMD()
            GenerateCMD.main(currentwork)

        elif event == 'Git Pull':
            from tools.refreshgit import RefreshGit
            RefreshGit = RefreshGit()
            RefreshGit.main()

        # Tools    
        elif event == 'Clean Sql':
            from tools.cleansql import CleanSql
            CleanSql = CleanSql()
            CleanSql.main()
        elif event == 'Custom Field':
            from tools.customfield import CustomField
            CustomField = CustomField()
            CustomField.main()
        elif event == 'Add Comment':
            from tools.addcomment import AddComment
            AddComment = AddComment()
            AddComment.main(currentwork)

        # Setting        
        elif event == 'Edit Config':
            from events.setting import Setting
            Setting = Setting()
            Setting.edit_config()
        elif event == 'Load Config':
            from events.setting import Setting
            Setting = Setting()
            Setting.load_config()
        elif event in ('cd188', 'localhost'):
            from events.setting import Setting
            Setting = Setting()
            Setting.swich_server(event)
            currentwork = window['tabgroup'].get()
            window.close()
            window = sg.Window('Work Manager {0}'.format(Version), generate_layout(), location=(700, 100))
            window.Finalize()
            if currentwork:
                window[currentwork].Select()

        # File
        elif event == 'Open Work Dir':
            from events.file import File
            File = File()
            File.open_work_dir(currentwork)
        elif event == 'Open Git Dir':
            from events.file import File
            File = File()
            File.open_git_dir()
        elif event == 'Open tmp.txt':
            from events.file import File
            File = File()
            File.open_tmp(currentwork)

    except:
        # display the any program error
        sg.PopupError(exception_format(), title=currentwork)
    finally:
        if currentwork:
            HandleConfig.handle_config('s', 'global', 'currentwork', currentwork)




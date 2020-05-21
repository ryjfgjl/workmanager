"""
A work manager

authorL zxb
date:2020-05-19
"""

Version = 1.0

# -------------------------- Program Interface -------------------------- #

import PySimpleGUI as sg
from common.handleconfig import HandleConfig

HandleConfig = HandleConfig()
sg.ChangeLookAndFeel('GreenTan')

while True:

    currentwork = HandleConfig.handle_config("g", "global", "currentwork")
    layout = [
        [sg.Text('{0}Curent Work: {1}'.format(' '*50,currentwork), text_color='blue', font=15)],
        [sg.Text(' ' * 160)],
        [sg.Button(button_text='New Work', size=(15, 3)),
         sg.Button(button_text='Import Excel', size=(15, 3), ), sg.Text(' ' * 40),
         ],

        [sg.Button(button_text='Dump Mysql', size=(15, 3)),
         sg.Button(button_text='Restore Mysql', size=(15, 3)), sg.Text(' ' * 20),
         sg.Button(button_text='Delete Work', size=(15, 3)),
         sg.Button(button_text='Add Comment', size=(15, 3), disabled=True)],

        [sg.Button(button_text='Configure Script', size=(15, 3)),
         sg.Button(button_text='Run Script', size=(15, 3)), sg.Text(' ' * 20),
         sg.Button(button_text='Refresh Git', size=(15, 3)), sg.Button(button_text='Parse Name', size=(15, 3), disabled=True)],
        [sg.Text('-' * 160)],
        [
         sg.Button(button_text='Change Work', size=(15, 5)), sg.Text(' ' * 90),
         sg.Button(button_text='Quit', size=(10, 5))],

    ]
    window = sg.Window('Work Manger {0}'.format(Version),
                       layout,
                       location=(2500, 100)
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
        from events.configurescript import ConfigureScript
        ConfigureScript = ConfigureScript()
        ConfigureScript.main(currentwork)
    elif event == 'Run Script':
        from events.runscript import RunScript
        RunScript = RunScript()
        RunScript.main(currentwork)
    elif event == 'Add Comment':
        pass
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
    elif event == 'Parse Name':
        pass

    window.close()
"""except:
    sg.Popup("Program Error")
    break"""


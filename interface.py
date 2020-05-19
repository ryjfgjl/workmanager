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
        [sg.Text('{0}Curent Work: {1}'.format(' '*50,currentwork))],
        [sg.Text(' ' * 160)],
        [sg.Button(button_text='New Work', size=(15, 3)),
         sg.Button(button_text='Import Excel', size=(15, 3), ), sg.Text(' ' * 40),
         sg.Button(button_text='Change Work', size=(15, 3))],

        [sg.Button(button_text='Dump Mysql', size=(15, 3)),
         sg.Button(button_text='Restore Mysql', size=(15, 3)), sg.Text(' ' * 20),
         sg.Button(button_text='Delete Work', size=(15, 3)), sg.Button(button_text='Add Work', size=(15, 3))],

        [sg.Button(button_text='Configure Script', size=(15, 3)),
         sg.Button(button_text='Run Script', size=(15, 3))],
        [sg.Text('-' * 160)],
        [sg.Button(button_text='Add Comment', size=(30, 3)), sg.Text(' ' * 70),
         sg.Button(button_text='Quit', size=(10, 5))],

    ]
    window = sg.Window('Work Manger {0}'.format(Version),
                       layout,
                       location=(2500, 100),
                       )
    event, values = window.read()
    if event in (None, 'Quit'):
        break

    if event == 'New Work':
        from events.newwork import NewWork
        NewWork = NewWork()
        NewWork.main()

    elif event == 'Import Excel':
        pass
    elif event == 'Dump Mysql':
        pass
    elif event == 'Restore Mysql':
        pass
    elif event == 'Configure Script':
        pass
    elif event == 'Run Script':
        pass
    elif event == 'Add Comment':
        pass
    elif event == 'Change Work':
        pass
    elif event == 'Delete Work':
        pass
    elif event == 'Add Work':
        pass
    window.close()
"""except:
    sg.Popup("Program Error")
    break"""


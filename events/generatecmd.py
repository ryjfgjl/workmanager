
from common.handleconfig import HandleConfig
import PySimpleGUI as sg
from common.conndb import ConnDB
import pyperclip

sg.ChangeLookAndFeel('GreenTan')

class GenerateCMD:

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def main(self, currentwork):
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")

        k0 = 'dbdump'
        k1 = 'dbrestore'
        k2 = 'dataImportRestore'
        k3 = 'dataImportRunScrip'
        k4 = 'dbremove'

        db0 = '{}_bak'.format(dbname)
        db1 = '{}_test'.format(dbname)
        db2 = '{}_test1'.format(dbname)
        db3 = '{}_test2'.format(dbname)

        layout = [
                 [sg.Radio(k0, 'R0', default=True, key=k0), sg.Text('                     New Database:')],
                 [sg.Radio(k1, 'R0', key=k1), sg.Text('               '), sg.Combo([db0, db1, db2, db3], key='db_new', size=(20,5))],
                 [sg.Radio(k2, 'R0', key=k2)],
                 [sg.Radio(k3, 'R0', key=k3)],
                 [sg.Radio(k4, 'R0', key=k4)],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]

        ]

        window = sg.Window('', layout=layout, )
        event, values = window.read()
        window.close()

        if event in (None, 'Cancel'):
            return None, None, None, None

        command = None
        if values[k0]:
            command = k0
        elif values[k1]:
            command = k1
        elif values[k2]:
            command = k2
        elif values[k3]:
            command = k3
        elif values[k4]:
            command = k4

        cmd = '/home/neon/leiwu/bin/' + command + '.sh ' + dbname + ' ' + values['db_new']
        if values[k3]:
            cmd = '/home/neon/leiwu/bin/' + command + '.sh ' + values['db_new'] + ' ' + dbname
        sg.Popup(cmd.strip())
        pyperclip.copy(cmd.strip())









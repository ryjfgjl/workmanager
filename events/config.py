
import os
import sys, shutil
import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')


class Config:

    def __init__(self):
        self.realpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.configini = self.realpath + r"\config.ini"

    def edit_config(self):
        os.popen(self.configini)

    def load_config(self):
        layout = [
            [sg.InputText('', key='e'), sg.FileBrowse()],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]

        ]
        window = sg.Window('', layout=layout, )
        event, values = window.read()
        window.close()
        if event in (None, 'Cancel'):
            return
        existconfig = values['e']
        if not existconfig:
            return
        shutil.copyfile(existconfig, self.configini)







import os, sys, shutil, PySimpleGUI as sg
from common.handleconfig import HandleConfig


class Setting:

    def __init__(self):
        self.realpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.configini = self.realpath + '\\config.ini'
        self.HandleConfig = HandleConfig()

    def edit_config(self):
        os.popen(self.configini)

    def load_config(self):
        layout = [
         [
          sg.InputText('', key='e'), sg.FileBrowse()],
         [
          sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]]
        window = sg.Window(title='', layout=layout)
        event, values = window.read()
        window.close()
        if event in (None, 'Cancel'):
            return
        existconfig = values['e']
        shutil.copyfile(existconfig, self.configini)

    def swich_server(self, event):
        current_server = event
        if current_server == 'localhost':
            new_server = 'cd188'
        else:
            new_server = 'localhost'
        self.HandleConfig.handle_config('s', 'global', 'server', new_server)
        navicat_script_path = self.HandleConfig.handle_config('g', new_server, 'navicat_script_path')
        self.HandleConfig.handle_config('s', 'defaultpath', 'navicat_script_path', navicat_script_path)


if '__name__' == '__main__':
    Setting = Setting()
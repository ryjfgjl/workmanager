"""
Transform work
"""

from common.handleconfig import HandleConfig
import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')

class ChangeWork:

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def main(self):
        works = [work for work in self.HandleConfig.handle_config()["worklist"].values()]

        layout = [
            [sg.Text("work list")],
            [sg.Listbox(works, key='l', size=(40,5))],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]
        ]
        window = sg.Window('', layout)
        event, values = window.read()
        window.close()

        if event in (None, 'Cancel'):
            return
        if values['l']:
            currentwork = values['l'][0]
            self.HandleConfig.handle_config("s", "global", "currentwork", currentwork)



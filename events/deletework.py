
from common.handleconfig import HandleConfig
import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')

class DeleteWork:

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def main(self, currentwork):
        works = [work for work in self.HandleConfig.handle_config()["worklist"].values()]

        layout = [
            [sg.Text("work list")],
            [sg.Listbox(works, key='l', size=(40,5), select_mode='multiple')],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]
        ]
        window = sg.Window('', layout)
        event, values = window.read()
        window.close()

        if event in (None, 'Cancel'):
            return
        works = values['l']
        if works:
            for work in works:
                self.HandleConfig.handle_config("rs", self.HandleConfig.handle_config("g", "worklist", work))
                self.HandleConfig.handle_config("ro", "worklist", key=work)
            if currentwork in works:
                works = [work for work in self.HandleConfig.handle_config()["worklist"].values()]
                currentwork = 'None'
                if works:
                    currentwork = works[0]
                self.HandleConfig.handle_config("s", "global", "currentwork", currentwork)

            sg.Popup("Delete Over!")



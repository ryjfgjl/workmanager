"""
Add comment
"""

from common.handleconfig import HandleConfig
import PySimpleGUI as sg
import pyperclip


class AddComment:

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def main(self, currentwork):
        worktype = self.HandleConfig.handle_config('g', currentwork, 'worktype')
        database = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        jiradb = self.HandleConfig.handle_config('g', currentwork, 'jiraname')

        with open(r'reference_files\persons.txt', "r") as f:
            personlist = f.readlines()

        layout = [
            [sg.Text('Role:')],
            [sg.Radio('Importer', 'R0', key='I', default=True), sg.Radio('Tester on aws', 'R0', key='T0'), sg.Radio('Tester on production', 'R0', key='T1')],
            [sg.Text('Person:')],
            [sg.Combo(personlist, key='P', default_value='Jia Yang')],
            [sg.Submit(), sg.Cancel()]
        ]
        window = sg.Window(title=currentwork, layout=layout)
        event, values = window.read()
        window.close()
        if event in (None, 'Cancel'):
            return

        if values['I']:
            role = "Importer"
        elif values['T0']:
            role = "Tester on aws"
        elif values['T1']:
            role = "Tester on production"
        person = values['P'].strip()

        if role == "Importer":

            if person == "Kun Li":
                comment = 'Hi Kun Li,\n\n' \
                          'The attached file [^{0}.zip] contains all the scripts for this {1}.\n' \
                          'You can apply the scripts to /{2}/.\nData Import Tag: general.\n\n' \
                          'Thanks.\nXiaobo'.format(jiradb, worktype, database)
            else:
                comment = "Hi {0},\n\n" \
                		  "Can you please test this {1}?" \
                          "\nhttps://neonuat.com:8443/np/clients/{2}/login.jsp\n\nThanks.\nXiaobo".format(person,
                                                                                                            worktype,
                                                                                                            database)

        elif role == "Tester on aws":
            comment = "Hi {0},\n\nAll of the issues have been fixed and test passed" \
                          "\nPlease upload the scripts.".format(person)
        else:
            comment = "Test passed on production!"

        pyperclip.copy(comment)


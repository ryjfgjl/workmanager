"""
create dictionary when get a work use jira name and database name
"""

from datetime import date
import os
from common.handleconfig import HandleConfig
import shutil
import PySimpleGUI as sg


sg.ChangeLookAndFeel('GreenTan')


class NewWork:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.image = self.HandleConfig.handle_config("g", "referencefile", "img")

    def main(self):
        jiraname, dbname, worktype = self.input_workinfo()
        if not jiraname:
            return
        workpath = self.HandleConfig.handle_config("g", "global", "workpath")
        year = str(date.today().year)
        month = str(date.today().month)
        yearpath = workpath + year + "\\"
        monthpath = yearpath + month + "\\"
        worktypepath = monthpath + worktype.replace(' ', '_') + "\\"
        jirapath = worktypepath + jiraname + "\\"

        if not os.path.exists(yearpath):
            os.makedirs(yearpath)
        if not os.path.exists(monthpath):
            os.makedirs(monthpath)
        if not os.path.exists(worktypepath):
            os.makedirs(worktypepath)
        if not os.path.exists(jirapath):
            os.makedirs(jirapath)

        questionpath = jirapath + "questions\\"
        scriptspath = jirapath + "scripts\\"
        scriptsbakpath = jirapath + "scripts_bak\\"
        xlspath = jirapath + "xls\\"
        if not os.path.exists(questionpath):
            os.makedirs(questionpath)
        if not os.path.exists(scriptspath):
            os.makedirs(scriptspath)
        if not os.path.exists(scriptsbakpath):
            os.makedirs(scriptsbakpath)
        if not os.path.exists(xlspath):
            os.makedirs(xlspath)

        script = scriptspath + r"\\{}.txt".format(jiraname.replace('-', '_').lower())
        if not os.path.isfile(script):  # only check file not file dictionary
            shutil.copyfile(self.HandleConfig.handle_config("g", "referencefile", "emptytxt"), script)
        importexcelpath = xlspath + "importexcels\\"
        if not os.path.exists(importexcelpath):
            os.makedirs(importexcelpath)

        self.HandleConfig.handle_config("a", jiraname)
        self.HandleConfig.handle_config("s", jiraname, "dbname", dbname)
        self.HandleConfig.handle_config("s", jiraname, "jiraname", jiraname)
        self.HandleConfig.handle_config("s", jiraname, "jirapath", jirapath)
        self.HandleConfig.handle_config("s", jiraname, "worktype", worktype)
        self.HandleConfig.handle_config("s", jiraname, "importexcelpath", importexcelpath)
        self.HandleConfig.handle_config("s", "worklist", jiraname, jiraname)

        sg.Popup('Complete!')


    def input_workinfo(self):

        layout = [
            [sg.Text('Jira Name:')],
            [sg.InputText(key='jiraname')],
            [sg.Text('Database Name:')],
            [sg.InputText(key='dbname')],
            [sg.Frame(layout=[
                [sg.Radio('First Import', 'R0', default=True, key='first'), sg.Radio('Second Import', 'R0', key='second'),
                 sg.Radio('Fix Import', 'R0', key='fix'), ]
            ], title='Work Type', title_color='red')],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]

        ]
        window = sg.Window('',layout=layout,)
        event, values = window.read()
        window.close()

        if event in (None, 'Cancel'):
            return None, None, None
        jiraname = values['jiraname'].strip().upper()
        dbname = values['dbname'].strip().lower()
        if values['first']:
            worktype = 'First Import'
        elif values['second']:
            worktype = 'Second Import'
        else:
            worktype = 'Fix Import'

        if jiraname == '' or dbname == '':
            sg.Popup('Jira Name or Database Name can not be blank!')
            self.input_workinfo()
            return None, None, None

        return jiraname, dbname, worktype

if __name__ == "__main__":
    run = NewWork()
    run.main()
"""
create dictionary when get a work use jira name and database name
"""

from datetime import date
import os, re
from common.handleconfig import HandleConfig
import shutil
import PySimpleGUI as sg


sg.ChangeLookAndFeel('GreenTan')


class NewWork:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.image = self.HandleConfig.handle_config("g", "referencefile", "img")

    def main(self):
        workpath = self.HandleConfig.handle_config("g", "global", "workpath")
        jiraname, dbname, worktype, existwork = self.input_workinfo(workpath)
        if not dbname:
            return
        if existwork:
            jirapath = existwork.replace('/','\\') + '\\'
            importexcelpath = jirapath + "\\xls\\importexcels\\"
            pattern = re.compile(r"^.*?\\(\d{4})\\(\d{1,2})\\(.*?)\\(.*?)\\$", re.S)
            match = re.match(pattern, jirapath)
            if match:
                worktype = match.group(3).replace('_',' ')
                jiraname = match.group(4)
                scriptspath = jirapath + 'scripts\\'
            else:
                sg.Popup('Error')
                return


        else:
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


    def input_workinfo(self, workpath):

        year = str(date.today().year)
        workpath = workpath + year + "\\"

        layout = [
            [sg.Frame(layout=[
                [sg.Radio('First Import', 'R0', default=True, key='first'),
                 sg.Radio('Second Import', 'R0', key='second'),
                 sg.Radio('Fix Import', 'R0', key='fix')]
            ], title='Work Type', title_color='red')],
            [sg.Text('Jira Name:')],
            [sg.InputText(key='jiraname')],
            [sg.Text('Database Name:')],
            [sg.InputText(key='dbname')],

            [sg.Text('Work Directionay')],
            [sg.InputText('', key='e'), sg.FolderBrowse(initial_folder=workpath)],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]

        ]
        window = sg.Window('',layout=layout,)
        event, values = window.read()
        window.close()

        if event in (None, 'Cancel'):
            return None, None, None, None
        jiraname = values['jiraname'].strip().upper()
        dbname = values['dbname'].strip().lower()
        worktype = 'First Import'
        if values['second']:
            worktype = 'Second Import'
        elif values['fix']:
            worktype = 'Fix Import'
        existwork = values['e']

        if (existwork != '' and dbname == '') or (existwork == '' and (dbname == '' or jiraname =='')):
            sg.Popup('Jira Name or Database Name or Work Dictionary can not be blank!')
            self.input_workinfo(workpath)
            return None, None, None, None

        return jiraname, dbname, worktype, existwork


if __name__ == "__main__":
    run = NewWork()
    run.main()
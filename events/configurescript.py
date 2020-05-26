from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg
import shutil
from events.mysqlrestore import MysqlRestore

sg.ChangeLookAndFeel('GreenTan')


class ConfigScript:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.MysqlRestore = MysqlRestore()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()

    def main(self, currentwork):
        jirapath = self.HandleConfig.handle_config("g", currentwork, "jirapath")
        jiraname = self.HandleConfig.handle_config("g", currentwork, "jiraname")
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")
        scriptspath = jirapath + "scripts\\"
        git_repo_path = self.HandleConfig.handle_config("g", "defaultpath", "git_repo_path")
        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'
        configration_sql = gitscriptpath + 'configration.sql'
        configration_sql_new = jirapath + 'scripts\\configration.sql'
        shutil.copy(configration_sql, configration_sql_new)

        k0 = 'Wipe Data And Keep Settings'
        k1 = 'Standardize Household Name And Household Salutation'
        k2 = 'Account De-dupe Rule'
        k3 = 'Retain Account Logic in duping'
        k4 = 'De-Dupe address using standard script'
        k5 = 'Merge Duplicate Accounts even if they are in the Same Company'
        k6 = 'Merge Duplicate Accounts even if they are in the Same Household'
        k7 = 'Merge households if one account is head in household, but is non-head in another'
        k8 = 'Merge Duplicate Accounts even if they have relationships to each other'
        k9 = 'Change Drop Down Custom Field To Checkbox If Multiple Options Are Selected'
        k10 = 'Drop down custom fieldId that should not be changed to checkbox'
        k11 = 'Legacy Account Custom Field Name'

        layout = [
            [sg.Text(k0), sg.Combo(['Yes', 'No'], default_value='No', key=k0)],
            [sg.Text(k1), sg.Combo(('Yes', 'No'), default_value='Yes', key=k1)],
            [sg.Text(k2), sg.Combo(('Name + Email/Address Match', 'Name Match', 'Name + Email Match', 'Name + Address Match', 'Do Not De-Dupe'), default_value='Name + Email/Address Match', key=k2)],
            [sg.Text(k3), sg.Combo(('Smallest ID', 'Biggest ID', 'Earliest Create Time', 'Most Recent Create Time', 'Others'), default_value='Smallest ID', key=k3)],
            [sg.Text(k4), sg.Combo(('Yes', 'No'), default_value='Yes', key=k4)],
            [sg.Text(k5), sg.Combo(('Yes', 'No'), default_value='Yes', key=k5)],
            [sg.Text(k6), sg.Combo(('Yes', 'No'), default_value='Yes', key=k6)],
            [sg.Text(k7), sg.Combo(('Yes', 'No'), default_value='Yes', key=k7)],
            [sg.Text(k8), sg.Combo(('Yes', 'No'), default_value='Yes', key=k8)],
            [sg.Text(k9), sg.Combo(('Yes', 'No'), default_value='Yes', key=k9)],
            [sg.Text(k10), sg.InputText('', key=k10)],
            [sg.Text(k11), sg.InputText('Legacy ID', key=k11)],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]
        ]
        window = sg.Window('', layout)
        event, values = window.read()
        window.close()
        if event in (None, 'Cancel'):
            return
        li = []
        sql_pre = 'INSERT INTO z_newcreate_data_import_config(taskName,taskValue) VALUES('
        for key, value in values.items():
            if value == '':
                value = 'NULL'
            sql = sql_pre + '"' + key + '",' + '"' + value + '");\n'
            li.append(sql)
        with open(configration_sql_new, 'r', encoding='utf8') as fa:
            lines = fa.readlines()
        idx_s = lines.index('# Custom Conigurations Start\n')
        idx_e = lines.index('# Custom Conigurations End\n')
        lines_new = lines[:idx_s+1] + li + lines[idx_e:]
        with open(configration_sql_new, 'w', encoding='utf8') as fw:
            fw.writelines(lines_new)
        merge = 'True'
        if values[k2] == 'Do Not De-Dupe':
            merge = 'False'
        self.HandleConfig.handle_config("s", jiraname, "merge", merge)
        self.MysqlRestore.main(currentwork)
































from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg
import shutil
import re
from events.mysqlrestore import MysqlRestore
from events.mysqldump import MysqlDump
from collections import defaultdict
from events.download import Download
from datetime import date


class ConfigScript:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.MysqlRestore = MysqlRestore()
        self.MysqlDump = MysqlDump()
        self.Download = Download()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()

    def main(self, currentwork):
        jirapath = self.HandleConfig.handle_config('g', currentwork, 'jirapath')
        jiraname = self.HandleConfig.handle_config('g', currentwork, 'jiraname')
        git_repo_path = self.HandleConfig.handle_config('g', 'defaultpath', 'git_repo_path')
        gitscriptpath = git_repo_path + 'dataImportScript\\script\\'
        configration_sql = gitscriptpath + 'configration.sql'
        configration_sql_new = jirapath + 'script\\configration.sql'
        # read local configration.sql
        with open(configration_sql_new, 'r', encoding='utf8') as (fa):
            lines = fa.readlines()
        idx_s = lines.index('# Custom Conigurations Start\n')
        idx_e = lines.index('# Custom Conigurations End\n')
        config_lines = lines[idx_s+1:idx_e]
        layout = []
        option_dict = defaultdict()
        idx = 0
        for line in config_lines:
            if not re.match('^INSERT INTO z_newcreate_data_import_config', line, re.IGNORECASE):
                continue
            s = line.split('(')
            k = s[2].split(',')[0].replace("'", '').strip()
            d = s[2].split(',')[1].replace("'", '').replace(')', '').replace(';', '').replace('#', '').strip()
            option_dict[k] = ''

            if len(s) > 3:
                # dropdown
                options = s[3:]
                option_dict[k] = '#(' + '('.join(options)
                for i in range(len(options)):
                    options[i] = options[i].replace("'", '').replace(')', '').replace('\n', '').replace(',', '')
                lay = [
                 sg.Text(k), sg.Combo(options, default_value=d, key=k)]
            else:
                # oneline text
                if re.match('^Legacy Account Custom Field Name', k, re.IGNORECASE):
                    k = 'Legacy Account Custom Field Name' + str(idx)
                    idx+=1
                option_dict[k] = ''
                lay = [sg.Text(k), sg.InputText(d, key=k)]
            layout.append(lay)

        layout.append([sg.Submit(), sg.Cancel(),sg.Button('Git Configration.sql')])
        window = sg.Window(title=currentwork, layout=layout)
        event, values = window.read()
        window.close()
        if event in (None, 'Cancel'):
            return

        # copy configration.sql from git repo
        # relace new config into configration.sql
        shutil.copy(configration_sql, configration_sql_new)
        if event == 'Git Configration.sql': 
            return
            
        li = []
        sql_pre = 'INSERT INTO z_newcreate_data_import_config(taskName,taskValue) VALUES('

        for key, value in values.items():
            key_true = key
            if re.match('^Legacy Account Custom Field Name', key, re.IGNORECASE):
                key_true = 'Legacy Account Custom Field Name'
            if key == 'Work Start Date':
                if value == '':
                    value = str(date.today())
            sql = sql_pre + "'" + key_true + "'," + "'" + value + "');" + option_dict[key] + '\n'
            li.append(sql)
        with open(configration_sql, 'r', encoding='utf8') as (fa):
            lines = fa.readlines()
        idx_s = lines.index('# Custom Conigurations Start\n')
        idx_e = lines.index('# Custom Conigurations End\n')
        lines_new = lines[:idx_s + 1] + li + lines[idx_e:]
        with open(configration_sql_new, 'w', encoding='utf8') as (fw):
            fw.writelines(lines_new)
        merge = 'True'
        if values['Account De-dupe Rule'] == 'No De-dupe':
            merge = 'False'
        self.HandleConfig.handle_config('s', jiraname, 'merge', merge)

        # download database
        if values['Pull Database From AWS'] == 'Yes':
            self.Download.main(currentwork)
        # restore
        self.MysqlRestore.main(currentwork, advanced=0)
        # dump to dbname_after
        self.MysqlDump.main(currentwork, after=1, op='mysqldump')

        sg.Popup('Config Complete!', title=currentwork)


if '__name__' == '__main__':
    ConfigScript = ConfigScript()
    ConfigScript.main('')

import os
from common.handleconfig import HandleConfig


class File:

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def open_work_dir(self, currentwork):
        work_dir = self.HandleConfig.handle_config('g', currentwork, 'jirapath')
        os.startfile(work_dir)

    def open_git_dir(self):
        git_dir = self.HandleConfig.handle_config('g', 'defaultpath', 'git_repo_path')
        os.startfile(git_dir)

    def open_tmp(self, currentwork):
        tmptxt = self.HandleConfig.handle_config('g', currentwork, 'jirapath') + 'script\\tmp.txt'
        os.popen(tmptxt)

    def append_templete_scripts(self, currentwork):
        import shutil
        git_dir = self.HandleConfig.handle_config('g', 'defaultpath', 'git_repo_path')
        navicat_script_path = self.HandleConfig.handle_config('g', 'defaultpath', 'navicat_script_path')
        dbname = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        navicat_script = navicat_script_path + dbname + '\\{}.sql'.format(dbname)
        gittemplatepath = git_dir + 'templates\\'
        scripts = [
            gittemplatepath + 'basic_account_info_extra_data_script.sql',
            gittemplatepath + 'transaction_script.sql',
            gittemplatepath + 'gais.sql',
            gittemplatepath + 'custom_field.sql',
        ]

        with open(navicat_script, 'a', encoding='utf8') as fa:
            for script in scripts:
                with open(script, 'r', encoding='utf8') as fr:
                    fa.writelines(['\n\n'])
                    shutil.copyfileobj(fr, fa)



if '__name__' == '__main__':
    File = File()
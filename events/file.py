
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


if '__name__' == '__main__':
    Setting = File()
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg
import git

sg.ChangeLookAndFeel('GreenTan')


class GitScripts:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()
        self.imgpath = self.HandleConfig.handle_config("g", "referencefile", "img")

    def main(self):
        git_repo_path = self.HandleConfig.handle_config("g", "global", "git_repo_path")

        repo = git.Repo(git_repo_path)
        remote = repo.remote()
        # 从远程版本库拉取分支
        remote.pull('master')


















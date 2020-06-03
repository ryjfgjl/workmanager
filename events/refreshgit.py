
from common.handleconfig import HandleConfig
import PySimpleGUI as sg
import git

sg.ChangeLookAndFeel('GreenTan')

class RefreshGit:

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def main(self):

        git_repo_path = self.HandleConfig.handle_config("g", "defaultpath", "git_repo_path")
        #git_repo_path = 'E:\\git\\hello-world\\'
        repo = git.Repo(git_repo_path)
        remote = repo.remote()
        remote.pull()
        sg.Popup('Complete!')


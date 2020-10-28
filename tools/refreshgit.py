
from common.handleconfig import HandleConfig
import PySimpleGUI as sg, git


class RefreshGit:

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def main(self):

        git_repo_path = self.HandleConfig.handle_config('g', 'defaultpath', 'git_repo_path')
        repo = git.Repo(git_repo_path)
        git_new = repo.git
        ret = git_new.pull()
        sg.Popup('{0}'.format(ret))


if '__name__' == '__main__':
    RefreshGit = RefreshGit()
    RefreshGit.main()
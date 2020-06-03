
from jira.client import JIRA
import re
from common.handleconfig import HandleConfig
import PySimpleGUI as sg


sg.ChangeLookAndFeel('GreenTan')


class CheckUpdate:

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def main(self, Version):

        download_dictionary = self.HandleConfig.handle_config("g", "defaultpath", "workpath")
        username = 'xiaobo.zhang@dev.neoncrm.com'
        password = 'qqq2577154121'
        api_token = "qxVxseuhgFhFBZ8S6uG180DB"
        jira = JIRA(basic_auth=(username, api_token),
                         options={'server': 'https://neoncrm.atlassian.net'})

        issue = jira.issue('INT-30')
        for attachment in issue.fields.attachment:
            name = attachment.filename
            if re.fullmatch(r"^Work Manager (\d+)\.(\d+)\.(\d+)\.zip$", name):
                match = re.fullmatch(r"^Work Manager (\d+\.\d+\.\d+)\.zip$", name)
                version_newest = match.group(1)
                version_newest_bakup = version_newest
                Version = int(Version.split('.')[0])*100 + int(Version.split('.')[1])*10 + int(Version.split('.')[2])*1
                version_newest = int(version_newest.split('.')[0])*100 + int(version_newest.split('.')[1])*10 + int(version_newest.split('.')[2])*1

                if Version < version_newest:
                    yn = sg.popup_yes_no("The newest version {} of Work Manager is available, get it now?".format(version_newest_bakup))
                    if yn == 'Yes':
                        path = download_dictionary + attachment.filename
                        with open(path, "wb") as f:
                            f.write(attachment.get())
                        sg.Popup("Work Manager {0} have downloaded to {1}".format(version_newest_bakup, download_dictionary))
                else:
                    sg.Popup("Work Manager is the newest")






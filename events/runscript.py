from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')

class RunScript:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.conn = self.ConnDB.conndb()
        self.imgpath = self.HandleConfig.handle_config("g", "referencefile", "img")

    def main(self, currentwork, sqlfiles=None):
        jirapath = self.HandleConfig.handle_config("g", currentwork, "jirapath")
        dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")

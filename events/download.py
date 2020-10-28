
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import os


class Download:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    def main(self, currentwork):
        dbname = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        winscppath = self.HandleConfig.handle_config('g', 'defaultpath', 'winscppath')
        database_backup = '/home/neon/leiwu/database_backup/' + dbname + '_backup.sql.gz'
        db_backup_path = self.HandleConfig.handle_config('g', currentwork, 'jirapath') + 'db_backup\\'
        cmd = '{0}WinSCP.com /command "open aws188" "get {1} {2}" "exit"'.format(winscppath, database_backup, db_backup_path)
        os.system(cmd)


if '__name__' == '__main__':
    Download = Download()
    Download.main('')
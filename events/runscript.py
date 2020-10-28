
from events.mysqlrestore import MysqlRestore


class RunScript:

    def __init__(self):
        self.MysqlRestore = MysqlRestore()

    def main(self, currentwork):
        self.MysqlRestore.main(currentwork, advanced=2)


if '__name__' == '__main__':
    RunScript = RunScript()
    RunScript.main('')
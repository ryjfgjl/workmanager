
"""
Dump mysql
"""

import shutil
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import gzip
import os
import PySimpleGUI as sg
from common.conndb import ConnDB


class MysqlDump:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    def main(self, currentwork, advanced=0, gz=False, after=0, op='mysqldump-no-r'):
        jirapath = self.HandleConfig.handle_config('g', currentwork, 'jirapath')
        dbname = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        sqlname = '{0}.sql'.format(dbname)
        sqlfile = jirapath + 'script\\' + sqlname
        if after:
            sqlfile = jirapath + 'script\\' + '{0}_after.sql'.format(dbname)
        if not op:
            op = 'mysqldump-no-r'
        tablesname = ''

        if advanced:
            layout = [
                [sg.Text('Database Name: {0}'.format(dbname))],
                [sg.Text('Tables Name:'), sg.InputText(key='tablesname')],
                [sg.Text('File Name:'), sg.InputText(key='filename')],
                [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]
            ]
            window = sg.Window('', layout=layout)
            event, values = window.read()
            window.close()
            if event in (None, 'Cancel'):
                return
            tablesname = values['tablesname']
            filename = values['filename']
            if filename:
                sqlfile = jirapath + 'script\\' + filename

        if gz:

            sql = """select TABLE_NAME from information_schema.TABLES t where TABLE_SCHEMA =database() and TABLE_NAME like 'z\_%' and TABLE_NAME NOT like 'z\_backup%' and TABLE_NAME NOT REGEXP '^z_excel_.*_20[0-9]{6}$' and TABLE_NAME NOT REGEXP '^z_newcreate_.*_20[0-9]{6}$' AND table_name NOT IN('z_newcreate_sequence_number_table','z_newcreate_revert_group_concat_bak','z_newcreate_extra_campaign','z_newcreate_extra_fund','z_newcreate_extra_purpose','z_newcreate_extra_tender','z_newcreate_extra_event','z_newcreate_extra_event_category_cd','z_newcreate_extra_membership_term','z_newcreate_extra_fundraiser','z_newcreate_all_custom_data_smoke_test', 'z_newcreate_all_custom_data_options_smoke_test', 'z_newcreate_wxm_membership_email_condition_smoke_test', 'z_newcreate_wxm_membershipEmailCondition_sep_smoke_test', 'z_newcreate_wxm_membershipLetterCondi_smoke_test', 'z_newcreate_wxm_membershipLetterCondi_sep_smoke_test', 'z_newcreate_wxm_shopping_cart_items_smoke_test', 'z_newcreate_prepare_statement_to_proceed_smoke_test', 'z_newcreate_wxm_may_be_drop_down_smoke_test', 'z_newcreate_cutoff_columns_smoke_test', 'z_newcreate_wxm_donation_smoke_test', 'z_newcreate_wxm_credit_card_id_smoke_test', 'z_newcreate_max_id_b4import_for_system_tables', 'z_newcreate_prepare_statement_to_proceed', 'z_newcreate_match_multiple_company', 'z_smoke_test_newcreate_past_duplicate_custom_field', 'z_newcreate_current_duplicate_custom_field_smoke_test', 'z_newcreate_check_table_name_column','z_newcreate_all_onelinetext_custom_field');"""
            conn = self.ConnDB.conndb(dbname)
            result = self.ConnDB.exec(conn, sql)
            result = ['drop table if exists '+t[0] for t in result]
            sql = ';'.join(result)
            self.ConnDB.exec(conn, sql)

            sqlfile = jirapath + 'db_backup\\' + sqlname
            sqlfile_gzip = jirapath + '\\db_backup\\{0}.sql.gz'.format(dbname)
            op = 'mysqldump'
            ret = self.ConnDB.cmd(dbname, op, sqlfile)
            if ret == 0:
                with open(sqlfile, 'rb') as (f_in):
                    with gzip.open(sqlfile_gzip, 'wb') as (f_out):
                        shutil.copyfileobj(f_in, f_out)
                os.remove(sqlfile)

            # get after_size
            after_size = os.path.getsize(sqlfile_gzip)/1024/1024
            after_size = int('{:.0f}'.format(after_size))
            try:
                b4_size = int(self.HandleConfig.handle_config('g', currentwork, 'b4_size'))
                if b4_size < 100 and after_size >= 100:
                    sql = "DROP TABLE IF EXISTS z_newcreate_table_row;CREATE TABLE z_newcreate_table_row SELECT 'account' tableName, (SELECT count(*) FROM account) tableRow " \
                          "UNION ALL SELECT 'donation' tableName, (SELECT count(*) FROM donation) tableRow UNION ALL SELECT 'event_registration' tableName, (SELECT count(*) FROM event_registration) tableRow " \
                          "UNION ALL SELECT 'event_attendee' tableName, (SELECT count(*) FROM event_attendee) tableRow UNION ALL SELECT 'membership_listing' tableName, (SELECT count(*) FROM membership_listing) tableRow " \
                          "UNION ALL SELECT 'payment' tableName, (SELECT count(*) FROM payment) tableRow;"
                    self.ConnDB.exec(conn, sql)
                    sg.Popup('The size of database is more than 100M! See z_newcreate_table_row', title=currentwork)
            except:
                pass

        else:
            ret = self.ConnDB.cmd(dbname, op, sqlfile, tablesname)
            if ret == 0:
                with open(sqlfile, 'a') as (fa):
                    fa.write('COMMIT;')
            if advanced:
                sg.Popup('Complete!')


if '__name__' == '__main__':
    MysqlDump = MysqlDump()
    MysqlDump.main('')
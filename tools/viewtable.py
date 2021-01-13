"""
Add comment
"""

from common.handleconfig import HandleConfig
import PySimpleGUI as sg
from common.conndb import ConnDB


class ViewTable:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    def main(self, currentwork):
        database = self.HandleConfig.handle_config('g', currentwork, 'dbname')
        conn = self.ConnDB.conndb(database)
        sql = """DROP table if exists z_newcreate_neon_data_stats_report;
create table z_newcreate_neon_data_stats_report(tableName varchar(100),tableRows INT);

insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'account',count(1) from account;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'user',count(1) from user;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'donation',count(1) from donation;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'membership_listing',count(1) from membership_listing;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'event_registration',count(1) from event_registration;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'event_attendee',count(1) from event_attendee;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'shopping_cart_items',count(1) from shopping_cart_items;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'payment',count(1) from payment;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'account_custom_data',count(1) from account_custom_data;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'donation_custom_data',count(1) from donation_custom_data;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'membership_listing_custom_data',count(1) from membership_listing_custom_data;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'event_registration_custom_data',count(1) from event_registration_custom_data;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'event_attendee_custom_data',count(1) from event_attendee_custom_data;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'user_custom_data',count(1) from user_custom_data;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'company_custom_data',count(1) from company_custom_data;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'contact_activity_custom_data',count(1) from contact_activity_custom_data;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'note',count(1) from note;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'address',count(1) from address;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'relation',count(1) from relation;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'company_contact',count(1) from company_contact;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'household_contact',count(1) from household_contact;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'contact_activity',count(1) from contact_activity;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'proposal',count(1) from proposal;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'solicitation',count(1) from solicitation;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'invitation',count(1) from invitation;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'material_tracking',count(1) from material_tracking;
insert into z_newcreate_neon_data_stats_report(tableName,tableRows)
  select 'soft_credit',count(1) from soft_credit;
  select * from z_newcreate_neon_data_stats_report order by tableRows desc"""
        ret = self.ConnDB.exec(conn, sql)
        result = ret.fetchall()
        if len(result) > 0:
            layout = [
                [sg.Table(result,
                          ['tableName', 'tableRows'],
                          col_widths=[25, 10], auto_size_columns=False, justification="left",size=(35,30))
                 ]
            ]
            window = sg.Window(title=currentwork, layout=layout)
            event, values = window.read()
            window.close()


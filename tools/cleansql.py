# Remove unless 9999 field from insert sql

import PySimpleGUI as sg
import pyperclip
import re
import sqlparse


class CleanSql:

    def main(self):
        layout = [
            [sg.Text('Input your sql')],
            [sg.Multiline(size=(150, 10), key='i')],
            [sg.Button('Clean')],
            [sg.Text('Cleaned sql')],
            [sg.Multiline(size=(150, 10), key='o')],
            [sg.Button('Copy')]
        ]
        window = sg.Window(title='Sql Cleaner', layout=layout)

        for i in range(10000000):
            try:
                event, values = window.read()
                sql_cleaned = ''
                if event is None:
                    break

                sql = values['i'].strip()

                if len(sql) == 0:
                    continue

                if event == 'Clean':
                    # parse sql
                    tokens = sqlparse.parse(sql)[0].tokens
                    insert = ''
                    selects = []
                    fields = []
                    select = ''
                    parse_insert = True
                    parse_select = False
                    parse_from = False
                    for token in tokens:
                        value = token.value
                        vtype = str(type(token))
                        ttype = str(token.ttype)

                        # parse insert sql
                        if parse_insert:
                            insert = insert + value
                            if ttype == 'Token.Keyword.DML' and value.upper() == 'SELECT':
                                parse_insert = False
                                parse_select = True

                        # parse select sql
                        if parse_select:
                            if ttype == 'Token.Keyword.DML' and value.upper() == 'SELECT':
                                fields.append(value)
                            elif vtype == "<class 'sqlparse.sql.IdentifierList'>":
                                for field in token.get_identifiers():
                                    fields.append(field.value)
                            elif ttype == 'Token.Keyword' and value.upper() == 'FROM':
                                parse_from = True
                                parse_select = False

                        if parse_from:
                            select = select + value

                        if ttype == 'Token.Keyword' and value.upper() in ('UNION', 'UNION ALL'):
                            select = ' ' + select
                            fields.append(select)
                            selects.append(fields)
                            select = ''
                            fields = []
                            parse_from = False
                            parse_select = True

                    select = ' ' + select
                    fields.append(select)
                    selects.append(fields)
                    insert = insert[:-6].strip()

                    insert = insert.split(')')[0]
                    insert, table = insert.split('(')[1], [insert.split('(')[0] + '(']
                    insert_fields = [i.strip() for i in insert.split(',')]
                    insert_fields = table + insert_fields + [')']

                    # check SQL syntax
                    error = 0
                    for select in selects:
                        if len(select) != len(insert_fields):
                            error = 1
                    if error:
                        sg.popup_error('SQL syntax Error!')
                        continue

                    # replace 9999 field to NULL
                    sele_num = len(selects)
                    remove_fields = []

                    for i in range(len(insert_fields)):
                        insert_field = insert_fields[i]
                        insert_field_9999 = insert_field + '9999'
                        num_9999 = 0
                        for select in selects:
                            select_field = select[i]
                            if select_field == insert_field_9999:
                                num_9999 += 1
                                if num_9999 == sele_num:
                                    remove_fields.append(insert_field)

                    # remove fields
                    for field in remove_fields:
                        insert_fields.remove(field)

                        for select in selects:
                            select.remove(field + '9999')

                    for i in range(len(insert_fields)):
                        insert_field = insert_fields[i]
                        insert_field_9999 = insert_field + '9999'
                        num_9999 = 0
                        for select in selects:
                            select_field = select[i]
                            if select_field == insert_field_9999:
                                if insert_field not in remove_fields:
                                    select[i] = 'NULL'

                    # combine cleaned insert sql
                    insert_cleaned = insert_fields[0] + ','.join(insert_fields[1:-1]) + insert_fields[-1]

                    # combine cleaned select sql
                    select_cleaned = ''

                    for select in selects:
                        select_cleaned = select_cleaned + select[0] + ' ' + ','.join(select[1:-1]) + select[-1] + '\n'

                    sql_cleaned = insert_cleaned + '\n' + select_cleaned

                if event == 'Copy':
                    sql_cleaned = values['o'].strip()
                    pyperclip.copy(sql_cleaned)

            except Exception as reason:
                sg.popup_error(reason)
                continue
            finally:
                window['o'].update(sql_cleaned)

        window.close()


if '__name__' == '__main__':
    CleanSql = CleanSql()
    CleanSql.main()

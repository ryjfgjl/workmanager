"""
batch import excels or csvs into mysql database in NeonCRM

"""

import easygui
import os
import pymysql
import re
from collections import defaultdict
import numpy as np
import pandas as pd
import chardet
from datetime import date
from common.handleconfig import HandleConfig
from common.conndb import ConnDB
import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')

class ImportExcel:

    def __init__(self):

        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()
        self.cleansql = self.HandleConfig.handle_config("g", "referencefile", "cleanexcel")
        self.nickname = self.HandleConfig.handle_config("g", "excelimporter", "nickname")
        self.indentify_col_name = int(self.HandleConfig.handle_config("g", "excelimporter", "indentify_col_name"))

    def main(self, currentwork):
        self.dbname = self.HandleConfig.handle_config("g", currentwork, "dbname")
        self.importexcelpath = self.HandleConfig.handle_config("g", currentwork, "jirapath") + 'xlsx\\importexcels\\'

        excelcsvs = self.get_excel()
        if not excelcsvs:
            sg.Popup("No excels can import!")
            return

        log_file = self.importexcelpath + "\\log.txt"
        if os.path.isfile(log_file):
            os.remove(log_file)

        sql = "drop database if exists `{0}`;create database `{0}`".format(self.dbname, self.dbname)
        conn_db = self.ConnDB.conndb()
        self.ConnDB.exec(conn_db, sql)
        conn_db.close()
        self.conn = self.ConnDB.conndb(self.dbname)
        print("Created database {}".format(self.dbname))

        longexcelcsvs = defaultdict()
        long_num = 0
        num = 0
        num_s = 0

        print("Begin to import...\n")
        for excelcsv, origin_tablename in excelcsvs.items():
            self.excel_name = excelcsv
            try:
                isexcel = 0
                if re.fullmatch(r"^.*?\.csv$", excelcsv, flags=re.IGNORECASE):
                    datasets = defaultdict()
                    csv = self.importexcelpath + "\\" + excelcsv
                    with open(csv, 'rb') as f:
                        bytes = f.read()
                        if len(bytes) > 100000:
                            with open(csv, 'rb') as f:
                                bytes = f.readline()
                    encode = chardet.detect(bytes)['encoding']
                    if encode == 'ascii':
                        encode = 'ansi'  # ansi is a super charset of ascii and .txt only support ansi

                    dataset = pd.read_csv(csv, encoding=encode, dtype=str, na_filter=False, header=0, engine="c")
                    datasets['sheet1'] = dataset

                if re.fullmatch(r"^.*?\.xlsx?$", excelcsv, flags=re.IGNORECASE):
                    isexcel = 1
                    excel = self.importexcelpath + "\\" + excelcsv
                    datasets = pd.read_excel(excel, dtype=str, na_filter=False, header=0, sheet_name=None)

                for k, v in datasets.items():
                    created_table = None
                    try:
                        sheet_name = k
                        dataset = v
                        tablename = origin_tablename
                        self.excel_name = excelcsv

                        if isexcel == 1 and len(datasets) > 1:
                            tablename = origin_tablename + '_' + re.sub(r"[^0-9a-z]+", "_", sheet_name,
                                                                        flags=re.IGNORECASE)
                            self.excel_name = excelcsv + '.' + sheet_name
                        tablename = tablename.lower() + "_" + str(date.today()).replace("-", "")
                        if len(tablename) > 64:
                            tablename = tablename[:51] + tablename[-9:] + "_{0}".format(long_num)
                            long_num += 1
                            longexcelcsvs[excelcsv] = tablename
                            with open(log_file, "a") as fw:
                                fw.write("extra long excel: {0}, tablename: {1}\n".format(self.excel_name, tablename))
                        col_maxlen, dataset = self.read_data(dataset)

                        if dataset.empty:
                            raise EmptyError("Empty")
                        created_table, created_sql = self.create_table(col_maxlen, tablename)
                        try:
                            self.insert_data(dataset, tablename)

                        except pymysql.err.InternalError as reason:
                            reason_num_0 = str(reason).split(",")[0].strip("(")

                            if reason_num_0 == "1366":
                                try:
                                    sql_0 = "alter table `{1}`.{2} convert to character set utf8mb4 collate utf8mb4_bin".format(
                                        self.dbname, self.dbname, created_table)
                                    self.ConnDB.exec(self.conn, sql_0)
                                    self.insert_data(dataset, tablename, charset="utf8mb4")
                                except pymysql.err.InternalError as reason:
                                    reason_num_1 = str(reason).split(",")[0].strip("(")
                                    if reason_num_1 == "1118":
                                        sql = re.sub(r"varchar\(\d+\)", "text", created_sql)
                                        sql_1 = "drop table if exists `{0}`.`{1}`;".format(self.dbname, tablename)
                                        self.ConnDB.exec(self.conn, sql_1)
                                        self.ConnDB.exec(self.conn, sql)

                                        sql_0 = "alter table `{1}`.{2} convert to character set utf8mb4 collate utf8mb4_bin".format(
                                            self.dbname, self.dbname, created_table)
                                        self.ConnDB.exec(self.conn, sql_0)
                                        self.insert_data(dataset, tablename, charset="utf8mb4")
                                    else:
                                        raise pymysql.err.InternalError(str(reason))

                            elif reason_num_0 == "1118":
                                sql = re.sub(r"varchar\(\d+\)", "text", created_sql)
                                sql_0 = "drop table if exists `{0}`.`{1}`;".format(self.dbname, tablename) + sql
                                self.ConnDB.exec(self.conn, sql_0)
                                self.insert_data(dataset, tablename)


                            else:
                                raise pymysql.err.InternalError(str(reason))


                    except Exception as reason:
                        print("Failed: {}".format(self.excel_name))

                        with open(log_file, "a") as fw:
                            fw.write("excel sheet name: {0}, error: {1}\n".format(self.excel_name, str(reason)))

                        if created_table:
                            sql = "drop table if exists `{0}`.`{1}`".format(self.dbname, created_table)
                            self.ConnDB.exec(self.conn, sql)

                        continue
                    else:
                        print("Imported: {}".format(self.excel_name))
                        num_s += 1
                    finally:
                        num += 1

            except Exception as reason:
                print("Failed: {}".format(excelcsv))
                with open(log_file, "a") as fw:
                    fw.write("excel file name: {0}, error: {1}\n".format(self.excel_name, str(reason)))
                num += 1
                continue

        print("\nTotal: {}, Imported: {}\n".format(num, num_s))
        event = 'Yes'
        if os.path.isfile(log_file):
            os.popen(log_file)
            sg.Popup("You have logs , see file '{}' \n\ncheck it first".format(log_file))
            if num_s == 0:
                sg.Popup("No imported tables!")
                return

            layout = [
                [sg.Text("Clean database {} now?".format(self.dbname))],
                [sg.Button('Yes', key='y'), sg.Button('No', key='n')]
            ]
            window = sg.Window('',layout)
            event, values = window.read()
            window.close()
        if event == 'Yes':
            self.clean_data()
        sg.Popup("Import Excel Over!")


    def get_excel(self):

        excels = os.listdir(self.importexcelpath)
        excelcsvs = defaultdict()

        for excel in excels:
            excel_dir = self.importexcelpath + "\\" + excel
            if os.path.isfile(excel_dir) and re.fullmatch(r"^.*?\.(xls|xlsx|csv)$", excel, flags=re.IGNORECASE):
                tablename = re.sub(r"\.(xls|xlsx|csv)$", '', excel.lower(), flags=re.IGNORECASE)
                tablename = "z_excel_" + self.nickname + '_' + re.sub(r"[^0-9a-z]+", "_", tablename,
                                                                      flags=re.IGNORECASE)
                excelcsvs[excel] = tablename

        return excelcsvs

    def read_data(self, dataset):
        # indentify_col_name
        dataset.columns = [str(col) for col in dataset.columns]
        self.columns = dataset.columns
        low_col = [col.lower() for col in self.columns]
        if self.indentify_col_name == 1:
            if "ignore" in low_col:
                self.columns = dataset[0:1]
                self.columns = np.array(self.columns)
                self.columns = self.columns.tolist()[0]
                dataset.columns = self.columns
                dataset.drop(0, inplace=True)

        self.columns = [str(col).strip() for col in self.columns]
        # fix blank col name
        f = lambda x: "unnamed" if x == "" else x
        self.columns = [f(col) for col in self.columns]

        f = lambda x: x if len(x) <= 63 else x[:62].strip()
        self.columns = [f(col) for col in self.columns]
        # fix duplicate column name

        while True:
            low_col = [col.lower() for col in self.columns]
            idx = 0
            odx = 0
            c = 0
            for i in self.columns:
                jdx = 0
                n = 1
                if idx == len(self.columns):
                    continue
                for j in low_col[idx + 1:]:
                    odx = idx + 1 + jdx
                    if j == i.lower():
                        self.columns[odx] = j + str(n)
                        n += 1
                        c += 1
                    jdx += 1
                idx += 1
            if c == 0:
                break

        dataset.columns = self.columns
        self.columns = np.array(self.columns)
        self.columns = self.columns.tolist()
        # speed faster 10 times

        f = lambda x: str(x).strip()
        dataset = dataset.applymap(f)
        f = lambda x: len(x)
        df1 = dataset.applymap(f)
        f = lambda x: max(x)
        df2 = df1.apply(f, axis=0)
        col_maxlen = df2.to_dict()

        df3 = df1.apply(f, axis=1)
        df3 = pd.DataFrame(df3, columns=["c"])
        indexs = df3.loc[df3["c"] == 0].index
        dataset.drop(indexs, inplace=True)

        f = lambda x: None if x == "" else x
        dataset = dataset.applymap(f)

        return col_maxlen, dataset

    def create_table(self, col_maxlen, tablename):
        sql = "create table `{0}`.`{1}`(".format(self.dbname, tablename)

        for col, maxLen in col_maxlen.items():
            colType = "varchar(255)"
            if maxLen > 255:
                colType = "TEXT"
            if maxLen > 65535:
                colType = "MEDIUMTEXT"
            if maxLen > 16777215:
                colType = "LONGTEXT"

            sql = sql + "`{0}` {1} default null,".format(col, colType)

        sql = sql[:-1] + ")"

        try:
            self.ConnDB.exec(self.conn, sql)

        except pymysql.InternalError:

            sql = re.sub(r"varchar\(\d+\)", "text", sql)
            self.ConnDB.exec(self.conn, sql)
        return tablename, sql

    def insert_data(self, dataset, tablename, charset="utf8"):
        # insert
        dataset = np.array(dataset)  # dataframe to ndarray
        datalist = dataset.tolist()  # ndarray to list
        cols = "`,`".join(self.columns)
        l = len(self.columns)
        v = "%s," * l
        v = v[:-1]
        sql = "insert into `%s`.`%s`(%s) values(" % (self.dbname, tablename, "`" + cols + "`")
        sql = sql + "%s)" % v

        if charset == "utf8mb4":
            conn_db = self.ConnDB.conndb(db=self.dbname, charset=charset)
            cur = conn_db.cursor()
            cur.executemany(sql, datalist)
            conn_db.commit()
            cur.close()
            conn_db.close()
        else:
            cur = self.conn.cursor()
            cur.executemany(sql, datalist)
            self.conn.commit()
            cur.close()

    def clean_data(self):
        print('Begin to clean data...\n')
        file = self.cleansql
        ret = self.ConnDB.cmd(self.dbname, "mysql", file)
        if ret == 0:
            print("Succeed: Clean data\n")
        else:
            sg.Popup("Clean Data Failed")

class EmptyError(Exception):
    pass


if "__name__" == "__main__":
    ImportExcel = ImportExcel()
    ImportExcel.main('')



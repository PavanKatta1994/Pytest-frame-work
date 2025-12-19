from datetime import datetime
import logging
import inspect
import os
import mysql.connector
import mysql
import softest
import openpyxl
import configparser

class Utils(softest.TestCase):

    @staticmethod
    def dataquery(schema, query):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
        )

        cursor = mydb.cursor()
        cursor.execute("use {};".format(schema))
        if ("update" in query.lower()) or ("insert" in query.lower()):
            cursor.execute("{};".format(query))
            mydb.commit()
            mydb.close()
        else:
            data = []
            cursor.execute("{};".format(query))
            data = cursor.fetchall()
            for d in data:
                print(d)
            mydb.close()
            return data

    @staticmethod
    def custom_logger(newlog = True):
        config = configparser.ConfigParser()
        config.read("../ConfigFiles/config.ini")
        generate_log = config["Logging"]["GenerateLogs"]
        loglevel = config["Logging"]["LogLevel"]
        if generate_log == "True":
            if newlog:
                try:
                    extn = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                    os.rename("../Logs/Automation_Log.log", "../Logs/Automation_Log_{}.log".format(extn))
                    os.chmod("../Logs/Automation_Log.log", 777)
                except FileNotFoundError:
                    print("No Log file found")
                    print("Proceeding to create new log file")
                else:
                    print("Existing log file renamed")
                    print("New log file to be created")
                # logger_name = inspect.stack()[1][3]
            frame = inspect.currentframe().f_back
            method_name = frame.f_code.co_name
            cls_name = frame.f_locals.get('self', None)
            class_name = cls_name.__class__.__name__ if cls_name else "NoClass"
            logger_name = f"{class_name}.{method_name}"
            logger = logging.getLogger(logger_name)
            logger.setLevel(loglevel)
            if not logger.handlers:
                fh = logging.FileHandler('../Logs/Automation_Log.log', mode='a')
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                              datefmt='%d-%m-%y %I:%M:%S %p')
                fh.setFormatter(formatter)
                logger.addHandler(fh)
            return logger


    @staticmethod
    def get_current_date():
        return datetime.today().date()

    @staticmethod
    def get_day_month_year_from_date(date):
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        except ValueError:
            print("provided Invalid date")
            print("Setting date as today")
            date_obj =  datetime.today().date()
            return date_obj.strftime("%d"),date_obj.strftime("%B"),date_obj.strftime("%Y"),date_obj
        else:
            return date_obj.strftime("%d"),date_obj.strftime("%B"),date_obj.strftime("%Y"),date_obj

    def compare_text_of_elements(self,element_list, value):
        utils = Utils()
        self.log = utils.custom_logger()
        fail_count = 0
        # print(type(element_list))
        self.log.info("no of values to be verified : {}".format(len(element_list)))
        for element in element_list:
            actual_value = element.text
            try:
                assert actual_value == value
                self.log.info(f"element {actual_value} was verified : {value}")
            except AssertionError:
                fail_count += 1
        return fail_count

    @staticmethod
    def update_excel(filename, sheetname, column_name, row_id, value):
        file = "../Testdata/" + filename + ".xlsx"
        excel = openpyxl.load_workbook(file)
        worksheet = excel[sheetname]
        column_count = 1
        for i in range(worksheet.max_column):
            col_val = worksheet.cell(1, i + 1).value
            if col_val == column_name:
                break
            else:
                column_count += 1
        col_id = column_count
        worksheet.cell(row_id + 1, column_count).value = value
        excel.save(file)
        excel.close()

    @staticmethod
    def ExcelData(filename, sheetname):
        file = "../Testdata/" + filename + ".xlsx"
        excel = openpyxl.load_workbook(file)
        worksheet = excel[sheetname]
        # calculating number of columns as test data
        column_count = 0
        for i in range(worksheet.max_column):
            value = worksheet.cell(1, i + 1).value
            if value != "Test Status":
                print(value)
                column_count += 1
            else:
                break
        rows = worksheet.max_row
        cols = column_count
        whole_date = []
        for i in range(rows-1):
            data = []
            for j in range(cols):
                value = worksheet.cell(i + 2, j + 1).value
                data.append(value)
            whole_date.append(data)
        excel.close()
        return whole_date

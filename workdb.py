# coding: future_fstrings
import config  # подключаем файл config.py с данным от БД
import psycopg2
from psycopg2 import Error

class SelectDatabase:
    """ Класс для работы с базой данных """

    def __init__(self):
        connection = None
        self.table_name = 'table_cef'
        self.processed_table_name = 'table_cef_processed'
        try:
            connection = self.connect()
            cursor = connection.cursor()
            print("Информация о сервере PostgreSQL")
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("Вы подключены к - ", record, "\n")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def connect(self):
        """ Подключение к базе данных """
        connection = psycopg2.connect(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_DATABASE
        )
        return connection

    def insert_info(self, data):
        """ Заполнение БД """

        connection = None

        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = "INSERT INTO public.table_cef (writing_utc, " \
                    "date_time, " \
                    "host, " \
                    "version, " \
                    "device_vendor, " \
                    "device_product, " \
                    "device_version, " \
                    "signature_id, " \
                    "name, " \
                    "severity, " \
                    "extension, " \
                    "original_message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            for row in data:
                cursor.execute(query, row)
                connection.commit()
            print('Результат записан')
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def insert_processed_data(self, data):
        connection = None

        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = f"INSERT INTO public.{self.processed_table_name} (processed_id, severity, device_id) VALUES (%s, %s, %s);"
            cursor.execute(query, data)
            connection.commit()
            print('Результат записан')
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def get_info(self, time=None, message=None, lastrec=None, dwnldreq=None, select_proc=None):
        """ Выборка данных из БД """

        connection = None
        raw_info = [time, message]
        info = []
        orderrec = ''
        reversedTuple = False
        info_table = self.table_name

        if lastrec is None:
            lastrec = 1000

        if lastrec == 100:
            orderrec = 'ORDER BY id DESC'
            reversedTuple = True

        if dwnldreq is not None and lastrec != 100:
            lastrec = 'ALL'

        if select_proc is not None:
            info_table = self.processed_table_name
        else:
            for i in range(len(raw_info)):
                k = raw_info[i]
                if None is not k:
                    if i == 0 and (time[0] and time[1]) is not None:
                        info.append(f"writing_utc BETWEEN '{time[0]}' and '{time[1]}'")
                    if i == 1:
                        message_array = message.replace(' ', '').split('&')
                        like_values = []
                        not_like_values = []
                        for message_element in message_array:
                            if message_element[0] == '!':
                                not_like_values.append(message_element[1:])
                            else:
                                like_values.append(message_element)
                        values_joined = "%'), ('%".join(like_values)
                        like_string = "values ('%" + values_joined + "%')"

                        info.append(f"original_message LIKE all({like_string})")

                        if not_like_values:
                            not_values_joined = "%'), ('%".join(not_like_values)
                            not_like_string = "values ('%" + not_values_joined + "%')"
                            info.append(f"original_message NOT LIKE all({not_like_string})")

        try:
            connection = self.connect()
            cursor = connection.cursor()
            if info:
                info_str = ' WHERE ' + ' and '.join(info)
            else:
                info_str = ''
            select_info = f'SELECT * FROM public.{info_table}{info_str} {orderrec} LIMIT {lastrec}'
            cursor.execute(select_info)
            result = cursor.fetchall()
            connection.commit()
            print("Результат успешно возвращен")
            if reversedTuple:
                result = tuple(reversed(result))
            return result
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def get_count(self, severity=None, processed=None):
        """ Получение количества строк из БД """
        connection = None
        info_str = None
        info_table = self.table_name

        if severity is not None:
            info_str = f' WHERE severity={severity}'
        else:
            info_str = ''

        if processed is not None:
            info_table = self.processed_table_name


        try:
            connection = self.connect()
            cursor = connection.cursor()
            select_info = f'SELECT COUNT(*) FROM public.{info_table}{info_str}'
            cursor.execute(select_info)
            result = cursor.fetchone()
            connection.commit()
            print("Результат успешно возвращен")
            return result[0]
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

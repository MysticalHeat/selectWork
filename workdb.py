# coding: future_fstrings
import config  # подключаем файл config.py с данным от БД
import psycopg2
from psycopg2 import Error


class SelectDatabase:
    """ Класс для работы с базой данных """

    def __init__(self):
        connection = None
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

    def get_info(self, time=None, message=None, lastrec=None, dwnldreq=None):
        """ Выборка данных из БД """

        connection = None
        raw_info = [time, message]
        info = []

        if lastrec is None:
            lastrec = 1000

        if dwnldreq is not None:
            lastrec = 'ALL'

        for i in range(len(raw_info)):
            k = raw_info[i]
            if None is not k:
                if i == 0 and (time[0] and time[1]) is not None:
                    info.append(f"writing_utc BETWEEN '{time[0]}' and '{time[1]}'")
                if i == 1:
                    info.append(f"to_tsvector(original_message) @@ to_tsquery('{message}')")

        try:
            connection = self.connect()
            cursor = connection.cursor()
            if info:
                info_str = ' WHERE ' + ' and '.join(info)
            else:
                info_str = ''
            select_info = f'SELECT * FROM public.table_cef{info_str} LIMIT {lastrec}'
            cursor.execute(select_info)
            result = cursor.fetchall()
            connection.commit()
            print("Результат успешно возвращен")
            return result
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")

    def get_count(self):
        """ Получение количества строк из БД """
        connection = None
        try:
            connection = self.connect()
            cursor = connection.cursor()
            select_info = 'SELECT COUNT(*) FROM public.table_cef'
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

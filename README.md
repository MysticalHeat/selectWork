# selectWork
Выборка данных из БД
Python 3.7

Команда для импорта БД:
pg_restore -h hostname -U username -F с -d dbname dump.tar.gz

Для импорта, БД уже должна существовать, файл только создает таблички и заполняет данными.

Также в корневом каталоге репозитория нужно создать файл config.py и добавить переменные DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE.

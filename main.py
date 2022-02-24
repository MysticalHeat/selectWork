import workdb

database = workdb.SelectDatabase()
database.get_info(time = ['2022-02-14 00:00:00', '2022-02-17 24:00:00'], source_id=[0, 2])
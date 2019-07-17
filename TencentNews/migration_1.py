from SqlHelper import SqlHelper
import config

sql = SqlHelper()

def col_exist(sql, colName):
    '''
    '''
    command = ("SELECT NULL FROM INFORMATION_SCHEMA.COLUMNS"
                " WHERE table_name='finance_news'" 
                " AND table_schema='news' AND column_name=")
                
    command += "'" + colName + "'"
    # returns list of Nones if column exists
    # returns None if column doesn't exist
    data = sql.query_one(command)
    return True if data else False

# adding new columns to the database:
if not col_exist(sql,'image_num'):
    command = "ALTER TABLE finance_news ADD image_num TINYINT UNSIGNED NOT NULL"
    sql.execute(command)

if not col_exist(sql,'img_urls'):
    command = "ALTER TABLE finance_news ADD img_urls TEXT"
    sql.execute(command)

if not col_exist(sql,'img_locs'):
    command = "ALTER TABLE finance_news ADD img_locs TEXT"
    sql.execute(command)

print("Done")
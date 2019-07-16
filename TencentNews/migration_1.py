from SqlHelper import SqlHelper
import config

sql = SqlHelper()
sql.execute("ALTER TABLE " + config.table_name + " ADD image_num TINYINT UNSIGNED NOT NULL")

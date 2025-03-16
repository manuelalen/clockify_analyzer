import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
table_name = "tiempos_produccion"
backup_file = "mysql\\tiempos_produccion.sql"


def exportar_mysql_a_sql(host, user, password, database, table_name, output_sql_file):
    # Conectar a MySQL
    conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()
    
    with open(output_sql_file, "w", encoding="utf-8") as f:
        # Obtener la estructura de la tabla específica
        cursor.execute(f"SHOW CREATE TABLE {table_name}")
        create_table_sql = cursor.fetchone()[1] + ";\n\n"
        f.write(create_table_sql)
        
        # Obtener los datos de la tabla específica
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        for row in rows:
            values = ", ".join([f"'{str(value).replace("'", "''")}'" if value is not None else "NULL" for value in row])
            insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({values});\n"
            f.write(insert_sql)
        f.write("\n")
    
    cursor.close()
    conn.close()
    print(f"Backup de la tabla {table_name} generado exitosamente en {output_sql_file}")




# Ejecutar la función de backup
exportar_mysql_a_sql(host, user, password, database, table_name, backup_file)

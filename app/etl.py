import os
from pathlib import Path
import pandas as pd
import pandera as pa
from dotenv import load_dotenv
from sqlalchemy import create_engine

from schema import ProductSchema, ProductSchemaKPI

def load_settings():
    dotenv_path = Path.cwd() / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    settings = {
        "db_host": os.getenv("POSTGRES_HOST"),
        "db_user": os.getenv("POSTGRES_USER"),
        "db_pass": os.getenv("POSTGRES_PASSWORD"),
        "db_name": os.getenv("POSTGRES_DB"),
        "db_port": os.getenv("POSTGRES_PORT")
    }
    return settings

@pa.check_output(ProductSchema, lazy=True)
def extract_from_sql(query: str) -> pd.DataFrame:
    settings = load_settings()
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"
    engine = create_engine(connection_string)
    with engine.connect() as conn, conn.begin():
        df_crm = pd.read_sql(query, conn)
    return df_crm

@pa.check_input(ProductSchema,lazy=True)
@pa.check_output(ProductSchemaKPI,lazy=True)
def transform(df: pd.DataFrame) -> pd.DataFrame:
    #calculate total stock value
    df['total_stock_value'] = df['quantity'] * df['price']

    #normalize category
    df['category_normalized'] = df['category'].str.lower()

    #Determine availability
    df['avalability'] = df['quantity'] > 0

    return df

import duckdb
import pandas as pd

@pa.check_input(ProductSchemaKPI,lazy=True)
def load_to_duckdb(df:pd.DataFrame, table_name: str, db_file: str = 'my_duckdb.db'):
    #connect to duckdb
    con = duckdb.connect(database=db_file, read_only=False)

    #Register with a temporary table
    con.register('df_temp', df)

    #Use SQL to insert data into the temp table in a permanent table
    con.execute((f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_temp"))

    #close connection
    con.close()

if __name__ == "__main__":

    query = 'SELECT * FROM product_bronze'
    df_crm = extract_from_sql(query=query)
    #df_crm_kpi=transform(df_crm)
    schema_crm=pa.infer_schema(df_crm)

    with open("schema_crm.py","w", encoding='UTF-8') as file:
        file.write(schema_crm.to_script())

    #load_to_duckdb(df=df_crm_kpi, table_name="kpi_table")
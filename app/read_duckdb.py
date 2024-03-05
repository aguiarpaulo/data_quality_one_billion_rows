import duckdb

def read_from_duckdb_and_print(table_name: str, db_file: str = 'my_duckdb.db'):
    """
    Read data from a DuckDB table and print the results.

    Parameters:
    - table_name: Name of the table from which data will be read.
    - db_file: Path to the DuckDB file.
    """
    # Connect to DuckDB
    con = duckdb.connect(database=db_file)

    # Execute SQL query
    query = f"SELECT * FROM {table_name}"
    result = con.execute(query).fetchall()

    # Close connection
    con.close()

    # Print results
    for row in result:
        print(row)

if __name__ == "__main__":
    # Table name for query
    table_name = "kpi_table"
    
    # Read data from table and print results
    read_from_duckdb_and_print(table_name)

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.etl import extract_from_sql, transform, load_to_duckdb

@pytest.fixture
def mock_create_engine():
    with patch('app.etl.create_engine') as mock:
        yield mock

def test_extract_from_sql(mock_create_engine):
    # Mock the connection and read_sql method
    mock_conn = MagicMock()
    mock_conn.begin().__enter__.return_value = mock_conn
    mock_read_sql = MagicMock(return_value=pd.DataFrame({
        'id': [1, 2, 3],
        'quantity': [10, 20, 30],
        'price': [5, 10, 15],
        'category': ['A', 'B', 'C']
    }))
    mock_conn.execute = MagicMock(return_value=mock_read_sql)
    mock_create_engine.return_value.connect.return_value = mock_conn

    # Call the function
    result_df = extract_from_sql('SELECT * FROM my_table')

    # Check if the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)

def test_transform():
    # Create a sample DataFrame
    df = pd.DataFrame({
        'quantity': [10, 20, 30],
        'price': [5, 10, 15],
        'category': ['A', 'B', 'C']
    })

    # Call the function
    result_df = transform(df)

    # Check if the total stock value is calculated correctly
    assert result_df['total_stock_value'].tolist() == [50, 200, 450]

    # Check if the category is normalized correctly
    assert result_df['category_normalized'].tolist() == ['a', 'b', 'c']

    # Check if availability is determined correctly
    assert result_df['avalability'].tolist() == [True, True, True]

def test_load_to_duckdb():
    # Create a sample DataFrame
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'quantity': [10, 20, 30],
        'price': [5, 10, 15],
        'category': ['A', 'B', 'C']
    })

    # Mock duckdb.connect method
    with patch('app.etl.duckdb.connect') as mock_connect:
        mock_con = MagicMock()
        mock_connect.return_value = mock_con

        # Call the function
        load_to_duckdb(df, 'test_table', 'test.db')

        # Check if duckdb.connect was called with correct arguments
        mock_connect.assert_called_with(database='test.db', read_only=False)

        # Check if duckdb.register and duckdb.execute were called with correct arguments
        mock_con.register.assert_called_with('df_temp', df)
        mock_con.execute.assert_called_with('CREATE OR REPLACE TABLE test_table AS SELECT * FROM df_temp')

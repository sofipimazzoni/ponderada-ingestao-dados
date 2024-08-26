import pytest
from unittest.mock import MagicMock
from data_pipeline.clickhouse_client import get_client, execute_sql_script, insert_dataframe

@pytest.fixture
def mock_client(mocker):
    # Mock do cliente ClickHouse
    return mocker.patch('data_pipeline.clickhouse_client.get_client', return_value=MagicMock())

def test_get_client(mocker):
    # Mock das variáveis de ambiente
    mocker.patch('os.getenv', side_effect=lambda key: {
        'CLICKHOUSE_HOST': 'localhost',
        'CLICKHOUSE_PORT': '8123'
    }.get(key))

    # Mock da função clickhouse_connect.get_client
    mock_get_client = mocker.patch('clickhouse_connect.get_client')
    get_client()
    mock_get_client.assert_called_once_with(host='localhost', port='8123')

def test_execute_sql_script(mock_client, mocker):
    script_path = 'path/to/script.sql'
    
    # Mock da leitura do arquivo
    mocker.patch('builtins.open', mocker.mock_open(read_data='SELECT * FROM table'))
    client = execute_sql_script(script_path)
    client.command.assert_called_once_with('SELECT * FROM table')

def test_insert_dataframe(mock_client, mocker):
    table_name = 'test_table'
    df = mocker.MagicMock()  # Mock do DataFrame

    insert_dataframe(mock_client, table_name, df)
    mock_client.insert_df.assert_called_once_with(table_name, df)

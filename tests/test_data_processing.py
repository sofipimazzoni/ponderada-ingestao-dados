import pytest
import pandas as pd
import pyarrow.parquet as pq
import os
from data_pipeline.data_processing import process_data, prepare_dataframe_for_insert

@pytest.fixture
def sample_data():
    return {"campo1": "sofia", "campo2": 10}

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'campo1': ['sofia', 'jp'],
        'campo2': [10, 20]
    })

def test_process_data(sample_data):
    filename = process_data(sample_data)
    
    assert os.path.exists(filename)
    table = pq.read_table(filename)
    assert table.num_rows == 1

    os.remove(filename)

def test_prepare_dataframe_for_insert(sample_dataframe):
    df = prepare_dataframe_for_insert(sample_dataframe)
  
    assert 'data_ingestao' in df.columns
    assert 'dado_linha' in df.columns
    assert 'tag' in df.columns
   
    assert pd.api.types.is_datetime64_any_dtype(df['data_ingestao'])
    assert df['dado_linha'].apply(lambda x: isinstance(x, str) and x.startswith('{')).all()
    assert (df['tag'] == 'example_tag').all()

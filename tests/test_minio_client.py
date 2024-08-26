import pytest
from data_pipeline.minio_client import create_bucket_if_not_exists, upload_file, download_file
import os

@pytest.fixture
def minio_client_mock(mocker):
    # Configurar o mock do cliente MinIO
    mock_minio = mocker.patch('data_pipeline.minio_client.minio_client')
    return mock_minio

def test_create_bucket_if_not_exists(minio_client_mock):
    bucket_name = 'test-bucket'
    
    # Simula o comportamento do método bucket_exists para retornar False
    minio_client_mock.bucket_exists.return_value = False
    create_bucket_if_not_exists(bucket_name)
    minio_client_mock.make_bucket.assert_called_once_with(bucket_name)

def test_create_bucket_if_not_exists_already_exists(minio_client_mock):
    bucket_name = 'existing-bucket'
    
    # Simula o comportamento do método bucket_exists para retornar True
    minio_client_mock.bucket_exists.return_value = True
    create_bucket_if_not_exists(bucket_name)
    minio_client_mock.make_bucket.assert_not_called()

def test_upload_file(minio_client_mock, tmpdir):
    bucket_name = 'test-bucket'
    file_path = os.path.join(tmpdir, 'test-file.txt')
    
    with open(file_path, 'w') as f:
        f.write('Test data')
    
    upload_file(bucket_name, file_path)
    minio_client_mock.fput_object.assert_called_once_with(bucket_name, 'test-file.txt', file_path)

def test_download_file(minio_client_mock, tmpdir):
    bucket_name = 'test-bucket'
    file_name = 'test-file.txt'
    local_file_path = os.path.join(tmpdir, 'downloaded-file.txt')

    download_file(bucket_name, file_name, local_file_path)
    minio_client_mock.fget_object.assert_called_once_with(bucket_name, file_name, local_file_path)


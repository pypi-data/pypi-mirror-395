import pytest
import boto3
from moto import mock_aws
from polly.s3_utils import copy_file


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    boto3.setup_default_session(
        aws_access_key_id="testing",
        aws_secret_access_key="testing",
        aws_session_token="testing",
    )


@pytest.fixture
def s3_client(aws_credentials):
    with mock_aws():
        conn = boto3.client("s3", region_name="us-east-1")
        yield conn


@pytest.fixture
def create_buckets(s3_client):
    s3_client.create_bucket(Bucket="source-bucket")
    s3_client.create_bucket(Bucket="destination-bucket")
    return s3_client


def test_copy_file_local_to_s3(create_buckets, s3_client, tmp_path):
    local_file = tmp_path / "test.txt"
    local_file.write_text("Hello, World!")

    copy_file(
        src_uri=str(local_file),
        dest_uri="s3://destination-bucket/test.txt",
        s3_client=s3_client,
    )

    response = s3_client.get_object(Bucket="destination-bucket", Key="test.txt")
    content = response["Body"].read().decode("utf-8")

    assert content == "Hello, World!"


def test_copy_file_s3_to_local(create_buckets, s3_client, tmp_path):
    s3_client.put_object(Bucket="source-bucket", Key="test.txt", Body="Hello, S3!")

    local_file = tmp_path / "downloaded_test.txt"
    copy_file(
        src_uri="s3://source-bucket/test.txt",
        dest_uri=str(local_file),
        s3_client=s3_client,
    )

    assert local_file.read_text() == "Hello, S3!"


def test_copy_file_s3_to_s3(create_buckets, s3_client):
    s3_client.put_object(
        Bucket="source-bucket", Key="test.txt", Body="Hello, S3 to S3!"
    )

    copy_file(
        src_uri="s3://source-bucket/test.txt",
        dest_uri="s3://destination-bucket/copied_test.txt",
        s3_client=s3_client,
    )

    response = s3_client.get_object(Bucket="destination-bucket", Key="copied_test.txt")
    content = response["Body"].read().decode("utf-8")

    assert content == "Hello, S3 to S3!"

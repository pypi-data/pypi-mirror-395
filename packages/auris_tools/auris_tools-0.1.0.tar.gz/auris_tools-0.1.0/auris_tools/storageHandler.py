import logging
from http import HTTPStatus

import boto3

from auris_tools.configuration import AWSConfiguration


class StorageHandler:
    def __init__(self, config=None):
        """
        Initialize the storage handler with AWS configuration.

        Args:
            config: An AWSConfiguration object, or None to use environment variables
        """
        if config is None:
            config = AWSConfiguration()

        # Create a boto3 session with the configuration
        session = boto3.session.Session(**config.get_boto3_session_args())

        # Create an S3 client with additional configuration if needed
        self.client = session.client('s3', **config.get_client_args())
        logging.info(f'Initialized S3 client in region {config.region}')

    def upload_file(self, file_path, bucket_name, object_name):
        """
        Upload a file to an S3 bucket.

        Args:
            file_path: Path to the file to upload
            bucket_name: Name of the bucket to upload to
            object_name: S3 object name (key)

        Returns:
            True if file was uploaded successfully, else False
        """
        try:
            self.client.upload_file(file_path, bucket_name, object_name)
            logging.info(
                f'Uploaded {file_path} to {bucket_name}/{object_name}'
            )
            return True
        except Exception as e:
            logging.error(f'Error uploading file {file_path}: {str(e)}')
            return False

    def download_file(self, bucket_name, object_name, file_path):
        """
        Download a file from an S3 bucket.

        Args:
            bucket_name: Bucket name
            object_name: S3 object name (key)
            file_path: Path where the file should be saved

        Returns:
            True if file was downloaded successfully, else False
        """
        try:
            self.client.download_file(bucket_name, object_name, file_path)
            logging.info(
                f'Downloaded {bucket_name}/{object_name} to {file_path}'
            )
            return True
        except Exception as e:
            logging.error(f'Error downloading file {object_name}: {str(e)}')
            return False

    def get_file_object(self, bucket_name, object_name, as_bytes=False):
        """
        Get a file object from an S3 bucket.

        Args:
            bucket_name: Bucket name
            object_name: S3 object name (key)
            as_bytes: If True, return the content as bytes instead of a streaming object

        Returns:
            S3 object (streaming) or bytes if as_bytes=True or None if not found
        """
        try:
            response = self.client.get_object(
                Bucket=bucket_name, Key=object_name
            )
            if as_bytes:
                return response['Body'].read()
            return response['Body']
        except Exception as e:
            logging.error(f'Error getting file object {object_name}: {str(e)}')
            return None

    def check_file_exists(self, bucket_name, object_name):
        """
        Check if a file exists in an S3 bucket.

        Args:
            bucket_name: Bucket name
            object_name: S3 object name (key)

        Returns:
            True if file exists, else False
        """
        try:
            self.client.head_object(Bucket=bucket_name, Key=object_name)
            return True
        except Exception:
            return False

    def check_file_size(self, bucket_name, object_name):
        """
        Get the size of a file in an S3 bucket.

        Args:
            bucket_name: Bucket name
            object_name: S3 object name (key)

        Returns:
            File size in bytes or None if file doesn't exist
        """
        try:
            response = self.client.head_object(
                Bucket=bucket_name, Key=object_name
            )
            return response.get('ContentLength')
        except Exception as e:
            logging.error(
                f'Error checking file size for {object_name}: {str(e)}'
            )
            return None

    def delete_file(self, bucket_name, object_name):
        """
        Delete a file from an S3 bucket.

        Args:
            bucket_name: Bucket name
            object_name: S3 object name (key)

        Returns:
            True if file was deleted successfully, else False
        """
        try:
            # Check if file exists before attempting deletion
            if not self.check_file_exists(bucket_name, object_name):
                logging.warning(
                    f'File {bucket_name}/{object_name} does not exist.'
                )
                return False

            response = self.client.delete_object(
                Bucket=bucket_name, Key=object_name
            )
            status_code = response.get('ResponseMetadata', {}).get(
                'HTTPStatusCode'
            )
            # Both 200 (OK) and 204 (No Content) are successful responses
            if status_code not in (HTTPStatus.OK, HTTPStatus.NO_CONTENT):
                logging.error(
                    f'Failed to delete {bucket_name}/{object_name}, status code: {status_code}'
                )
                return False

            logging.info(f'Deleted {bucket_name}/{object_name}')
            return True
        except Exception as e:
            logging.error(f'Error deleting file {object_name}: {str(e)}')
            return False

    def list_files(self, bucket_name, prefix=''):
        """
        List files in an S3 bucket with optional prefix filtering.

        Args:
            bucket_name: Bucket name
            prefix: Prefix to filter objects (folder path)

        Returns:
            List of object keys or empty list if error occurs
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket_name, Prefix=prefix
            )
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append(obj['Key'])
            return files
        except Exception as e:
            logging.error(
                f'Error listing files in {bucket_name}/{prefix}: {str(e)}'
            )
            return []

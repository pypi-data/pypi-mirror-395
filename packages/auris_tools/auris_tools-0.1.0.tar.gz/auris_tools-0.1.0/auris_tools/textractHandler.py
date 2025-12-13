import logging
import time

import boto3

from auris_tools.configuration import AWSConfiguration


class TextractHandler:
    """
    Handler for Amazon Textract operations to extract text from documents.

    This class provides methods to interact with AWS Textract service for
    text extraction from documents stored in S3.
    """

    def __init__(self, config=None):
        """
        Initialize the Textract handler with AWS configuration.

        Args:
            config: An AWSConfiguration object, or None to use environment variables
        """
        if config is None:
            config = AWSConfiguration()

        # Create a boto3 session with the configuration
        session = boto3.session.Session(**config.get_boto3_session_args())

        # Create a Textract client with additional configuration if needed
        self.client = session.client('textract', **config.get_client_args())
        logging.info(f'Initialized Textract client in region {config.region}')

    def start_job(self, s3_bucket_name, object_name):
        """
        Start an asynchronous text detection job for a document in S3.

        Args:
            s3_bucket_name: Name of the S3 bucket containing the document
            object_name: Object key of the document in the S3 bucket

        Returns:
            str: The JobId of the started Textract job

        Raises:
            Exception: If there is an error starting the job
        """
        try:
            response = self.client.start_document_text_detection(
                DocumentLocation={
                    'S3Object': {'Bucket': s3_bucket_name, 'Name': object_name}
                }
            )
            job_id = response['JobId']
            logging.info(
                f'Started Textract job {job_id} for {s3_bucket_name}/{object_name}'
            )
            return job_id
        except Exception as e:
            logging.error(
                f'Error starting Textract job for {s3_bucket_name}/{object_name}: {str(e)}'
            )
            raise

    def get_job_status(self, job_id):
        """
        Get the status of a Textract job.

        Args:
            job_id: ID of the Textract job

        Returns:
            str: The job status (e.g., 'IN_PROGRESS', 'SUCCEEDED', 'FAILED')
        """
        try:
            response = self.client.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']
            logging.info(f'Textract job {job_id} status: {status}')
            return status
        except Exception as e:
            logging.error(
                f'Error getting status for Textract job {job_id}: {str(e)}'
            )
            raise

    def is_job_complete(self, job_id):
        """
        Check if a Textract job has completed.

        Args:
            job_id: ID of the Textract job

        Returns:
            str: The job status
        """
        time.sleep(1)  # Avoid rate limiting
        return self.get_job_status(job_id)

    def get_job_results(self, job_id):
        """
        Get the results of a completed Textract job.

        This method handles pagination of results automatically.

        Args:
            job_id: ID of the Textract job

        Returns:
            list: List of response pages from Textract
        """
        pages = []
        next_token = None

        try:
            # Get first page
            response = self.client.get_document_text_detection(JobId=job_id)
            pages.append(response)
            logging.info(f'Received page 1 of results for job {job_id}')

            # Get next token if available
            if 'NextToken' in response:
                next_token = response['NextToken']

            # Get additional pages if available
            page_num = 2
            while next_token:
                time.sleep(1)  # Avoid rate limiting
                response = self.client.get_document_text_detection(
                    JobId=job_id, NextToken=next_token
                )
                pages.append(response)
                logging.info(
                    f'Received page {page_num} of results for job {job_id}'
                )
                page_num += 1

                next_token = response.get('NextToken')

            return pages
        except Exception as e:
            logging.error(
                f'Error getting results for Textract job {job_id}: {str(e)}'
            )
            raise

    def get_full_text(self, response):
        """
        Extract the full text from Textract response pages.

        Args:
            response: List of response pages from Textract

        Returns:
            str: The full extracted text as a string
        """
        try:
            text_lines = []
            for result_page in response:
                for item in result_page.get('Blocks', []):
                    if item.get('BlockType') == 'LINE':
                        text_lines.append(item.get('Text', ''))

            full_text = ' '.join(text_lines)
            return full_text
        except Exception as e:
            logging.error(
                f'Error extracting full text from Textract response: {str(e)}'
            )
            return ''

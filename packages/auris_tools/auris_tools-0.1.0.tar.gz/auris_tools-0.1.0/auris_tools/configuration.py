import logging
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AWSConfiguration:
    """
    AWS Configuration class that handles credentials and region settings.
    Prioritizes environment variables over constructor parameters.
    """

    def __init__(
        self,
        access_key: str = None,
        secret_key: str = None,
        region: str = None,
        profile: str = None,
        endpoint_url: str = None,
    ):
        # Try to get credentials from environment variables first
        self.access_key = (
            access_key if access_key else os.environ.get('AWS_ACCESS_KEY_ID')
        )
        self.secret_key = (
            secret_key
            if secret_key
            else os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        self.region = (
            region
            if region
            else os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1'
        )
        self.profile = profile if profile else os.environ.get('AWS_PROFILE')
        self.endpoint_url = (
            endpoint_url
            if endpoint_url
            else os.environ.get('AWS_ENDPOINT_URL')
        )

        # Validate configuration
        self._validate_config()

    def _validate_config(self):
        """Validate that we have enough configuration to proceed."""
        if not ((self.access_key and self.secret_key) or self.profile):
            logging.warning(
                'No AWS credentials provided via environment variables or constructor. '
                'AWS operations may fail unless credentials are configured via '
                '~/.aws/credentials, IAM roles, or other AWS credential providers.'
            )

    def get_boto3_session_args(self):
        """
        Return a dictionary of arguments that can be passed to boto3.session.Session()
        """
        session_args = {'region_name': self.region}

        if self.access_key and self.secret_key:
            session_args['aws_access_key_id'] = self.access_key
            session_args['aws_secret_access_key'] = self.secret_key

        if self.profile:
            session_args['profile_name'] = self.profile

        return session_args

    def get_client_args(self):
        """
        Return a dictionary of arguments that can be passed to boto3 client creation
        """
        client_args = {}

        if self.endpoint_url:
            client_args['endpoint_url'] = self.endpoint_url

        return client_args

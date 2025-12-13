import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class GoogleGeminiHandler:
    """A handler class for interacting with Google's Gemini AI models.

    This class provides a convenient interface for generating content using Google's
    Gemini generative AI models. It handles authentication, model configuration,
    and content generation with automatic error handling and logging.

    Attributes:
        api_key (str): The Google AI API key used for authentication.
        model_name (str): The name of the Gemini model to use.
        temperature (float): Controls randomness in generation (0.0 to 1.0).
        response_schema (dict): Optional schema for structured responses.
        response_mime_type (str): MIME type for response format.
        generation_config (genai.types.GenerationConfig): Configuration for content generation.
        model (genai.GenerativeModel): The configured Gemini model instance.

    Example:
        Basic usage with environment variable API key:

        >>> handler = GoogleGeminiHandler()
        >>> response = handler.generate_output("What is artificial intelligence?")
        >>> text = handler.get_text(response)

        Usage with custom parameters:

        >>> handler = GoogleGeminiHandler(
        ...     api_key="your-api-key",
        ...     model="gemini-2.0-flash-exp",
        ...     temperature=0.7,
        ...     response_mime_type="text/plain"
        ... )
    """

    def __init__(
        self, api_key: str = None, model: str = 'gemini-2.5-flash', **kwargs
    ):
        """Initialize the Google Gemini handler.

        Args:
            api_key (str, optional): Google AI API key. If not provided, will attempt
                to load from GEMINI_API_KEY environment variable. Defaults to None.
            model (str, optional): Name of the Gemini model to use.
                Defaults to 'gemini-2.5-flash'.
            **kwargs: Additional configuration parameters:
                - temperature (float): Controls randomness (0.0-1.0). Defaults to 0.5.
                - response_schema (dict): Schema for structured responses. Defaults to None.
                - response_mime_type (str): Response MIME type. Defaults to 'application/json'.

        Raises:
            TypeError: If the specified model is not available.

        Example:
            >>> handler = GoogleGeminiHandler(
            ...     api_key="your-api-key",
            ...     model="gemini-2.0-flash-exp",
            ...     temperature=0.7
            ... )
        """

        self.api_key = api_key if api_key else os.getenv('GEMINI_API_KEY')
        if self.api_key is None:
            logger.error(
                'Gemini API key not configured. Please, define the GEMINI_API_KEY environment variable or enter your key directly in the code.'
            )

        self.model_name = model
        self._check_model_availability()

        # More configuration from input parameters
        self.temperature = kwargs.get('temperature', 0.5)
        self.response_schema = kwargs.get('response_schema', None)
        self.response_mime_type = kwargs.get(
            'response_mime_type', 'application/json'
        )

        self.generation_config = genai.types.GenerationConfig(
            temperature=self.temperature,
            response_schema=self.response_schema,
            response_mime_type=self.response_mime_type,
        )

        self.model = genai.GenerativeModel(
            generation_config=self.generation_config,
            model_name=self.model_name,
        )

    def generate_output(
        self, prompt: str, input_data: str = None, input_mime_type: str = None
    ):
        """Generate content using the configured Gemini model.

        This method sends a prompt to the Gemini model and returns the generated response.
        It supports both text-only prompts and multimodal inputs with additional data.

        Args:
            prompt (str): The text prompt to send to the model. This is the main
                instruction or question for the AI to respond to.
            input_data (str, optional): Additional input data to include with the prompt.
                This could be text content, encoded media, or other data. Requires
                input_mime_type to be specified. Defaults to None.
            input_mime_type (str, optional): MIME type of the input_data. Required if
                input_data is provided. Examples: 'text/plain', 'image/jpeg',
                'application/pdf'. Defaults to None.

        Returns:
            genai.types.GenerateContentResponse or str: The response from the Gemini model
            if successful, or an empty string if an error occurred.

        Raises:
            ValueError: If input_data is provided without input_mime_type or vice versa.

        Example:
            Text-only generation:

            >>> response = handler.generate_output("Explain quantum computing")

            Multimodal generation with additional data:

            >>> response = handler.generate_output(
            ...     prompt="Describe this image",
            ...     input_data=base64_encoded_image,
            ...     input_mime_type="image/jpeg"
            ... )
        """
        if (input_data is not None and input_mime_type is None) or (
            input_data is None and input_mime_type is not None
        ):
            raise ValueError(
                'input_mime_type must be provided if input_data is given, or otherwise both must be None.'
            )

        if input_data and input_mime_type:  # Add input data if provided
            prompt = [
                prompt,
                {'mime_type': input_mime_type, 'content': input_data},
            ]

        try:
            response = self.model.generate_content(prompt)
            return response
        except Exception as e:
            logger.error(f'Error generating LLM output: {str(e)}')
            return ''

    def get_text(self, response) -> str:
        """Extract text content from a Gemini model response.

        This method parses the response object returned by the Gemini model and
        extracts the generated text content. It handles the response structure
        safely and provides fallbacks for various response formats.

        Args:
            response (genai.types.GenerateContentResponse or dict): The response object
                returned from the generate_output method. This can be either a
                GenerateContentResponse object or a dictionary representation.

        Returns:
            str: The extracted text content from the response. Returns an empty
            string if no content is found or if an error occurs during extraction.

        Example:
            >>> response = handler.generate_output("What is AI?")
            >>> text_content = handler.get_text(response)
            >>> print(text_content)
            "Artificial Intelligence (AI) refers to..."

            >>> # Handle case with no candidates
            >>> empty_response = {'candidates': []}
            >>> text = handler.get_text(empty_response)
            >>> print(text)  # Returns empty string
            ""
        """
        try:
            if 'candidates' in response and len(response['candidates']) > 0:
                return response['candidates'][0]['content']
            else:
                logger.warning('No candidates found in the response.')
                return ''
        except Exception as e:
            logger.error(f'Error extracting text from response: {str(e)}')
            return ''

    def _check_model_availability(self):
        """Check if the specified Gemini model is available.

        This private method validates that the requested model name exists in the
        list of available Google Gemini models. It queries the Google AI API to
        get the current list of available models and compares against the requested
        model name.

        Raises:
            TypeError: If the specified model is not found in the list of available
                models from the Google AI API.

        Note:
            This method is called automatically during initialization and will
            prevent the handler from being created if an invalid model is specified.
            It also logs the availability check results for debugging purposes.

        Example:
            This method is called internally during initialization:

            >>> # This will call _check_model_availability internally
            >>> handler = GoogleGeminiHandler(model="gemini-2.5-flash")  # Success
            >>> handler = GoogleGeminiHandler(model="invalid-model")     # Raises TypeError
        """
        try:
            genai.configure(api_key=self.api_key)
            available_models = genai.list_models()
            # Extract model names and handle the 'models/' prefix
            available_model_names = []
            for model in available_models:
                model_name = model.name
                # Remove 'models/' prefix if present
                if model_name.startswith('models/'):
                    model_name = model_name[7:]  # Remove 'models/' prefix
                available_model_names.append(model_name)

            if self.model_name not in available_model_names:
                logger.error(
                    f'Model {self.model_name} is not available. Please check the model name.'
                )
                logger.info(
                    f'Available models: {", ".join(available_model_names)}'
                )
                raise TypeError(f'Invalid model name: {self.model_name}')
            else:
                logger.info(f'Model {self.model_name} is available.')
        except Exception as e:
            if 'Invalid model name' in str(e):
                raise  # Re-raise our custom error
            else:
                logger.error(f'Error checking model availability: {str(e)}')
                # Don't raise error for API connectivity issues, just log

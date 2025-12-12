"""Client for assistant operations (similar to Pinecone Assistant)."""

import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Union, Dict, Any

try:
    import backoff
except ImportError:
    backoff = None

from ..models import Message, Namespace, File, FileListResponse
from ..http_client import HTTPClient
from ..utils.s3 import download_files_from_s3_folder

# Set up logger for this module
logger = logging.getLogger(__name__)


class AssistantInstance:
    """
    Client for managing a specific assistant (namespace).
    
    Similar to PineconeAssistant, this class provides methods to interact
    with a specific assistant, including generating responses, managing files,
    and uploading files from S3.
    """

    def __init__(self, assistant_name: str, http_client: HTTPClient):
        """
        Initialize the Assistant client.

        Args:
            assistant_name: Name of the assistant (namespace)
            http_client: HTTP client for making requests
        """
        self.assistant_name = assistant_name
        self._http = http_client
        self._namespace = None
        self._chat = None
        self._files = None
        logger.debug(f"Initialized AssistantInstance for '{assistant_name}'")

    @property
    def name(self) -> str:
        """Get the assistant name."""
        return self.assistant_name

    def chat(
        self,
        messages: List[Union[Message, Dict[str, str]]],
        model: str = "claude-sonnet-4-20250514",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Chat with the assistant.

        Args:
            messages: List of messages (Message objects or dicts)
            model: Model to use for generation (default: gpt-3.5-turbo)
            **kwargs: Additional arguments passed to chat client

        Returns:
            Dict with structure: {'message': {'content': ...}}

        Raises:
            NotFoundError: If assistant not found
            AuthenticationError: If authentication fails
            BadRequestError: If request parameters are invalid
        """
        chat_client = self._get_chat_client()
        response = chat_client.create(
            namespace=self.assistant_name,
            messages=messages,
            model=model,
            **kwargs,
        )
        # Return in the format: {'message': {'content': ...}}
        return {
            'message': {
                'content': response.content if isinstance(response.content, str) else str(response.content)
            }
        }

    def namespace(self) -> Namespace:
        """Get the namespace object for this assistant."""
        logger.debug(f"Getting namespace for assistant '{self.assistant_name}'")
        if self._namespace is None:
            # Try to get the namespace
            logger.debug(f"Namespace not cached, fetching from API")
            namespaces_response = self._http.get("/api/v1/namespaces")
            if isinstance(namespaces_response, list):
                logger.debug(f"Found {len(namespaces_response)} namespaces in response")
                for ns_data in namespaces_response:
                    ns = Namespace.from_dict(ns_data)
                    if ns.name == self.assistant_name:
                        self._namespace = ns
                        logger.info(f"Found namespace '{self.assistant_name}' with ID: {ns.id}")
                        break
            if self._namespace is None:
                logger.error(f"Assistant '{self.assistant_name}' not found in namespaces")
                raise ValueError(f"Assistant '{self.assistant_name}' not found")
        else:
            logger.debug(f"Using cached namespace for '{self.assistant_name}'")
        return self._namespace

    def _get_chat_client(self):
        """Get or create the chat client."""
        if self._chat is None:
            logger.debug("Creating new ChatClient instance")
            from .chat import ChatClient
            self._chat = ChatClient(self._http)
        return self._chat

    def _get_files_client(self):
        """Get or create the files client."""
        if self._files is None:
            logger.debug("Creating new FilesClient instance")
            from .files import FilesClient
            self._files = FilesClient(self._http)
        return self._files

    def generate_response(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        max_retries: int = 3,
    ) -> str:
        """
        Generate a response from the assistant.

        Args:
            prompt: User prompt/question
            model: Model to use for generation (default: gpt-3.5-turbo)
            max_retries: Maximum number of retries on failure (default: 3)

        Returns:
            Response content as a string

        Raises:
            NotFoundError: If assistant not found
            AuthenticationError: If authentication fails
            BadRequestError: If request parameters are invalid
        """
        logger.info(
            f"Generating response for assistant '{self.assistant_name}' "
            f"with model '{model}' (max_retries={max_retries})"
        )
        logger.debug(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
        
        message = Message(role="user", content=prompt)

        # Use backoff if available, otherwise retry manually
        if backoff is not None:
            logger.debug("Using backoff library for retries")
            @backoff.on_exception(backoff.expo, Exception, max_tries=max_retries)
            def _generate():
                logger.debug(f"Attempting to generate response (backoff retry)")
                res = self.chat(messages=[message], model=model)
                content = res['message']['content']
                logger.info(f"Successfully generated response (length: {len(content)} chars)")
                return content

            try:
                result = _generate()
                return result
            except Exception as e:
                logger.error(
                    f"Failed to generate response after {max_retries} retries: {str(e)}",
                    exc_info=True
                )
                raise
        else:
            # Manual retry logic
            logger.debug("Using manual retry logic (backoff not available)")
            last_exception = None
            for attempt in range(max_retries):
                try:
                    logger.debug(f"Generation attempt {attempt + 1}/{max_retries}")
                    res = self.chat(messages=[message], model=model)
                    content = res['message']['content']
                    logger.info(
                        f"Successfully generated response on attempt {attempt + 1} "
                        f"(length: {len(content)} chars)"
                    )
                    return content
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Generation attempt {attempt + 1} failed: {str(e)}"
                    )
                    if attempt < max_retries - 1:
                        sleep_time = 2 ** attempt
                        logger.debug(f"Waiting {sleep_time}s before retry (exponential backoff)")
                        time.sleep(sleep_time)
                    continue
            logger.error(
                f"Failed to generate response after {max_retries} attempts: {str(last_exception)}",
                exc_info=True
            )
            raise last_exception

    def list_files(self, limit: int = 50, skip: int = 0) -> FileListResponse:
        """
        List files in the assistant.

        Args:
            limit: Maximum number of files to return
            skip: Number of files to skip (for pagination)

        Returns:
            FileListResponse with files and pagination info

        Raises:
            NotFoundError: If assistant not found
            AuthenticationError: If authentication fails
        """
        logger.info(
            f"Listing files for assistant '{self.assistant_name}' "
            f"(limit={limit}, skip={skip})"
        )
        files_client = self._get_files_client()
        try:
            result = files_client.list_by_namespace(
                namespace=self.assistant_name,
                limit=limit,
                skip=skip,
            )
            logger.info(
                f"Found {len(result.files)} files (total: {result.total}) "
                f"for assistant '{self.assistant_name}'"
            )
            return result
        except Exception as e:
            logger.error(
                f"Failed to list files for assistant '{self.assistant_name}': {str(e)}",
                exc_info=True
            )
            raise

    def upload_s3_folder(
        self,
        bucket_name: str,
        folder_path: str,
        exclude: Optional[List[str]] = None,
        max_workers: int = 10,
        rate_limit_delay: float = 5.0,
    ) -> None:
        """
        Upload files from an S3 folder to the assistant.

        This method:
        1. Lists existing files in the assistant
        2. Downloads files from S3 that don't already exist
        3. Uploads them to the assistant in parallel

        Args:
            bucket_name: Name of the S3 bucket
            folder_path: Path to the folder in S3
            exclude: List of filenames to exclude from upload
            max_workers: Maximum number of parallel upload workers
            rate_limit_delay: Delay between uploads in seconds (for rate limiting)

        Raises:
            ImportError: If boto3 is not installed
            Exception: If S3 download or upload fails
        """
        logger.info(
            f"Starting S3 folder upload for assistant '{self.assistant_name}': "
            f"bucket={bucket_name}, folder={folder_path}, "
            f"max_workers={max_workers}, rate_limit_delay={rate_limit_delay}s"
        )
        
        # Get existing files
        logger.debug("Fetching existing files from assistant")
        file_list = self.list_files(limit=1000)  # Get up to 1000 files
        existing_files = [file.file_name for file in file_list.files]
        logger.info(f"Found {len(existing_files)} existing files in assistant")

        # Combine existing files with exclude list
        exclude_list = existing_files.copy()
        if exclude:
            exclude_list.extend(exclude)
            logger.debug(f"Excluding {len(exclude)} additional files from exclude list")
        logger.debug(f"Total files to exclude: {len(exclude_list)}")

        # Download files from S3 (already excludes existing files)
        logger.info(f"Downloading files from S3: s3://{bucket_name}/{folder_path}")
        try:
            downloaded_files = download_files_from_s3_folder(
                bucket_name=bucket_name,
                folder_path=folder_path,
                exclude=exclude_list,
            )
            logger.info(f"Downloaded {len(downloaded_files)} files from S3")
        except Exception as e:
            logger.error(
                f"Failed to download files from S3: {str(e)}",
                exc_info=True
            )
            raise

        if not downloaded_files:
            logger.info("No new files to upload (all files already exist or excluded)")
            return

        files_client = self._get_files_client()

        def upload_file_to_assistant(file_path: str) -> bool:
            """Upload a single file to the assistant."""
            try:
                logger.debug(f"Uploading file: {file_path}")
                files_client.upload(
                    file_path=file_path,
                    namespace=self.assistant_name,
                )
                logger.debug(f"Successfully uploaded: {file_path}")
                time.sleep(rate_limit_delay)  # Rate limiting
                return True
            except Exception as e:
                # Log error with full details
                logger.error(
                    f"Error uploading {file_path}: {str(e)}",
                    exc_info=True
                )
                return False

        # Upload files in parallel
        logger.info(f"Starting parallel upload of {len(downloaded_files)} files")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(upload_file_to_assistant, downloaded_files))
            successful_uploads = sum(1 for result in results if result is True)
            failed_uploads = len(downloaded_files) - successful_uploads
            
            logger.info(
                f"Upload complete: {successful_uploads}/{len(downloaded_files)} files "
                f"uploaded successfully to assistant '{self.assistant_name}'"
            )
            if failed_uploads > 0:
                logger.warning(f"{failed_uploads} files failed to upload")
            
            print(
                f"Successfully uploaded {successful_uploads}/{len(downloaded_files)} "
                f"files to assistant '{self.assistant_name}'"
            )

    def delete_assistant(self) -> None:
        """
        Delete the assistant (namespace) and all files under it.

        This method:
        1. Lists all files in the namespace
        2. Deletes each file
        3. Deletes the namespace

        Raises:
            NotFoundError: If assistant not found
            AuthenticationError: If authentication fails
            ForbiddenError: If user doesn't have permission
        """
        logger.info(f"Deleting assistant '{self.assistant_name}' and all its files")
        # Get namespace ID
        namespace = self.namespace
        if namespace.id is None:
            logger.error(f"Assistant '{self.assistant_name}' has no ID")
            raise ValueError(f"Assistant '{self.assistant_name}' has no ID")

        # Delete all files in the namespace
        files_client = self._get_files_client()
        deleted_files = 0
        failed_files = 0
        
        try:
            # List all files with pagination
            skip = 0
            limit = 100  # Process in batches
            total_files = 0
            
            while True:
                logger.debug(f"Listing files for assistant '{self.assistant_name}' (skip={skip}, limit={limit})")
                file_list = self.list_files(limit=limit, skip=skip)
                
                if not file_list.files:
                    break
                
                total_files = file_list.total
                logger.info(f"Found {len(file_list.files)} files to delete (total: {total_files})")
                
                # Delete each file
                for file in file_list.files:
                    if file.id is None:
                        logger.warning(f"File '{file.file_name}' has no ID, skipping")
                        failed_files += 1
                        continue
                    
                    try:
                        logger.debug(f"Deleting file '{file.file_name}' (ID: {file.id})")
                        files_client.delete(file.id)
                        deleted_files += 1
                        logger.debug(f"Successfully deleted file '{file.file_name}'")
                    except Exception as e:
                        logger.warning(
                            f"Failed to delete file '{file.file_name}' (ID: {file.id}): {str(e)}"
                        )
                        failed_files += 1
                        # Continue with other files even if one fails
                        continue
                
                # Check if there are more files to process
                skip += limit
                if skip >= total_files:
                    break
            
            if total_files > 0:
                logger.info(
                    f"File deletion complete: {deleted_files}/{total_files} files deleted "
                    f"({failed_files} failed) for assistant '{self.assistant_name}'"
                )
            else:
                logger.info(f"No files found in assistant '{self.assistant_name}'")
        
        except Exception as e:
            logger.warning(
                f"Error while deleting files for assistant '{self.assistant_name}': {str(e)}. "
                f"Continuing with namespace deletion."
            )
            # Continue with namespace deletion even if file deletion fails

        # Delete the namespace
        logger.debug(f"Deleting namespace with ID: {namespace.id}")
        try:
            from .namespaces import NamespacesClient
            namespaces_client = NamespacesClient(self._http)
            namespaces_client.delete(namespace.id)
            logger.info(
                f"Successfully deleted assistant '{self.assistant_name}' "
                f"(deleted {deleted_files} files)"
            )
        except Exception as e:
            logger.error(
                f"Failed to delete assistant '{self.assistant_name}': {str(e)}",
                exc_info=True
            )
            raise


class Assistant:
    """
    Factory class for managing assistants (similar to Pinecone's assistant pattern).
    
    This class provides:
    - Factory methods: create_assistant()
    - Callable interface: assistant("name") returns AssistantInstance
    - Class attribute: Assistant.Assistant can be instantiated directly
    
    Example:
        >>> client = GushworkRAG(api_key="key")
        >>> # Create an assistant
        >>> client.assistant.create_assistant("my-assistant", "instructions")
        >>> # Get an assistant instance (callable)
        >>> assistant = client.assistant("my-assistant")
        >>> # Or use the class attribute (Pinecone-like pattern)
        >>> assistant = client.assistant.Assistant("my-assistant")
    """
    
    # Expose AssistantInstance as a class attribute for Pinecone-like pattern
    Assistant = AssistantInstance
    
    def __init__(self, http_client: HTTPClient):
        """
        Initialize the Assistant factory.

        Args:
            http_client: HTTP client for making requests
        """
        self._http = http_client
        logger.debug("Initialized Assistant factory")
    
    def create_assistant(
        self,
        assistant_name: str,
        instructions: str = "",
        timeout: Optional[int] = 30,
    ) -> Namespace:
        """
        Create a new assistant (namespace).

        Args:
            assistant_name: Name of the assistant
            instructions: Instructions for the assistant
            timeout: Request timeout in seconds (not used in current implementation)

        Returns:
            Created Namespace object representing the assistant

        Raises:
            BadRequestError: If assistant already exists
            AuthenticationError: If authentication fails
            ForbiddenError: If user doesn't have permission
        """
        logger.info(
            f"Creating assistant '{assistant_name}' "
            f"(instructions length: {len(instructions)} chars)"
        )
        logger.debug(f"Instructions: {instructions[:200]}{'...' if len(instructions) > 200 else ''}")
        
        data = {"name": assistant_name, "instructions": instructions}
        try:
            response = self._http.post("/api/v1/namespaces", data)
            namespace = Namespace.from_dict(response.get("namespace", {}))
            logger.info(
                f"Successfully created assistant '{assistant_name}' "
                f"with ID: {namespace.id}"
            )
            return namespace
        except Exception as e:
            logger.error(
                f"Failed to create assistant '{assistant_name}': {str(e)}",
                exc_info=True
            )
            raise

    
    def __call__(self, assistant_name: str) -> AssistantInstance:
        """
        Get an AssistantInstance for a specific assistant name.
        
        This allows the pattern: client.assistant("assistant-name")
        
        Args:
            assistant_name: Name of the assistant
            
        Returns:
            AssistantInstance for the specified assistant
        """
        logger.debug(f"Creating AssistantInstance for '{assistant_name}' via __call__")
        return AssistantInstance(assistant_name=assistant_name, http_client=self._http)

    



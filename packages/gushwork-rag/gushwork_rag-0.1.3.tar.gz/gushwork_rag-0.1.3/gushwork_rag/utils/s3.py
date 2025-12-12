"""S3 utility functions for downloading files."""

import os
import tempfile
from typing import List, Optional

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError:
    boto3 = None
    ClientError = None
    NoCredentialsError = None


def download_files_from_s3_folder(
    bucket_name: str,
    folder_path: str,
    exclude: Optional[List[str]] = None,
    local_path: Optional[str] = None,
) -> List[str]:
    """
    Download all files from an S3 folder to a local directory.

    Args:
        bucket_name: Name of the S3 bucket
        folder_path: Path to the folder in S3 (without leading/trailing slashes)
        exclude: List of filenames to exclude from download
        local_path: Local directory to save files (defaults to temp directory)

    Returns:
        List of local file paths for downloaded files

    Raises:
        ImportError: If boto3 is not installed
        Exception: If download fails or AWS credentials are missing
    """
    if boto3 is None:
        raise ImportError(
            "boto3 is required for S3 operations. Install it with: pip install boto3"
        )

    if exclude is None:
        exclude = []

    if local_path is None:
        local_path = tempfile.mkdtemp()

    os.makedirs(local_path, exist_ok=True)

    s3_client = boto3.client("s3")
    downloaded_files = []

    try:
        # List all objects in the folder
        prefix = folder_path.rstrip("/") + "/"
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in pages:
            if "Contents" not in page:
                continue

            for obj in page["Contents"]:
                if obj["Key"].endswith("/"):
                    continue

                # Get the filename
                filename = os.path.basename(obj["Key"])

                # Skip if in exclude list
                if filename in exclude:
                    continue

                # Download the file
                local_file_path = os.path.join(local_path, filename)
                try:
                    s3_client.download_file(bucket_name, obj["Key"], local_file_path)
                    downloaded_files.append(local_file_path)
                except ClientError as e:
                    raise Exception(f"Failed to download {obj['Key']}: {str(e)}")

    except NoCredentialsError:
        raise Exception("AWS credentials not found. Please configure AWS credentials.")
    except ClientError as e:
        raise Exception(f"Failed to list objects in S3: {str(e)}")

    return downloaded_files


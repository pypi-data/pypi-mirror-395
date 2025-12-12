"""
Google Cloud utility classes for C1G projects.

Provides clients for:
- Secret Manager
- Google Sheets
- Cloud Storage
- Google Drive
- Google Docs
"""

from io import BytesIO
from typing import Any

from google.cloud import secretmanager, storage
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload


class SecretManagerClient:
    """
    Client for Google Cloud Secret Manager.

    Args:
        project_id: GCP project ID.

    Example:
        >>> from c1gpy.google_utils import SecretManagerClient
        >>> client = SecretManagerClient("my-project")
        >>> api_key = client.get_secret("api-key")
        >>> db_password = client.get_secret("db-password", version="2")
    """

    def __init__(self, project_id: str) -> None:
        self._project_id = project_id
        self._client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str, version: str = "latest") -> str:
        """
        Retrieve a secret value from Secret Manager.

        Args:
            secret_id: The secret ID.
            version: Secret version (default: "latest").

        Returns:
            The secret value as a string.
        """
        name = f"projects/{self._project_id}/secrets/{secret_id}/versions/{version}"
        response = self._client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def list_secrets(self) -> list[str]:
        """List all secret IDs in the project."""
        parent = f"projects/{self._project_id}"
        secrets = self._client.list_secrets(request={"parent": parent})
        return [secret.name.split("/")[-1] for secret in secrets]

    def create_secret(self, secret_id: str, secret_value: str) -> None:
        """
        Create a new secret with an initial version.

        Args:
            secret_id: The secret ID to create.
            secret_value: The secret value.
        """
        parent = f"projects/{self._project_id}"
        self._client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        self.add_secret_version(secret_id, secret_value)

    def add_secret_version(self, secret_id: str, secret_value: str) -> str:
        """
        Add a new version to an existing secret.

        Args:
            secret_id: The secret ID.
            secret_value: The new secret value.

        Returns:
            The new version name.
        """
        parent = f"projects/{self._project_id}/secrets/{secret_id}"
        response = self._client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": secret_value.encode("UTF-8")},
            }
        )
        return response.name


class GoogleSheetsClient:
    """
    Client for Google Sheets API.

    Args:
        credentials_path: Path to service account JSON file.
            If None, uses Application Default Credentials.

    Example:
        >>> from c1gpy.google_utils import GoogleSheetsClient
        >>> client = GoogleSheetsClient("service-account.json")
        >>> data = client.read_sheet("spreadsheet_id", "Sheet1!A1:D10")
        >>> client.write_sheet("spreadsheet_id", "Sheet1!A1", [["Name", "Age"], ["Alice", 30]])
    """

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, credentials_path: str | None = None) -> None:
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=self.SCOPES
            )
        else:
            credentials = None
        self._service = build("sheets", "v4", credentials=credentials)

    def read_sheet(self, spreadsheet_id: str, range_name: str) -> list[list[Any]]:
        """
        Read data from a Google Sheet.

        Args:
            spreadsheet_id: The spreadsheet ID.
            range_name: The A1 notation range (e.g., "Sheet1!A1:D10").

        Returns:
            List of rows, each row is a list of cell values.
        """
        result = (
            self._service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        return result.get("values", [])

    def write_sheet(
        self,
        spreadsheet_id: str,
        range_name: str,
        values: list[list[Any]],
        value_input_option: str = "USER_ENTERED",
    ) -> dict[str, Any]:
        """
        Write data to a Google Sheet.

        Args:
            spreadsheet_id: The spreadsheet ID.
            range_name: The A1 notation range (e.g., "Sheet1!A1").
            values: List of rows to write.
            value_input_option: How to interpret input ("RAW" or "USER_ENTERED").

        Returns:
            API response dict.
        """
        body = {"values": values}
        return (
            self._service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )

    def append_sheet(
        self,
        spreadsheet_id: str,
        range_name: str,
        values: list[list[Any]],
        value_input_option: str = "USER_ENTERED",
    ) -> dict[str, Any]:
        """
        Append data to a Google Sheet.

        Args:
            spreadsheet_id: The spreadsheet ID.
            range_name: The A1 notation range (e.g., "Sheet1!A1").
            values: List of rows to append.
            value_input_option: How to interpret input ("RAW" or "USER_ENTERED").

        Returns:
            API response dict.
        """
        body = {"values": values}
        return (
            self._service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )

    def clear_sheet(self, spreadsheet_id: str, range_name: str) -> dict[str, Any]:
        """Clear a range in a Google Sheet."""
        return (
            self._service.spreadsheets()
            .values()
            .clear(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )


class CloudStorageClient:
    """
    Client for Google Cloud Storage.

    Args:
        project_id: GCP project ID (optional, uses default if not provided).

    Example:
        >>> from c1gpy.google_utils import CloudStorageClient
        >>> client = CloudStorageClient()
        >>> client.upload_blob("my-bucket", "data.json", '{"key": "value"}')
        >>> content = client.download_blob("my-bucket", "data.json")
        >>> client.upload_file("my-bucket", "image.png", "/path/to/image.png")
    """

    def __init__(self, project_id: str | None = None) -> None:
        self._client = storage.Client(project=project_id)

    def upload_blob(
        self,
        bucket_name: str,
        blob_name: str,
        data: str | bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        """
        Upload data to a blob.

        Args:
            bucket_name: The bucket name.
            blob_name: The blob path/name.
            data: String or bytes to upload.
            content_type: MIME type of the data.

        Returns:
            Public URL of the blob.
        """
        bucket = self._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        if isinstance(data, str):
            blob.upload_from_string(data, content_type=content_type)
        else:
            blob.upload_from_string(data, content_type=content_type)
        return blob.public_url

    def upload_file(
        self,
        bucket_name: str,
        blob_name: str,
        file_path: str,
        content_type: str | None = None,
    ) -> str:
        """
        Upload a file to a blob.

        Args:
            bucket_name: The bucket name.
            blob_name: The blob path/name.
            file_path: Local file path.
            content_type: MIME type (auto-detected if None).

        Returns:
            Public URL of the blob.
        """
        bucket = self._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path, content_type=content_type)
        return blob.public_url

    def download_blob(self, bucket_name: str, blob_name: str) -> bytes:
        """
        Download a blob's content.

        Args:
            bucket_name: The bucket name.
            blob_name: The blob path/name.

        Returns:
            Blob content as bytes.
        """
        bucket = self._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        return blob.download_as_bytes()

    def download_blob_to_file(
        self, bucket_name: str, blob_name: str, file_path: str
    ) -> None:
        """Download a blob to a local file."""
        bucket = self._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.download_to_filename(file_path)

    def delete_blob(self, bucket_name: str, blob_name: str) -> None:
        """Delete a blob."""
        bucket = self._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()

    def list_blobs(self, bucket_name: str, prefix: str | None = None) -> list[str]:
        """
        List blobs in a bucket.

        Args:
            bucket_name: The bucket name.
            prefix: Optional prefix to filter blobs.

        Returns:
            List of blob names.
        """
        bucket = self._client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    def blob_exists(self, bucket_name: str, blob_name: str) -> bool:
        """Check if a blob exists."""
        bucket = self._client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        return blob.exists()


class GoogleDriveClient:
    """
    Client for Google Drive API.

    Args:
        credentials_path: Path to service account JSON file.
            If None, uses Application Default Credentials.

    Example:
        >>> from c1gpy.google_utils import GoogleDriveClient
        >>> client = GoogleDriveClient("service-account.json")
        >>> files = client.list_files()
        >>> content = client.download_file("file_id")
        >>> client.upload_file("/path/to/file.pdf", "document.pdf", folder_id="folder_id")
    """

    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self, credentials_path: str | None = None) -> None:
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=self.SCOPES
            )
        else:
            credentials = None
        self._service = build("drive", "v3", credentials=credentials)

    def list_files(
        self,
        query: str | None = None,
        page_size: int = 100,
        folder_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        List files in Google Drive.

        Args:
            query: Optional Drive API query string.
            page_size: Number of results per page.
            folder_id: Optional folder ID to list files from.

        Returns:
            List of file metadata dicts.
        """
        if folder_id and not query:
            query = f"'{folder_id}' in parents"
        elif folder_id and query:
            query = f"'{folder_id}' in parents and {query}"

        results = (
            self._service.files()
            .list(q=query, pageSize=page_size, fields="files(id, name, mimeType, size)")
            .execute()
        )
        return results.get("files", [])

    def download_file(self, file_id: str) -> bytes:
        """
        Download a file's content.

        Args:
            file_id: The file ID.

        Returns:
            File content as bytes.
        """
        request = self._service.files().get_media(fileId=file_id)
        buffer = BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        return buffer.getvalue()

    def download_file_to_path(self, file_id: str, file_path: str) -> None:
        """Download a file to a local path."""
        content = self.download_file(file_id)
        with open(file_path, "wb") as f:
            f.write(content)

    def upload_file(
        self,
        file_path: str,
        name: str | None = None,
        folder_id: str | None = None,
        mime_type: str | None = None,
    ) -> dict[str, Any]:
        """
        Upload a file to Google Drive.

        Args:
            file_path: Local file path.
            name: File name in Drive (defaults to local filename).
            folder_id: Optional parent folder ID.
            mime_type: MIME type (auto-detected if None).

        Returns:
            File metadata dict with id and name.
        """
        import os

        file_name = name or os.path.basename(file_path)
        file_metadata: dict[str, Any] = {"name": file_name}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        return (
            self._service.files()
            .create(body=file_metadata, media_body=media, fields="id, name")
            .execute()
        )

    def upload_bytes(
        self,
        data: bytes,
        name: str,
        folder_id: str | None = None,
        mime_type: str = "application/octet-stream",
    ) -> dict[str, Any]:
        """
        Upload bytes to Google Drive.

        Args:
            data: Bytes to upload.
            name: File name in Drive.
            folder_id: Optional parent folder ID.
            mime_type: MIME type.

        Returns:
            File metadata dict with id and name.
        """
        file_metadata: dict[str, Any] = {"name": name}
        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = MediaIoBaseUpload(BytesIO(data), mimetype=mime_type, resumable=True)
        return (
            self._service.files()
            .create(body=file_metadata, media_body=media, fields="id, name")
            .execute()
        )

    def delete_file(self, file_id: str) -> None:
        """Delete a file."""
        self._service.files().delete(fileId=file_id).execute()

    def create_folder(
        self, name: str, parent_folder_id: str | None = None
    ) -> dict[str, Any]:
        """
        Create a folder in Google Drive.

        Args:
            name: Folder name.
            parent_folder_id: Optional parent folder ID.

        Returns:
            Folder metadata dict with id and name.
        """
        file_metadata: dict[str, Any] = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_folder_id:
            file_metadata["parents"] = [parent_folder_id]

        return (
            self._service.files()
            .create(body=file_metadata, fields="id, name")
            .execute()
        )


class GoogleDocsClient:
    """
    Client for Google Docs API.

    Args:
        credentials_path: Path to service account JSON file.
            If None, uses Application Default Credentials.

    Example:
        >>> from c1gpy.google_utils import GoogleDocsClient
        >>> client = GoogleDocsClient("service-account.json")
        >>> content = client.get_document_text("document_id")
        >>> client.insert_text("document_id", "Hello, World!", index=1)
    """

    SCOPES = [
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, credentials_path: str | None = None) -> None:
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path, scopes=self.SCOPES
            )
        else:
            credentials = None
        self._service = build("docs", "v1", credentials=credentials)
        self._drive_service = build("drive", "v3", credentials=credentials)

    def get_document(self, document_id: str) -> dict[str, Any]:
        """
        Get full document metadata and content.

        Args:
            document_id: The document ID.

        Returns:
            Document object dict.
        """
        return self._service.documents().get(documentId=document_id).execute()

    def get_document_text(self, document_id: str) -> str:
        """
        Extract plain text from a document.

        Args:
            document_id: The document ID.

        Returns:
            Document text content.
        """
        doc = self.get_document(document_id)
        text_parts = []

        for element in doc.get("body", {}).get("content", []):
            if "paragraph" in element:
                for para_element in element["paragraph"].get("elements", []):
                    if "textRun" in para_element:
                        text_parts.append(para_element["textRun"].get("content", ""))

        return "".join(text_parts)

    def create_document(self, title: str) -> dict[str, Any]:
        """
        Create a new Google Doc.

        Args:
            title: Document title.

        Returns:
            Document metadata dict with documentId and title.
        """
        return self._service.documents().create(body={"title": title}).execute()

    def insert_text(
        self, document_id: str, text: str, index: int = 1
    ) -> dict[str, Any]:
        """
        Insert text at a specific index.

        Args:
            document_id: The document ID.
            text: Text to insert.
            index: Character index (1-based, 1 = start of document).

        Returns:
            API response dict.
        """
        requests = [{"insertText": {"location": {"index": index}, "text": text}}]
        return (
            self._service.documents()
            .batchUpdate(documentId=document_id, body={"requests": requests})
            .execute()
        )

    def replace_text(self, document_id: str, find: str, replace: str) -> dict[str, Any]:
        """
        Replace all occurrences of text in a document.

        Args:
            document_id: The document ID.
            find: Text to find.
            replace: Replacement text.

        Returns:
            API response dict.
        """
        requests = [
            {
                "replaceAllText": {
                    "containsText": {"text": find, "matchCase": True},
                    "replaceText": replace,
                }
            }
        ]
        return (
            self._service.documents()
            .batchUpdate(documentId=document_id, body={"requests": requests})
            .execute()
        )

    def delete_content(
        self, document_id: str, start_index: int, end_index: int
    ) -> dict[str, Any]:
        """
        Delete content in a range.

        Args:
            document_id: The document ID.
            start_index: Start character index.
            end_index: End character index.

        Returns:
            API response dict.
        """
        requests = [
            {
                "deleteContentRange": {
                    "range": {"startIndex": start_index, "endIndex": end_index}
                }
            }
        ]
        return (
            self._service.documents()
            .batchUpdate(documentId=document_id, body={"requests": requests})
            .execute()
        )

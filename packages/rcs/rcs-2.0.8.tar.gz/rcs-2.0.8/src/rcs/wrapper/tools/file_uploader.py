import mimetypes
from pathlib import Path
from typing import Optional
import httpx
from ...tools.file.client import FileClient, AsyncFileClient
from ...tools.file.types.upload_file_options import UploadFileOptions
from ...errors.not_found_error import NotFoundError
from ...errors.bad_request_error import BadRequestError
from ...errors.internal_server_error import InternalServerError
from ...types.error import Error
from ...core.client_wrapper import SyncClientWrapper, AsyncClientWrapper


def _get_mime_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)

    if not mime_type:
        return "application/octet-stream"

    supported_types = {
        "audio/mpeg",
        "audio/mp4",
        "audio/ogg",
        "audio/aac",
        "audio/webm",
        "audio/wav",
        "audio/3gpp",
        "audio/amr",
        "video/mp4",
        "video/mpeg",
        "video/quicktime",
        "video/webm",
        "video/3gpp",
        "video/H264",
        "video/x-m4v",
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/bmp",
        "image/tiff",
        "image/webp",
        "application/pdf",
        "text/csv",
        "application/rtf",
        "text/vcard",
        "text/calendar",
    }

    if mime_type in supported_types:
        return mime_type

    base_type = mime_type.split("/")[0]
    if base_type in ["audio", "video", "image"]:
        print(
            f"WARNING: MIME type {mime_type} may not be fully supported. Proceeding anyway."
        )
        return mime_type

    return "application/octet-stream"


class FileUploader(FileClient):
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)
        self._client_wrapper = client_wrapper

    def upload_from_path(
        self,
        file_path: str,
        *,
        name: Optional[str] = None,
        options: Optional[UploadFileOptions] = None,
    ) -> str:
        path = Path(file_path)

        if not path.exists():
            raise NotFoundError(body=Error(error=f"File not found: {file_path}"))

        if path.is_dir():
            raise BadRequestError(body=f"Path is a directory, not a file: {file_path}")

        try:
            stats = path.stat()
        except Exception as e:
            raise InternalServerError(
                body=Error(error=f"Failed to access file: {str(e)}")
            )

        size = stats.st_size
        file_name = name or path.name
        content_type = _get_mime_type(file_path)

        upload_result = self.upload(
            content_type=content_type,
            size=size,
            name=file_name,
            options=options or UploadFileOptions(),
        )

        if upload_result.upload_url:
            with open(file_path, "rb") as f:
                file_content = f.read()

            with httpx.Client() as client:
                response = client.put(
                    upload_result.upload_url,
                    content=file_content,
                    headers={"Content-Type": content_type},
                )
                response.raise_for_status()

        return upload_result.download_url


class AsyncFileUploader(AsyncFileClient):
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        super().__init__(client_wrapper=client_wrapper)
        self._client_wrapper = client_wrapper

    async def upload_from_path(
        self,
        file_path: str,
        *,
        name: Optional[str] = None,
        options: Optional[UploadFileOptions] = None,
    ) -> str:
        path = Path(file_path)

        if not path.exists():
            raise NotFoundError(body=Error(error=f"File not found: {file_path}"))

        if path.is_dir():
            raise BadRequestError(body=f"Path is a directory, not a file: {file_path}")

        try:
            stats = path.stat()
        except Exception as e:
            raise InternalServerError(
                body=Error(error=f"Failed to access file: {str(e)}")
            )

        size = stats.st_size
        file_name = name or path.name
        content_type = _get_mime_type(file_path)

        upload_result = await self.upload(
            content_type=content_type,
            size=size,
            name=file_name,
            options=options or UploadFileOptions(),
        )

        if upload_result.upload_url:
            with open(file_path, "rb") as f:
                file_content = f.read()

            async with httpx.AsyncClient() as client:
                response = await client.put(
                    upload_result.upload_url,
                    content=file_content,
                    headers={"Content-Type": content_type},
                )
                response.raise_for_status()

        return upload_result.download_url

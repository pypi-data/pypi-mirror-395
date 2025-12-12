from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from pinecone_plugins.assistant.data.core.client.model.inline_response200 import (
    InlineResponse200 as OpenAPIListFilesResponse,
)
from pinecone_plugins.assistant.models.core.dataclass import BaseDataclass
from pinecone_plugins.assistant.models.file_model import FileModel


@dataclass
class Pagination(BaseDataclass):
    next: Optional[str]

    @classmethod
    def from_openapi(
        cls, pagination: Optional[Dict[str, Any]]
    ) -> Optional["Pagination"]:
        if pagination is None:
            return None
        return cls(
            next=pagination.get("next"),
        )

    @classmethod
    def from_dict(cls, d: Optional[Dict[str, Any]]) -> Optional["Pagination"]:
        if d is None:
            return None
        return cls(
            next=d.get("next"),
        )


@dataclass
class ListFilesResponse(BaseDataclass):
    files: List[FileModel]
    pagination: Optional[Pagination]

    @classmethod
    def from_openapi(cls, response: OpenAPIListFilesResponse) -> "ListFilesResponse":
        files = [FileModel.from_openapi(file) for file in response.files]
        pagination = None
        if hasattr(response, "pagination") and response.pagination is not None:
            pagination = Pagination.from_openapi(response.pagination)
        return cls(
            files=files,
            pagination=pagination,
        )

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ListFilesResponse":
        files = [FileModel.from_dict(file) for file in d.get("files", [])]
        pagination = Pagination.from_dict(d.get("pagination"))
        return cls(
            files=files,
            pagination=pagination,
        )

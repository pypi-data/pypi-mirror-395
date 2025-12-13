from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from pathlib import Path


class ReportData(BaseModel):
    """
    Model representing a single entry in a report.
    """
    id: Optional[str] = Field(
        None,
        description="Unique identifier for the report entry",
    )
    name: Optional[str] = Field(
        None,
        description="Name associated with the report entry",
    )
    extension: Optional[str] = Field(
        None,
        description="File extension of the report entry",
    )
    appFileExtension: Optional[str] = Field(
        None,
        description="Application file extension of the report entry",
    )
    processName: Optional[str] = Field(
        None,
        description="Name of the process associated with the report entry",
    )
    routePath: Optional[str] = Field(
        None,
        description="Route path associated with the report entry",
    )
    reportTypes: Optional[list[str]] = Field(
        None,
        description="Types of reports associated with the entry",
    )
    children: Optional[list["ReportData"]] = Field(
        None,
        description="List of child entries associated with the report entry",
    )
    file_path: Optional[str] = Field(
        None,
        description="Injected file path extracted from routePath",
    )
    fileSize: Optional[int] = Field(
        None,
        description="Size of the file in bytes",
    )


ReportData.model_rebuild()


class MultiReportData(BaseModel):
    """
    Model representing the data for multiple reports.
    """
    total: Optional[int] = Field(
        None,
        description="Total number of entries in the report",
    )
    data: list[ReportData] = Field(
        ...,
        description="List of entries in the report data",
    )


class FileUploadRequest(BaseModel):
    """
    Model representing a file upload request to a report.
    """
    local_file_path: str = Field(
        ...,
        description="Path to the local file to upload",
    )
    report_id: str = Field(
        ...,
        description="ID of the report to upload to",
    )
    target_dir: Optional[str] = Field(
        None,
        description="Target directory within the report",
    )

    @field_validator('local_file_path')
    @classmethod
    def validate_file_exists(cls, v):
        """Validate that the file exists"""
        if not Path(v).exists():
            raise ValueError(f"File does not exist: {v}")
        return v


class FileUploadResponse(BaseModel):
    """
    Model representing the response from a file upload operation.
    """
    success: bool = Field(
        ...,
        description="Whether the upload was successful",
    )
    message: str = Field(
        ...,
        description="Response message from the upload operation",
    )
    file_id: Optional[str] = Field(
        None,
        description="ID of the uploaded file if successful",
    )


class ReportDirectory(BaseModel):
    """
    Model representing a directory within a report.
    """
    path: str = Field(
        ...,
        description="The directory path",
    )
    name: str = Field(
        ...,
        description="The directory name",
    )

    @field_validator('name', mode='before')
    @classmethod
    def extract_name_from_path(cls, v, info):
        """Extract directory name from path if not provided"""
        if not v and 'path' in info.data:
            return Path(info.data['path']).name
        return v


class ReportPathsResponse(BaseModel):
    """
    Model representing the response containing all report paths.
    """
    paths: List[str] = Field(
        ...,
        description="List of all unique report paths",
    )
    total_count: int = Field(
        ...,
        description="Total number of unique paths",
    )

    @field_validator('total_count', mode='before')
    @classmethod
    def set_total_count(cls, v, info):
        """Set total count based on paths length if not provided"""
        if v is None and 'paths' in info.data:
            return len(info.data['paths'])
        return v

# redix_client/models.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class BatchStatusResponse(BaseModel):
    job_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    total_files_found: Optional[int]
    files_processed: Optional[int]
    successful_files: Optional[int]
    failed_files: Optional[int]
    summary: Optional[str]
    details: List[Dict[str, Any]]
    error: Optional[str]

class BatchJobSummary(BaseModel):
    job_id: str
    status: str
    profile: str
    input_folder: str
    output_folder: str
    start_time: datetime
    end_time: Optional[datetime]
    total_files_found: int
    files_processed: int
    successful_files: int
    failed_files: int
    error: Optional[str]

class ConversionResponse(BaseModel):
    success: bool
    conversion_id: str
    filename_base: str
    input_file_name: Optional[str]
    input_file_path: Optional[str]
    input_file_view_url: Optional[str]
    output_file_path: Optional[str]
    output_file_view_url: Optional[str]
    error_file_path: Optional[str]
    error_file_view_url: Optional[str]
    ack_file_path: Optional[str]
    ack_file_view_url: Optional[str]
    ta1_file_path: Optional[str]
    ta1_file_view_url: Optional[str]
    archived_file_path: Optional[str]
    archived_file_view_url: Optional[str]
    conversion_result_summary: str
    warnings: List[str]
    processing_time_ms: int

class UploadResponse(BaseModel):
    message: str
    filename: str

class FileDeleteResponse(BaseModel):
    message: str

class FileInfo(BaseModel):
    name: str
    path: str
    is_dir: bool
    size: Optional[int]
    last_modified: str

class FileViewResponse(BaseModel):
    content: str

class BatchLog(BaseModel):
    timestamp: str
    level: str
    message: str

class BatchFileDetail(BaseModel):
    filename: str
    status: str
    success: bool
    summary: str
    warnings: List[str]
    output_url: Optional[str]
    error_url: Optional[str]
    ack_url: Optional[str]
    ta1_url: Optional[str]
    archive_path: Optional[str]

class BatchSummaryResponse(BaseModel):
    total_jobs: int
    total_successful_files: int
    total_failed_files: int
    average_files_processed: float

class StagingProfilesResponse(BaseModel):
    default_profile: Optional[str]
    available_profiles: List[str]
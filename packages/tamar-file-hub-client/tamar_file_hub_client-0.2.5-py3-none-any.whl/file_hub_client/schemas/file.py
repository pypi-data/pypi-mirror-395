"""
文件相关数据模型
"""
from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum


class File(BaseModel):
    """文件信息模型"""
    id: str = Field(..., description="文件ID")
    folder_id: str = Field(..., description="所属文件夹ID")
    file_name: str = Field(..., description="原始文件名")
    file_type: str = Field(..., description="文件类型")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UploadFile(BaseModel):
    """上传文件信息模型"""
    id: str = Field(..., description="上传文件ID")
    folder_id: str = Field(..., description="所属文件夹ID")
    storage_type: str = Field(..., description="存储类型")
    stored_name: str = Field(..., description="存储文件名")
    stored_path: str = Field(..., description="存储路径")
    file_id: str = Field(..., description="所属文件ID")
    file_name: str = Field(..., description="原始文件名")
    file_size: int = Field(0, description="文件大小（字节）")
    file_ext: str = Field(..., description="文件后缀")
    mime_type: str = Field(..., description="MIME类型")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class FileUploadResponse(BaseModel):
    """文件上传返回"""
    file: File = Field(..., description="文件信息")
    upload_file: UploadFile = Field(..., description="上传文件信息")


class UploadUrlResponse(BaseModel):
    """上传URL响应"""
    file: File = Field(..., description="文件信息")
    upload_file: UploadFile = Field(..., description="上传文件信息")
    upload_url: str = Field(..., description="上传URL")


class ShareLinkRequest(BaseModel):
    """生成分享链接请求"""
    file_id: str = Field(..., description="文件ID")
    is_public: bool = Field(True, description="是否公开")
    access_scope: str = Field("view", description="访问范围")
    expire_seconds: int = Field(86400, description="过期时间（秒）")
    max_access: Optional[int] = Field(None, description="最大访问次数")
    password: Optional[str] = Field(None, description="访问密码")


class FileVisitRequest(BaseModel):
    """文件访问请求"""
    file_share_id: str = Field(..., description="分享ID")
    access_type: str = Field(..., description="访问类型")
    access_duration: int = Field(..., description="访问时长")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class FileListRequest(BaseModel):
    """文件列表请求"""
    folder_id: str = Field(..., description="文件夹ID")
    file_name: Optional[str] = Field(None, description="文件名")
    file_type: Optional[List[str]] = Field(None, description="文件类型")
    created_by_role: Optional[str] = Field(None, description="创建者角色")
    created_by: Optional[str] = Field(None, description="创建者")
    page_size: int = Field(20, description="每页大小")
    page: int = Field(1, description="页码")


class FileListResponse(BaseModel):
    """文件列表响应"""
    files: List[File] = Field(default_factory=list, description="文件列表")


class GetFileResponse(BaseModel):
    """获取文件响应"""
    file: File = Field(..., description="文件信息")
    upload_file: Optional[UploadFile] = Field(None, description="上传文件信息")


class DownloadUrlInfo(BaseModel):
    """下载URL信息"""
    file_id: str = Field(..., description="文件ID")
    url: str = Field(..., description="下载URL")
    mime_type: str = Field(..., description="MIME类型")
    error: Optional[str] = Field(None, description="错误信息")


class BatchDownloadUrlResponse(BaseModel):
    """批量下载URL响应"""
    download_urls: List[DownloadUrlInfo] = Field(default_factory=list, description="下载URL列表")


class GcsUrlInfo(BaseModel):
    """GCS URL信息"""
    file_id: str = Field(..., description="文件ID")
    gcs_url: str = Field(..., description="GCS URL")
    mime_type: str = Field(..., description="MIME类型")
    error: Optional[str] = Field(None, description="错误信息")


class GetGcsUrlResponse(BaseModel):
    """获取GCS URL响应"""
    gcs_url: str = Field(..., description="GCS URL")
    mime_type: str = Field(..., description="MIME类型")


class BatchGcsUrlResponse(BaseModel):
    """批量GCS URL响应"""
    gcs_urls: List[GcsUrlInfo] = Field(default_factory=list, description="GCS URL列表")


# ========= 压缩服务相关模型 =========

class CompressedVariant(BaseModel):
    """压缩变体信息"""
    variant_name: str = Field(..., description="变体名称")
    variant_type: str = Field(..., description="变体类型")
    media_type: str = Field(..., description="媒体类型")
    width: int = Field(..., description="宽度")
    height: int = Field(..., description="高度")
    file_size: int = Field(..., description="文件大小")
    format: str = Field(..., description="格式")
    quality: Optional[int] = Field(None, description="质量")
    duration: Optional[float] = Field(None, description="时长")
    bitrate: Optional[int] = Field(None, description="比特率")
    fps: Optional[int] = Field(None, description="帧率")
    compression_ratio: float = Field(..., description="压缩比")
    stored_path: str = Field(..., description="存储路径")


class CompressionStatusResponse(BaseModel):
    """压缩状态响应"""
    status: str = Field(..., description="状态: pending, processing, completed, failed")
    error_message: Optional[str] = Field(None, description="错误信息")
    variants: List[CompressedVariant] = Field(default_factory=list, description="压缩变体列表")


class GetVariantsResponse(BaseModel):
    """获取变体响应"""
    variants: List[CompressedVariant] = Field(default_factory=list, description="压缩变体列表")


class RecompressionResponse(BaseModel):
    """重新压缩响应"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="状态")


class VariantDownloadUrlResponse(BaseModel):
    """变体下载URL响应"""
    url: str = Field(..., description="下载URL")
    error: Optional[str] = Field(None, description="错误信息")
    variant_info: Optional[CompressedVariant] = Field(None, description="变体详细信息")


# ========= 文件状态服务相关模型 =========

class FileUploadStatus(str, Enum):
    """文件上传状态枚举"""
    UPLOAD_UNKNOWN = "UPLOAD_UNKNOWN"
    UPLOAD_PENDING = "UPLOAD_PENDING"
    UPLOAD_PROCESSING = "UPLOAD_PROCESSING"
    UPLOAD_COMPLETED = "UPLOAD_COMPLETED"
    UPLOAD_FAILED = "UPLOAD_FAILED"
    UPLOAD_FILE_NOT_FOUND = "UPLOAD_FILE_NOT_FOUND"


class FileCompressionStatus(str, Enum):
    """文件压缩状态枚举"""
    COMPRESSION_UNKNOWN = "COMPRESSION_UNKNOWN"
    COMPRESSION_NOT_APPLICABLE = "COMPRESSION_NOT_APPLICABLE"
    COMPRESSION_PENDING = "COMPRESSION_PENDING"
    COMPRESSION_PROCESSING = "COMPRESSION_PROCESSING"
    COMPRESSION_COMPLETED = "COMPRESSION_COMPLETED"
    COMPRESSION_FAILED = "COMPRESSION_FAILED"
    COMPRESSION_SKIPPED = "COMPRESSION_SKIPPED"
    COMPRESSION_FILE_NOT_FOUND = "COMPRESSION_FILE_NOT_FOUND"


class FileSyncStatus(str, Enum):
    """文件同步状态枚举"""
    SYNC_UNKNOWN = "SYNC_UNKNOWN"
    SYNC_NOT_REQUIRED = "SYNC_NOT_REQUIRED"
    SYNC_PENDING = "SYNC_PENDING"
    SYNC_PROCESSING = "SYNC_PROCESSING"
    SYNC_PARTIAL = "SYNC_PARTIAL"
    SYNC_COMPLETED = "SYNC_COMPLETED"
    SYNC_FAILED = "SYNC_FAILED"
    SYNC_FILE_NOT_FOUND = "SYNC_FILE_NOT_FOUND"


class FileStatusDetails(BaseModel):
    """文件状态详情"""
    file_size: Optional[int] = Field(None, description="文件大小")
    storage_type: Optional[str] = Field(None, description="存储类型")
    storage_region: Optional[str] = Field(None, description="存储区域")
    compression_task_id: Optional[str] = Field(None, description="压缩任务ID")
    compression_variants_count: Optional[int] = Field(None, description="压缩变体数量")
    compression_progress: Optional[float] = Field(None, description="压缩进度")
    sync_regions_total: Optional[int] = Field(None, description="同步区域总数")
    sync_regions_completed: Optional[int] = Field(None, description="已完成同步区域数")
    sync_pending_regions: List[str] = Field(default_factory=list, description="待同步区域列表")


class FileStatusInfo(BaseModel):
    """文件状态信息"""
    file_id: str = Field(..., description="文件ID")
    upload_status: FileUploadStatus = Field(..., description="上传状态")
    compression_status: FileCompressionStatus = Field(..., description="压缩状态")
    sync_status: FileSyncStatus = Field(..., description="同步状态")
    details: Optional[FileStatusDetails] = Field(None, description="状态详情")
    error_message: Optional[str] = Field(None, description="错误信息")


class BatchFileStatusResponse(BaseModel):
    """批量文件状态响应"""
    statuses: List[FileStatusInfo] = Field(default_factory=list, description="文件状态列表")
    timestamp: int = Field(..., description="查询时间戳")
    cache_hit_count: int = Field(..., description="缓存命中数量（用于性能监控）")


class ImportFromGcsResponse(BaseModel):
    """从GCS导入文件响应"""
    file: File = Field(..., description="创建的文件信息")
    upload_file: UploadFile = Field(..., description="上传文件信息")


class ImageKitTransformations(BaseModel):
    """ImageKit上传时的转换参数"""
    width: Optional[int] = Field(None, description="宽度")
    height: Optional[int] = Field(None, description="高度")
    quality: Optional[int] = Field(None, description="质量 (1-100)")
    format: Optional[str] = Field(None, description="格式 (jpg, png, webp, auto)")
    crop: Optional[str] = Field(None, description="裁剪模式 (maintain_ratio, force, at_least, at_max)")
    progressive: Optional[bool] = Field(None, description="渐进式加载")


class UploadToImageKitResponse(BaseModel):
    """上传到ImageKit响应"""
    file: File = Field(..., description="创建的文件信息")
    upload_file: UploadFile = Field(..., description="上传文件信息")
    imagekit_url: str = Field(..., description="ImageKit访问URL")
    imagekit_file_id: str = Field(..., description="ImageKit文件ID")
    thumbnail_url: Optional[str] = Field(None, description="缩略图URL（如果有）")

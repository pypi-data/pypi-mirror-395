"""
MIME类型到文件扩展名的映射工具
用于从MIME类型推断正确的文件扩展名，特别适用于AI模型生成的文件
"""
from typing import Optional, Dict


class MimeExtensionMapper:
    """MIME类型到文件扩展名的映射器"""
    
    # MIME类型到文件扩展名的映射表
    MIME_TO_EXTENSION: Dict[str, str] = {
        # 图片类型（AI生图常用）
        'image/jpeg': 'jpg',
        'image/jpg': 'jpg', 
        'image/png': 'png',
        'image/gif': 'gif',
        'image/webp': 'webp',
        'image/bmp': 'bmp',
        'image/tiff': 'tiff',
        'image/svg+xml': 'svg',
        'image/x-icon': 'ico',
        
        # 视频类型（AI生视频常用）
        'video/mp4': 'mp4',
        'video/mpeg': 'mpeg',
        'video/quicktime': 'mov',
        'video/x-msvideo': 'avi',
        'video/webm': 'webm',
        'video/x-flv': 'flv',
        'video/3gpp': '3gp',
        
        # 音频类型（AI生音频常用）
        'audio/mpeg': 'mp3',
        'audio/wav': 'wav',
        'audio/x-wav': 'wav',
        'audio/ogg': 'ogg',
        'audio/mp4': 'm4a',
        'audio/aac': 'aac',
        'audio/flac': 'flac',
        'audio/x-ms-wma': 'wma',
        'audio/amr': 'amr',
        'audio/basic': 'au',
        'audio/aiff': 'aiff',
        
        # 文档类型
        'application/pdf': 'pdf',
        'application/msword': 'doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'application/vnd.ms-excel': 'xls',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
        'application/vnd.ms-powerpoint': 'ppt',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
        'application/vnd.ms-office': 'doc',  # MS Office通用格式
        'application/vnd.openxmlformats-officedocument': 'docx',  # Office 2007+通用格式
        
        # 文本类型
        'text/plain': 'txt',
        'text/html': 'html',
        'text/css': 'css',
        'text/javascript': 'js',
        'text/csv': 'csv',
        'application/json': 'json',
        'application/xml': 'xml',
        'text/xml': 'xml',
        
        # 压缩文件类型
        'application/zip': 'zip',
        'application/x-rar-compressed': 'rar',
        'application/vnd.rar': 'rar',
        'application/x-7z-compressed': '7z',
        'application/x-tar': 'tar',
        'application/gzip': 'gz',
        'application/x-bzip2': 'bz2',
        
        # 可执行文件类型
        'application/x-msdownload': 'exe',
        'application/x-executable': 'bin',
        'application/x-mach-binary': 'bin',
        
        # 其他常用类型
        'application/octet-stream': 'dat',  # 通用二进制文件，保持与现有逻辑一致
    }
    
    @classmethod
    def get_extension_from_mime(cls, mime_type: str) -> Optional[str]:
        """
        从MIME类型获取文件扩展名
        
        Args:
            mime_type: MIME类型字符串
            
        Returns:
            文件扩展名（不包含点号），如果无法映射则返回None
        """
        if not mime_type:
            return None
            
        # 清理MIME类型（去除参数部分，如charset等）
        mime_type = mime_type.split(';')[0].strip().lower()
        
        return cls.MIME_TO_EXTENSION.get(mime_type)
    
    @classmethod
    def get_extension_with_fallback(cls, mime_type: str, fallback: str = 'dat') -> str:
        """
        从MIME类型获取文件扩展名，如果无法映射则返回fallback
        
        Args:
            mime_type: MIME类型字符串
            fallback: 默认扩展名，当无法从MIME类型推断时使用
            
        Returns:
            文件扩展名（不包含点号）
        """
        extension = cls.get_extension_from_mime(mime_type)
        return extension if extension is not None else fallback
    
    @classmethod
    def is_supported_mime(cls, mime_type: str) -> bool:
        """
        检查是否支持该MIME类型的映射
        
        Args:
            mime_type: MIME类型字符串
            
        Returns:
            是否支持该MIME类型
        """
        return cls.get_extension_from_mime(mime_type) is not None


# 便捷函数
def get_extension_from_mime_type(mime_type: str) -> Optional[str]:
    """
    从MIME类型获取文件扩展名的便捷函数
    
    Args:
        mime_type: MIME类型字符串
        
    Returns:
        文件扩展名（不包含点号），如果无法映射则返回None
    """
    return MimeExtensionMapper.get_extension_from_mime(mime_type)


def get_extension_from_mime_type_with_fallback(mime_type: str, fallback: str = 'dat') -> str:
    """
    从MIME类型获取文件扩展名的便捷函数，带fallback
    
    Args:
        mime_type: MIME类型字符串
        fallback: 默认扩展名
        
    Returns:
        文件扩展名（不包含点号）
    """
    return MimeExtensionMapper.get_extension_with_fallback(mime_type, fallback)
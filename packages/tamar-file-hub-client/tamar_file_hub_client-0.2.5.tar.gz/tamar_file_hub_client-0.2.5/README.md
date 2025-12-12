# File Hub Client

Python SDK，用于文件中心系统 - 一个支持传统文件、文件夹和电子表格（Taple）的综合文件管理系统。

## 功能特性

- 🚀 **双模式支持**：提供异步（AsyncIO）和同步两种客户端实现
- 📁 **完整的文件管理**：上传、下载、分享、重命名、删除文件
- 📂 **文件夹管理**：创建、重命名、移动、删除分层文件夹结构
- 📊 **Taple电子表格**：类Excel的完整功能，包括工作表、行、列、单元格操作
- 🔄 **多种上传模式**：普通模式、流式模式，根据文件大小自动选择
- 🎯 **智能MIME检测**：26+种文件格式的魔术字节检测和扩展名推断
- 🤖 **AI友好**：完美支持AI模型输出（字节+MIME类型）
- 🔒 **上传保护**：支持GCS和OSS存储后端的禁止覆盖功能
- 🎨 **媒体压缩**：自动生成和管理压缩的图片/视频变体
- 📊 **批量操作**：批量状态查询和批量操作支持
- 🛡️ **健壮的错误处理**：完善的异常体系和自动重试机制
- 📝 **完整类型支持**：完整的类型提示，更好的IDE支持
- 📡 **gRPC日志**：JSON格式的请求/响应日志，可自定义级别
- 🔧 **灵活配置**：支持环境变量和程序化配置

## 安装

```bash
pip install file-hub-client
```

## 快速开始

### 基础设置

```python
from file_hub_client import AsyncFileHubClient, FileHubClient

# 异步客户端
async_client = AsyncFileHubClient(
    host="your-file-hub-server.com",
    port=50051,
    use_tls=True
)

# 同步客户端
client = FileHubClient(
    host="your-file-hub-server.com",
    port=50051,
    use_tls=True
)
```

### 环境变量配置

```bash
# 服务器配置
FILE_HUB_HOST=your-file-hub-server.com
FILE_HUB_PORT=50051
FILE_HUB_USE_TLS=true

# 可选认证头
FILE_HUB_HEADER_X_ORG_ID=your-org-id
FILE_HUB_HEADER_X_USER_ID=your-user-id

# 日志配置
FILE_HUB_LOG_LEVEL=INFO
FILE_HUB_LOG_GRPC_ENABLED=true
FILE_HUB_LOG_REQUEST_PAYLOAD=false
FILE_HUB_LOG_RESPONSE_PAYLOAD=false
```

## 文件操作

### 上传文件

```python
# 简单上传
result = await async_client.blobs.upload(
    file=b"Hello, World!",
    file_name="hello.txt"
)
print(f"文件ID: {result.file.id}")

# 使用文件路径上传
result = await async_client.blobs.upload(
    file="/path/to/local/file.pdf"
)

# 带MIME类型上传（适用于AI生成的内容）
result = await async_client.blobs.upload(
    file=ai_generated_bytes,
    mime_type="image/png",
    file_name="generated.png"
)

# 上传到指定文件夹
result = await async_client.blobs.upload(
    file="/path/to/document.docx",
    folder_id="folder_123"
)

# 大文件流式上传（10MB-100MB）
result = await async_client.blobs.upload(
    file=large_file_path,
    mode=UploadMode.STREAM
)

# 禁止覆盖（防止重复上传）
result = await async_client.blobs.upload(
    file=content,
    forbid_overwrite=True  # 如果文件已存在将失败
)

# 临时文件带过期时间
result = await async_client.blobs.upload(
    file=temp_content,
    is_temporary=True,
    expire_seconds=3600  # 1小时后过期
)
```

### 下载文件

```python
# 下载到文件
await async_client.blobs.download(
    file_id="file_123",
    save_path="/path/to/save/file.pdf"
)

# 下载到字节
file_bytes = await async_client.blobs.download_to_bytes(
    file_id="file_123"
)

# 生成下载URL
url_response = await async_client.blobs.generate_download_url(
    file_id="file_123"
)
download_url = url_response.download_url

# 批量生成下载URL
batch_response = await async_client.blobs.batch_generate_download_url(
    file_ids=["file_1", "file_2", "file_3"]
)
for item in batch_response.items:
    print(f"{item.file_id}: {item.download_url}")
```

### 文件分享

```python
# 生成分享链接
share_response = await async_client.files.generate_share_link(
    file_id="file_123",
    expire_seconds=86400,  # 24小时
    password="secret123",
    max_visit_count=10
)
print(f"分享URL: {share_response.share_url}")

# 访问分享的文件
file_info = await async_client.files.visit_file(
    share_url="https://share.example.com/xxx",
    password="secret123"
)
```

### 文件管理

```python
# 获取文件信息
file_info = await async_client.files.get_file(file_id="file_123")

# 重命名文件
await async_client.files.rename_file(
    file_id="file_123",
    new_name="新名称.pdf"
)

# 删除文件
await async_client.files.delete_file(file_id="file_123")

# 列出文件夹中的文件
files = await async_client.files.list_files(
    folder_id="folder_123",
    page=1,
    page_size=20
)
```

### 压缩和变体

```python
# 获取压缩状态
status = await async_client.blobs.get_compression_status(
    file_id="image_123"
)
print(f"压缩状态: {status.status}")

# 获取压缩变体
variants = await async_client.blobs.get_compressed_variants(
    file_id="image_123"
)
for variant in variants.variants:
    print(f"{variant.spec}: {variant.size} 字节")

# 生成变体下载URL
variant_url = await async_client.blobs.generate_variant_download_url(
    file_id="image_123",
    variant_spec="800x600"
)

# 触发重新压缩
await async_client.blobs.trigger_recompression(
    file_id="image_123",
    variant_specs=["1920x1080", "1280x720", "640x480"]
)
```

### 批量状态查询

```python
# 批量查询文件状态
status_response = await async_client.blobs.batch_get_file_status(
    file_ids=["file_1", "file_2", "file_3"]
)

for status in status_response.statuses:
    print(f"文件 {status.file_id}:")
    print(f"  上传状态: {status.upload_status}")
    print(f"  压缩状态: {status.compression_status}")
    print(f"  同步状态: {status.sync_status}")
```

## 文件夹操作

```python
# 创建文件夹
folder = await async_client.folders.create_folder(
    name="我的文档",
    parent_folder_id="parent_123"  # 可选
)

# 重命名文件夹
await async_client.folders.rename_folder(
    folder_id="folder_123",
    new_name="重要文档"
)

# 移动文件夹
await async_client.folders.move_folder(
    folder_id="folder_123",
    new_parent_folder_id="parent_456"
)

# 删除文件夹
await async_client.folders.delete_folder(
    folder_id="folder_123",
    force=True  # 即使非空也删除
)

# 列出文件夹
folders = await async_client.folders.list_folders(
    parent_folder_id="parent_123",
    page=1,
    page_size=20
)
```

## Taple（电子表格）操作

### 表格管理

```python
# 创建表格
table = await async_client.taples.create_table(
    name="销售报告 2024",
    description="年度销售数据"
)

# 获取表格信息
table_info = await async_client.taples.get_table(
    table_id="table_123"
)

# 更新表格
await async_client.taples.update_table(
    table_id="table_123",
    name="销售报告 2024（更新版）",
    description="包含第四季度更新的年度销售数据"
)

# 删除表格
await async_client.taples.delete_table(
    table_id="table_123"
)
```

### 工作表操作

```python
# 创建工作表
sheet = await async_client.taples.create_sheet(
    table_id="table_123",
    name="第一季度销售",
    position=0
)

# 列出工作表
sheets = await async_client.taples.list_sheets(
    table_id="table_123"
)

# 获取工作表数据
sheet_data = await async_client.taples.get_sheet_data(
    sheet_id="sheet_123"
)

# 更新工作表
await async_client.taples.update_sheet(
    sheet_id="sheet_123",
    name="第一季度销售（修订版）"
)
```

### 列操作

```python
# 创建列
column = await async_client.taples.create_column(
    sheet_id="sheet_123",
    name="产品名称",
    data_type="string",
    position=0,
    width=200
)

# 更新列
await async_client.taples.update_column(
    column_id="col_123",
    name="产品描述",
    width=300
)

# 批量编辑列
await async_client.taples.batch_edit_columns(
    sheet_id="sheet_123",
    operations=[
        {"type": "create", "name": "价格", "data_type": "number"},
        {"type": "create", "name": "数量", "data_type": "integer"},
        {"type": "update", "column_id": "col_123", "width": 150}
    ]
)
```

### 行操作

```python
# 创建行
row = await async_client.taples.create_row(
    sheet_id="sheet_123",
    data={"col_1": "iPhone 15", "col_2": 6999.00, "col_3": 100},
    position=0
)

# 更新行
await async_client.taples.update_row(
    row_id="row_123",
    data={"col_2": 6499.00, "col_3": 150}
)

# 批量编辑行
await async_client.taples.batch_edit_rows(
    sheet_id="sheet_123",
    operations=[
        {"type": "create", "data": {"col_1": "iPad Pro"}},
        {"type": "update", "row_id": "row_123", "data": {"col_3": 200}},
        {"type": "delete", "row_id": "row_456"}
    ]
)
```

### 单元格操作

```python
# 编辑单元格
await async_client.taples.edit_cell(
    sheet_id="sheet_123",
    row_id="row_123",
    column_id="col_456",
    value="新值",
    style={"bold": True, "color": "#FF0000"}
)

# 批量编辑单元格
await async_client.taples.batch_edit_cells(
    sheet_id="sheet_123",
    operations=[
        {
            "row_id": "row_1",
            "column_id": "col_1",
            "value": "已更新",
            "style": {"italic": True}
        },
        {
            "row_id": "row_2",
            "column_id": "col_2",
            "value": 123.45
        }
    ]
)

# 获取单元格数据
cell_data = await async_client.taples.get_cell_data(
    sheet_id="sheet_123",
    row_id="row_123",
    column_id="col_456"
)
```

### 数据导入/导出

```python
# 导出表格数据
export_result = await async_client.taples.export_table_data(
    table_id="table_123",
    format=ExportFormat.XLSX,
    include_styles=True
)
# 使用file_id下载导出的文件
await async_client.blobs.download(
    file_id=export_result.file_id,
    save_path="导出的表格.xlsx"
)

# 从文件导入数据
import_result = await async_client.taples.import_table_data(
    table_id="table_123",
    file_id="file_789",  # Excel/CSV文件
    sheet_id="sheet_123",  # 目标工作表
    mode="append",  # 或 "replace"
    has_header=True
)

# 克隆表格
clone_result = await async_client.taples.clone_table_data(
    source_table_id="table_123",
    target_table_id="table_456",
    mode="override"
)
```

## 同步模式使用

所有操作也都支持同步模式：

```python
from file_hub_client import FileHubClient

# 初始化同步客户端
client = FileHubClient(
    host="your-file-hub-server.com",
    port=50051
)

# 同步上传
result = client.blobs.upload(
    file=b"Hello, 同步世界!",
    file_name="hello_sync.txt"
)

# 同步下载
client.blobs.download(
    file_id="file_123",
    save_path="/path/to/save.pdf"
)

# 同步文件夹操作
folder = client.folders.create_folder(
    name="同步文件夹"
)

# 同步Taple操作
table = client.taples.create_table(
    name="同步表格"
)
```

## 日志配置

```python
from file_hub_client.utils.logging import setup_logging

# 基础设置
setup_logging(
    level="DEBUG",
    enable_grpc_logging=True
)

# 高级设置带自定义处理器
import logging
custom_handler = logging.FileHandler("file_hub.log")

setup_logging(
    level="INFO",
    enable_grpc_logging=True,
    log_request_payload=True,  # 记录请求数据
    log_response_payload=True,  # 记录响应数据
    handler=custom_handler,
    use_json_format=True  # JSON格式日志
)

# 自定义格式的人类可读日志
setup_logging(
    level="DEBUG",
    use_json_format=False,
    format_string="[%(asctime)s] %(levelname)s - %(message)s"
)
```

## 错误处理

```python
from file_hub_client.errors import (
    FileHubError,
    ValidationError,
    NotFoundError,
    PermissionError,
    NetworkError,
    ServerError
)

try:
    result = await async_client.blobs.upload(
        file=content,
        forbid_overwrite=True
    )
except ValidationError as e:
    print(f"输入无效: {e}")
except NotFoundError as e:
    print(f"资源未找到: {e}")
except PermissionError as e:
    print(f"权限拒绝: {e}")
except NetworkError as e:
    print(f"网络问题: {e}")
except ServerError as e:
    print(f"服务器错误: {e}")
except FileHubError as e:
    print(f"一般错误: {e}")
```

## 高级配置

### 自定义元数据

```python
# 向请求添加自定义元数据
result = await async_client.blobs.upload(
    file=content,
    file_name="document.pdf",
    request_id="unique-request-id-123",  # 用于幂等性
    **{
        "x-custom-header": "custom-value",
        "x-trace-id": "trace-123"
    }
)
```

### 连接池设置

```python
# 配置连接池
client = AsyncFileHubClient(
    host="server.com",
    port=50051,
    max_connections=100,
    connection_timeout=30,
    request_timeout=60,
    retry_config={
        "max_attempts": 3,
        "initial_backoff": 1,
        "max_backoff": 30,
        "backoff_multiplier": 2
    }
)
```

### 上传模式选择

SDK根据文件大小自动选择最优上传模式：

- **NORMAL** (< 10MB)：直接gRPC上传
- **STREAM** (10MB - 100MB)：流式上传到云存储
- **STREAM** (> 100MB)：当前使用流式上传（OSS断点续传功能待完成）

您也可以手动指定上传模式：

```python
from file_hub_client.enums import UploadMode

# 强制使用流式模式
result = await async_client.blobs.upload(
    file=small_file,
    mode=UploadMode.STREAM
)
```

## MIME类型检测

SDK使用魔术字节自动检测以下格式的MIME类型：

**图片**：JPEG、PNG、GIF、BMP、WebP、ICO、TIFF、SVG
**视频**：MP4、AVI、MOV、WMV、FLV、WebM、MKV
**文档**：PDF、DOCX、XLSX、PPTX
**压缩包**：ZIP、RAR、7Z、TAR、GZIP
**其他**：MP3、WAV、JSON、XML、HTML

对于AI生成的内容或已知MIME类型的情况：

```python
# 显式设置MIME类型
result = await async_client.blobs.upload(
    file=ai_generated_bytes,
    mime_type="image/png"  # SDK会推断出.png扩展名
)
```

## 存储后端支持

SDK自动处理不同的存储后端：

- **谷歌云存储（GCS）**：自动检测和头部管理
- **阿里云OSS**：自动检测和头部管理
- **自定义S3兼容存储**：可与任何S3兼容存储配合使用

根据上传URL检测的存储类型自动应用禁止覆盖头部。

## 最佳实践

1. **I/O密集型操作使用异步客户端**：异步客户端在处理多个并发操作时更高效。

2. **批量操作**：处理多个文件时使用批量方法，减少网络开销。

3. **错误处理**：始终使用try-except块包装操作，优雅地处理潜在错误。

4. **连接复用**：创建客户端实例一次，在整个应用程序中复用。

5. **日志记录**：开发中启用gRPC日志，但在生产环境中考虑禁用载荷日志以提高性能。

6. **上传保护**：在生产环境中使用`forbid_overwrite=True`防止意外文件覆盖。

7. **请求ID**：为关键操作提供唯一的请求ID以实现幂等性。

## 许可证

MIT许可证

## 支持

有关问题、疑问或贡献，请访问[GitHub仓库](https://github.com/your-org/file-hub-client)。
# Revornix Python Library

[English](./README.md) | [简体中文](./README.zh-CN.md)

Revornix API 的 Python SDK 与 CLI。

📕 API 文档：[revornix/api](https://revornix.com/en/docs/features/api)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Qingyon-AI/Revornix)

## 完整应用

完整的 Revornix 应用在这里：

[Qingyon-AI/Revornix](https://github.com/Qingyon-AI/Revornix)

## 项目简介

- 路线图：[RoadMap](https://huaqinda.notion.site/RoadMap-224bbdbfa03380fabd7beda0b0337ea3)
- 官网：[revornix.com](https://revornix.com)
- 社区：[Discord](https://discord.com/invite/3XZfz84aPN) | [微信](https://github.com/Qingyon-AI/Revornix/discussions/1#discussioncomment-13638435) | [QQ](https://github.com/Qingyon-AI/Revornix/discussions/1#discussioncomment-13638435)

## 安装

从 PyPI 安装：

```shell
pip install revornix
```

本地开发时从源码安装：

```shell
pip install -e .
```

## 认证

Python SDK 和 CLI 都需要以下凭据：

- `base_url`：你的 Revornix API 基础地址
- `api_key`：你的 Revornix API Key

CLI 支持以下环境变量：

```shell
export REVORNIX_BASE_URL="YOUR_API_PREFIX"
export REVORNIX_API_KEY="YOUR_API_KEY"
```

## CLI

安装完成后，可以使用 `revornix` 命令。

查看帮助：

```shell
revornix --help
```

你也可以直接通过参数传入凭据：

```shell
revornix --base-url "YOUR_API_PREFIX" --api-key "YOUR_API_KEY" --help
```

或者使用环境变量：

```shell
export REVORNIX_BASE_URL="YOUR_API_PREFIX"
export REVORNIX_API_KEY="YOUR_API_KEY"
revornix --help
```

### CLI 快速开始

上传文件：

```shell
revornix files upload \
  --local-file-path ./tests/fixtures/test.txt \
  --remote-file-path uploads/test.txt
```

创建快速笔记文档：

```shell
revornix documents create-quick-note \
  --content "hello world" \
  --section 1 \
  --section 2 \
  --label 10 \
  --auto-summary
```

创建网页文档：

```shell
revornix documents create-website \
  --url https://www.google.com \
  --section 1 \
  --label 10
```

创建文件文档：

```shell
revornix documents create-file \
  --file-name demo.pdf \
  --section 1 \
  --label 10
```

创建音频文档：

```shell
revornix documents create-audio \
  --file-name demo.mp3 \
  --section 1 \
  --label 10 \
  --auto-transcribe
```

本地文件上传并一步创建文件文档：

```shell
revornix documents upload-create-file \
  --local-file-path ./tests/fixtures/test.txt \
  --remote-file-path uploads/test.txt \
  --section 1 \
  --label 10
```

创建文档标签：

```shell
revornix labels create-document-label --name research
```

创建专栏标签：

```shell
revornix labels create-section-label --name tutorial
```

列出所有文档标签：

```shell
revornix labels list-document-labels
```

列出所有专栏：

```shell
revornix sections list
```

获取文档详情：

```shell
revornix documents detail --document-id 123
```

搜索我的文档：

```shell
revornix documents search-mine --keyword notes --label 10 --desc true
```

执行文档向量检索：

```shell
revornix documents search-vector --query "检索增强生成"
```

创建专栏：

```shell
revornix sections create \
  --title "AI Notes" \
  --description "Knowledge base for AI" \
  --process-task-trigger-type 1 \
  --label 10 \
  --auto-publish
```

获取专栏详情：

```shell
revornix sections detail --section-id 12
```

发布专栏：

```shell
revornix sections publish --section-id 12 --status true
```

### CLI 命令参考

#### `files`

上传本地文件：

```shell
revornix files upload \
  --local-file-path ./demo.txt \
  --remote-file-path uploads/demo.txt \
  --content-type text/plain
```

#### `documents`

创建文件文档：

```shell
revornix documents create-file \
  --file-name demo.pdf \
  --title "Demo File" \
  --description "Imported from uploaded file" \
  --section 1 \
  --label 10 \
  --auto-summary
```

创建网页文档：

```shell
revornix documents create-website \
  --url https://example.com \
  --title "Example Website" \
  --section 1 \
  --label 10 \
  --auto-summary
```

创建快速笔记文档：

```shell
revornix documents create-quick-note \
  --content "Meeting notes" \
  --title "Meeting Notes" \
  --section 1 \
  --label 10
```

创建音频文档：

```shell
revornix documents create-audio \
  --file-name call.mp3 \
  --title "Customer Call" \
  --section 1 \
  --label 10 \
  --auto-transcribe \
  --auto-summary
```

上传文件并在一个命令里创建文件文档：

```shell
revornix documents upload-create-file \
  --local-file-path ./demo.pdf \
  --remote-file-path uploads/demo.pdf \
  --title "Demo File" \
  --section 1 \
  --label 10
```

上传音频文件并在一个命令里创建音频文档：

```shell
revornix documents upload-create-audio \
  --local-file-path ./call.mp3 \
  --remote-file-path uploads/call.mp3 \
  --title "Customer Call" \
  --section 1 \
  --label 10 \
  --auto-transcribe
```

获取文档详情：

```shell
revornix documents detail --document-id 123
```

更新文档元数据：

```shell
revornix documents update \
  --document-id 123 \
  --title "Updated Title" \
  --section 1 \
  --label 10
```

删除文档：

```shell
revornix documents delete --document-id 123 --document-id 124
```

搜索我的文档：

```shell
revornix documents search-mine \
  --keyword notes \
  --label 10 \
  --start 0 \
  --limit 20 \
  --desc true
```

执行文档向量检索：

```shell
revornix documents search-vector --query "检索增强生成"
```

#### `labels`

列出文档标签：

```shell
revornix labels list-document-labels
```

创建文档标签：

```shell
revornix labels create-document-label --name article
```

创建专栏标签：

```shell
revornix labels create-section-label --name collection
```

列出专栏标签：

```shell
revornix labels list-section-labels
```

删除文档标签：

```shell
revornix labels delete-document-labels --label-id 10 --label-id 11
```

删除专栏标签：

```shell
revornix labels delete-section-labels --label-id 20 --label-id 21
```

#### `sections`

列出专栏：

```shell
revornix sections list
```

创建专栏：

```shell
revornix sections create \
  --title "Weekly Digest" \
  --description "Weekly curated content" \
  --process-task-trigger-type 1 \
  --process-task-trigger-scheduler "0 0 * * 1" \
  --label 10
```

获取专栏详情：

```shell
revornix sections detail --section-id 12
```

列出专栏内的文档：

```shell
revornix sections documents --section-id 12 --start 0 --limit 20 --desc true
```

搜索我的专栏：

```shell
revornix sections search-mine --keyword digest --label 10 --desc true
```

更新专栏：

```shell
revornix sections update \
  --section-id 12 \
  --title "Weekly Digest" \
  --auto-podcast true \
  --auto-illustration false
```

删除专栏：

```shell
revornix sections delete --section-id 12
```

获取发布状态：

```shell
revornix sections get-publish --section-id 12
```

发布或取消发布：

```shell
revornix sections publish --section-id 12 --status true
revornix sections publish --section-id 12 --status false
```

重新发布：

```shell
revornix sections republish --section-id 12
```

### CLI 说明

- 多个专栏请重复传入 `--section`
- 多个标签请重复传入 `--label`
- `--section` 和 `--label` 都要求传数值 ID
- CLI 响应会以 JSON 输出
- `documents upload-create-file` 和 `documents upload-create-audio` 会先上传本地文件，再创建对应文档
- `documents search-vector` 依赖服务端已为目标文档生成 embedding
示例：

```shell
revornix documents create-quick-note \
  --content "hello" \
  --section 1 \
  --section 2 \
  --label 10 \
  --label 11
```

## Python SDK

### 创建 Session

```python
from revornix import Session

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)
```

### 导入 Schema 模型

```python
from revornix.schema import DocumentSchema, SectionSchema
```

### 上传文件

```python
from revornix import Session

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

res = session.upload_file(
    local_file_path="./tests/fixtures/test.txt",
    remote_file_path="uploads/test.txt",
)
```

### 创建文档标签

```python
from revornix import Session
from revornix.schema import DocumentSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = DocumentSchema.LabelAddRequest(name="test")
res = session.create_document_label(data=data)
```

### 创建专栏标签

```python
from revornix import Session
from revornix.schema import SectionSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = SectionSchema.LabelAddRequest(name="test")
res = session.create_section_label(data=data)
```

### 创建专栏

```python
from revornix import Session
from revornix.schema import SectionSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = SectionSchema.SectionCreateRequest(
    title="test",
    description="test",
    cover="test.png",
    labels=[],
    auto_publish=False,
    auto_podcast=False,
    auto_illustration=False,
    process_task_trigger_type=1,
    process_task_trigger_scheduler=None,
)

res = session.create_section(data=data)
```

### 获取所有文档标签

```python
from revornix import Session

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

res = session.get_mine_all_document_labels()
```

### 获取所有专栏

```python
from revornix import Session

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

res = session.get_mine_all_sections()
```

### 创建快速笔记文档

```python
from revornix import Session
from revornix.schema import DocumentSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = DocumentSchema.QuickNoteDocumentParameters(
    title="Quick Note",
    description="Created from SDK",
    cover=None,
    sections=[1, 2],
    labels=[10],
    content="test",
    auto_summary=False,
    auto_podcast=False,
    auto_tag=False,
)

res = session.create_quick_note_document(data=data)
```

### 创建网页文档

```python
from revornix import Session
from revornix.schema import DocumentSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = DocumentSchema.WebsiteDocumentParameters(
    title="Website Import",
    description="Created from URL",
    cover=None,
    sections=[1],
    labels=[10],
    url="https://www.google.com",
    auto_summary=False,
    auto_podcast=False,
    auto_tag=False,
)

res = session.create_website_document(data=data)
```

### 创建文件文档

```python
from revornix import Session
from revornix.schema import DocumentSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = DocumentSchema.FileDocumentParameters(
    title="File Import",
    description="Created from uploaded file",
    cover=None,
    sections=[1],
    labels=[10],
    file_name="demo.pdf",
    auto_summary=False,
    auto_podcast=False,
    auto_tag=False,
)

res = session.create_file_document(data=data)
```

### 创建音频文档

```python
from revornix import Session
from revornix.schema import DocumentSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = DocumentSchema.AudioDocumentParameters(
    title="Audio Import",
    description="Created from uploaded audio",
    cover=None,
    sections=[1],
    labels=[10],
    file_name="demo.mp3",
    auto_summary=False,
    auto_podcast=False,
    auto_transcribe=True,
    auto_tag=False,
)

res = session.create_audio_document(data=data)
```

### 执行文档向量检索

```python
from revornix import Session
from revornix.schema import DocumentSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = DocumentSchema.VectorSearchRequest(query="检索增强生成")
res = session.search_document_vector(data=data)
```

### 删除文档

```python
from revornix import Session
from revornix.schema import DocumentSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = DocumentSchema.DocumentDeleteRequest(document_ids=[123, 124])
res = session.delete_document(data=data)
```

### 删除专栏

```python
from revornix import Session
from revornix.schema import SectionSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = SectionSchema.SectionDeleteRequest(section_id=12)
res = session.delete_section(data=data)
```

## 可用的 SDK 方法

当前 `Session` 提供的方法有：

- `upload_file`
- `create_file_document`
- `create_website_document`
- `create_quick_note_document`
- `create_audio_document`
- `get_mine_all_document_labels`
- `create_document_label`
- `delete_document_label`
- `get_document_detail`
- `update_document`
- `delete_document`
- `search_mine_documents`
- `search_document_vector`
- `create_section_label`
- `get_mine_all_section_labels`
- `delete_section_label`
- `create_section`
- `update_section`
- `delete_section`
- `get_section_detail`
- `get_section_documents`
- `get_mine_all_sections`
- `search_mine_sections`
- `publish_section`
- `get_section_publish`
- `republish_section`

## 开发

项目结构：

- `src/revornix/session.py`：Revornix API 的核心 `Session` 客户端
- `src/revornix/cli/`：Typer CLI 入口、命令分组和 CLI 工作流
- `src/revornix/schema/`：Pydantic 请求与响应模型
- `src/revornix/endpoints/`：API 端点常量
- `tests/unit/`：不访问真实网络的单元测试
- `tests/integration/`：按需启用的真实 API 集成测试
- `tests/fixtures/`：测试和 CLI 示例使用的本地文件

运行测试：

```shell
pytest
```

只运行 CLI 测试：

```shell
pytest tests/unit/test_cli.py
```

运行全部单元测试：

```shell
pytest tests/unit
```

集成测试默认不运行；需要同时提供凭据并显式打开开关：

```shell
export REVORNIX_RUN_INTEGRATION_TESTS=true
pytest tests/integration
```

## 贡献者

<a href="https://github.com/Qingyon-AI/Revornx/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Qingyon-AI/Revornix" />
</a>

# Revornix Python Library

Python SDK and CLI for the Revornix API.

📕 API Documentation: [revornix/api](https://revornix.com/en/docs/features/api)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Qingyon-AI/Revornix)

## Full Application

The full Revornix application is available here:

[Qingyon-AI/Revornix](https://github.com/Qingyon-AI/Revornix)

## Introduction

- RoadMap: [RoadMap](https://huaqinda.notion.site/RoadMap-224bbdbfa03380fabd7beda0b0337ea3)
- Official Website: [revornix.com](https://revornix.com)
- Community: [Discord](https://discord.com/invite/3XZfz84aPN) | [WeChat](https://github.com/Qingyon-AI/Revornix/discussions/1#discussioncomment-13638435) | [QQ](https://github.com/Qingyon-AI/Revornix/discussions/1#discussioncomment-13638435)

## Installation

Install from PyPI:

```shell
pip install revornix
```

Install from source for local development:

```shell
pip install -e .
```

## Authentication

Both the Python SDK and CLI require:

- `base_url`: your Revornix API base URL
- `api_key`: your Revornix API key

For CLI usage, these environment variables are supported:

```shell
export REVORNIX_BASE_URL="YOUR_API_PREFIX"
export REVORNIX_API_KEY="YOUR_API_KEY"
```

Legacy aliases are also supported for compatibility:

```shell
export REVORNIX_URL_PREFIX="YOUR_API_PREFIX"
export API_KEY="YOUR_API_KEY"
```

## CLI

After installation, the `revornix` command is available.

Show help:

```shell
revornix --help
```

You can pass credentials with flags:

```shell
revornix --base-url "YOUR_API_PREFIX" --api-key "YOUR_API_KEY" --help
```

Or use environment variables:

```shell
export REVORNIX_BASE_URL="YOUR_API_PREFIX"
export REVORNIX_API_KEY="YOUR_API_KEY"
revornix --help
```

### CLI Quick Start

Upload a file:

```shell
revornix files upload \
  --local-file-path ./tests/test.txt \
  --remote-file-path uploads/test.txt
```

Create a quick note document:

```shell
revornix documents create-quick-note \
  --content "hello world" \
  --section 1 \
  --section 2 \
  --label 10 \
  --auto-summary
```

Create a website document:

```shell
revornix documents create-website \
  --url https://www.google.com \
  --section 1 \
  --label 10
```

Create a file document:

```shell
revornix documents create-file \
  --file-name demo.pdf \
  --section 1 \
  --label 10
```

Create an audio document:

```shell
revornix documents create-audio \
  --file-name demo.mp3 \
  --section 1 \
  --label 10 \
  --auto-transcribe
```

Create a document label:

```shell
revornix labels create-document --name research
```

Create a section label:

```shell
revornix labels create-section --name tutorial
```

List all document labels:

```shell
revornix labels list-document
```

List all sections:

```shell
revornix sections list
```

Create a section:

```shell
revornix sections create \
  --title "AI Notes" \
  --description "Knowledge base for AI" \
  --process-task-trigger-type 1 \
  --label 10 \
  --auto-publish
```

### CLI Command Reference

#### `files`

Upload a local file:

```shell
revornix files upload \
  --local-file-path ./demo.txt \
  --remote-file-path uploads/demo.txt \
  --content-type text/plain
```

#### `documents`

Create a file document:

```shell
revornix documents create-file \
  --file-name demo.pdf \
  --title "Demo File" \
  --description "Imported from uploaded file" \
  --section 1 \
  --label 10 \
  --auto-summary
```

Create a website document:

```shell
revornix documents create-website \
  --url https://example.com \
  --title "Example Website" \
  --section 1 \
  --label 10 \
  --auto-summary
```

Create a quick note document:

```shell
revornix documents create-quick-note \
  --content "Meeting notes" \
  --title "Meeting Notes" \
  --section 1 \
  --label 10
```

Create an audio document:

```shell
revornix documents create-audio \
  --file-name call.mp3 \
  --title "Customer Call" \
  --section 1 \
  --label 10 \
  --auto-transcribe \
  --auto-summary
```

#### `labels`

List document labels:

```shell
revornix labels list-document
```

Create a document label:

```shell
revornix labels create-document --name article
```

Create a section label:

```shell
revornix labels create-section --name collection
```

#### `sections`

List sections:

```shell
revornix sections list
```

Create a section:

```shell
revornix sections create \
  --title "Weekly Digest" \
  --description "Weekly curated content" \
  --process-task-trigger-type 1 \
  --process-task-trigger-scheduler "0 0 * * 1" \
  --label 10
```

### CLI Notes

- Use repeated `--section` options to pass multiple sections.
- Use repeated `--label` options to pass multiple labels.
- `--section` and `--label` expect numeric IDs.
- CLI responses are printed as JSON.

Example:

```shell
revornix documents create-quick-note \
  --content "hello" \
  --section 1 \
  --section 2 \
  --label 10 \
  --label 11
```

## Python SDK

### Create a Session

```python
from revornix import Session

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)
```

### Import Schema Models

```python
from revornix.schema import DocumentSchema, SectionSchema
```

### Upload a File

```python
from revornix import Session

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

res = session.upload_file(
    local_file_path="./tests/test.txt",
    remote_file_path="uploads/test.txt",
)
```

### Create a Document Label

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

### Create a Section Label

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

### Create a Section

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

### Get All Document Labels

```python
from revornix import Session

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

res = session.get_mine_all_document_labels()
```

### Get All Sections

```python
from revornix import Session

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

res = session.get_mine_all_sections()
```

### Create a Quick Note Document

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

### Create a Website Document

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

### Create a File Document

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

### Create an Audio Document

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

## Available SDK Methods

The current `Session` methods are:

- `upload_file`
- `create_file_document`
- `create_website_document`
- `create_quick_note_document`
- `create_audio_document`
- `get_mine_all_document_labels`
- `create_document_label`
- `create_section_label`
- `create_section`
- `get_mine_all_sections`

## Development

Run tests:

```shell
pytest
```

Run CLI tests only:

```shell
pytest tests/test_cli.py
```

## Contributors

<a href="https://github.com/Qingyon-AI/Revornx/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Qingyon-AI/Revornix" />
</a>

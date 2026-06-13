# Revornix Python Library

[English](./README.md) | [简体中文](./README.zh-CN.md)

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
  --local-file-path ./tests/fixtures/test.txt \
  --remote-file-path uploads/test.txt
```

Create a quick note document:

```shell
revornix documents create-quick-note \
  --content "hello world" \
  --section 1 \
  --section 2 \
  --label 10 \
  --auto-summary \
  --auto-publish \
  --access-key open-sesame
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

Upload a local file and create a file document in one step:

```shell
revornix documents upload-create-file \
  --local-file-path ./tests/fixtures/test.txt \
  --remote-file-path uploads/test.txt \
  --section 1 \
  --label 10
```

Create a document label:

```shell
revornix labels create-document-label --name research
```

Create a section label:

```shell
revornix labels create-section-label --name tutorial
```

List all document labels:

```shell
revornix labels list-document-labels
```

List all sections:

```shell
revornix sections list
```

Get document detail:

```shell
revornix documents detail --document-id 123
```

Search my documents:

```shell
revornix documents search-mine --keyword notes --label 10 --desc true
```

Run document vector search:

```shell
revornix documents search-vector --query "retrieval augmented generation"
```

Ask document AI and manage reading state:

```shell
revornix documents ask --document-id 123 --question "Summarize the key decisions"
revornix documents read --document-id 123 --status true
revornix documents star --document-id 123 --status true
```

Work with notes, task generation, and graphs:

```shell
revornix documents create-note --document-id 123 --content "Follow up next week"
revornix documents generate-graph --document-id 123
revornix documents generate-podcast --document-id 123
revornix graphs document --document-id 123
revornix graphs section --section-id 12
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

Get section detail:

```shell
revornix sections detail --section-id 12
```

Publish a section:

```shell
revornix sections publish --section-id 12 --status true
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

Upload a file and create a file document in one command:

```shell
revornix documents upload-create-file \
  --local-file-path ./demo.pdf \
  --remote-file-path uploads/demo.pdf \
  --title "Demo File" \
  --section 1 \
  --label 10
```

Upload an audio file and create an audio document in one command:

```shell
revornix documents upload-create-audio \
  --local-file-path ./call.mp3 \
  --remote-file-path uploads/call.mp3 \
  --title "Customer Call" \
  --section 1 \
  --label 10 \
  --auto-transcribe
```

Get document detail:

```shell
revornix documents detail --document-id 123
```

Update document metadata:

```shell
revornix documents update \
  --document-id 123 \
  --title "Updated Title" \
  --section 1 \
  --label 10
```

Delete documents:

```shell
revornix documents delete --document-id 123 --document-id 124
```

Search my documents:

```shell
revornix documents search-mine \
  --keyword notes \
  --label 10 \
  --start 0 \
  --limit 20 \
  --desc true
```

Run document vector search:

```shell
revornix documents search-vector --query "retrieval augmented generation"
```

#### `labels`

List document labels:

```shell
revornix labels list-document-labels
```

Create a document label:

```shell
revornix labels create-document-label --name article
```

Create a section label:

```shell
revornix labels create-section-label --name collection
```

List section labels:

```shell
revornix labels list-section-labels
```

Delete document labels:

```shell
revornix labels delete-document-labels --label-id 10 --label-id 11
```

Delete section labels:

```shell
revornix labels delete-section-labels --label-id 20 --label-id 21
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

Get section detail:

```shell
revornix sections detail --section-id 12
```

List section documents:

```shell
revornix sections documents --section-id 12 --start 0 --limit 20 --desc true
```

Search my sections:

```shell
revornix sections search-mine --keyword digest --label 10 --desc true
```

Update a section:

```shell
revornix sections update \
  --section-id 12 \
  --title "Weekly Digest" \
  --auto-podcast true \
  --auto-illustration false
```

Delete a section:

```shell
revornix sections delete --section-id 12
```

Get publish status:

```shell
revornix sections get-publish --section-id 12
```

Publish or unpublish:

```shell
revornix sections publish --section-id 12 --status true
revornix sections publish --section-id 12 --status false
```

Set or clear a publish access key:

```shell
revornix documents set-publish-access-key --document-id 123 --access-key open-sesame
revornix sections set-publish-access-key --section-id 12 --access-key section-key
revornix sections set-publish-access-key --section-id 12
```

Republish:

```shell
revornix sections republish --section-id 12
```

### CLI Notes

- Use repeated `--section` options to pass multiple sections.
- Use repeated `--label` options to pass multiple labels.
- `--section` and `--label` expect numeric IDs.
- CLI responses are printed as JSON.
- `documents upload-create-file` and `documents upload-create-audio` upload the local file first, then create the corresponding document.
- `documents search-vector` requires the target documents to already have embeddings generated on the server side.
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
    local_file_path="./tests/fixtures/test.txt",
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

### Run Document Vector Search

```python
from revornix import Session
from revornix.schema import DocumentSchema

session = Session(
    base_url="YOUR_API_PREFIX",
    api_key="YOUR_API_KEY",
)

data = DocumentSchema.VectorSearchRequest(query="retrieval augmented generation")
res = session.search_document_vector(data=data)
```

### Delete Documents

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

### Delete a Section

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

## Available SDK Methods

The current `Session` methods are:

- `upload_file`
- `create_file_document`
- `create_website_document`
- `create_quick_note_document`
- `create_audio_document`
- `get_mine_all_document_labels`
- `create_document_label`
- `delete_document_label`
- `get_document_detail`
- `ask_document`
- `create_document_ai_summary`
- `create_document_embedding`
- `transcribe_audio_document`
- `generate_document_graph`
- `generate_document_podcast`
- `get_document_month_summary`
- `create_document_note`
- `search_document_notes`
- `delete_document_notes`
- `update_document`
- `transform_document_markdown`
- `delete_document`
- `publish_document`
- `get_document_publish`
- `update_document_publish_access_key`
- `search_mine_documents`
- `search_unread_documents`
- `search_recent_documents`
- `search_star_documents`
- `search_document_vector`
- `set_document_read_status`
- `set_document_star_status`
- `create_section_label`
- `get_mine_all_section_labels`
- `delete_section_label`
- `create_section`
- `update_section`
- `delete_section`
- `get_section_detail`
- `get_section_documents`
- `ask_section`
- `get_mine_all_sections`
- `search_mine_sections`
- `search_subscribed_sections`
- `search_public_sections`
- `search_user_sections`
- `generate_section_podcast`
- `generate_section_ppt`
- `trigger_section_process`
- `retry_section_document`
- `publish_section`
- `get_section_publish`
- `update_section_publish_access_key`
- `republish_section`
- `search_graph`
- `search_document_graph`
- `search_section_graph`

## Development

Project layout:

- `src/revornix/session.py`: core `Session` client for the Revornix API
- `src/revornix/cli/`: Typer CLI entrypoint, command groups, and CLI workflows
- `src/revornix/schema/`: Pydantic request and response models
- `src/revornix/endpoints/`: API endpoint constants
- `tests/unit/`: unit tests that do not hit the real network
- `tests/integration/`: opt-in real API integration tests
- `tests/fixtures/`: local files used by tests and CLI examples

Run tests:

```shell
pytest
```

Run CLI tests only:

```shell
pytest tests/unit/test_cli.py
```

Run all unit tests:

```shell
pytest tests/unit
```

Integration tests are opt-in and require both credentials and an explicit switch:

```shell
export REVORNIX_RUN_INTEGRATION_TESTS=true
pytest tests/integration
```

## Contributors

<a href="https://github.com/Qingyon-AI/Revornx/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Qingyon-AI/Revornix" />
</a>

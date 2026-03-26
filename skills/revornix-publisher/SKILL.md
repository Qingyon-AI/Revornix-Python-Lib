---
name: revornix-publisher
description: Create and manage Revornix sections, labels, and documents from OpenClaw. Use when the user asks to create Revornix 专栏/section, 标签/label, quick note, website document, file document, audio document, or upload files to Revornix. Prefer this skill whenever OpenClaw needs to publish, sync, or organize content inside Revornix.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
    os:
      - darwin
      - linux
---

# Revornix Publisher

Use the bundled script through `bash` instead of hand-writing HTTP requests.

## Prerequisites

Require one of these environment variable pairs before making API calls:

- `REVORNIX_BASE_URL` and `REVORNIX_API_KEY`
- `REVORNIX_URL_PREFIX` and `API_KEY`

Fail fast if credentials are missing.

## Command Entry Point

Run:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py --help
```

If the skill is installed under a different root, adjust the path accordingly and keep using the bundled script from the skill folder.

## Workflow

1. Determine the target action first: list sections, create section, create label, upload file, or create a document.
2. Resolve section IDs and label IDs before creating a document. If the user gives names instead of IDs, list existing sections or labels first and only create missing labels or sections when that is clearly requested.
3. For file and audio documents:
   - If the user provides a local file, prefer the combined commands `upload-and-create-file-document` or `upload-and-create-audio-document`.
   - If the file was already uploaded earlier, use `create-file-document` or `create-audio-document`.
4. Use repeated `--section` flags for multiple sections and repeated `--label` flags for multiple labels.
5. When creating a section and the user does not provide a trigger type, default `--process-task-trigger-type` to `1` and state that assumption.
6. Return the JSON result and mention the created IDs in the final reply.

## Common Commands

List sections:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py list-sections
```

Create a section:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-section \
  --title "AI Notes" \
  --description "Knowledge base for AI" \
  --process-task-trigger-type 1
```

List document labels:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py list-document-labels
```

Create a document label:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-document-label --name research
```

Create a quick note document:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-quick-note \
  --content "hello world" \
  --section 1 \
  --label 10
```

Upload a local file and create a file document:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py upload-and-create-file-document \
  --local-file-path ./demo.pdf \
  --remote-file-path uploads/demo.pdf \
  --section 1 \
  --label 10
```

Upload a local audio file and create an audio document:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py upload-and-create-audio-document \
  --local-file-path ./demo.mp3 \
  --remote-file-path uploads/demo.mp3 \
  --section 1 \
  --label 10 \
  --auto-transcribe
```

## Guardrails

- Do not invent section IDs or label IDs.
- Do not create duplicate labels or sections when an existing one already matches the user intent.
- Do not expose API keys in responses.
- Prefer the bundled script over ad-hoc `curl` unless the user explicitly asks for raw HTTP.

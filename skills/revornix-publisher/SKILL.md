---
name: revornix-publisher
description: Create, search, inspect, update, publish, and organize Revornix sections, labels, and documents from OpenClaw. Use when the user asks to create Revornix 专栏 or section, 标签 or label, quick note, website document, file document, audio document, upload files, inspect document or section detail, search mine documents or sections, update metadata, or publish or republish sections in Revornix.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    os:
      - darwin
      - linux
---

# Revornix Publisher

Use the bundled Python script through `bash`. Do not hand-write HTTP requests unless the user explicitly asks for raw API calls.

## Prerequisites

Require one of these environment variable pairs before making API calls:

- `REVORNIX_BASE_URL` and `REVORNIX_API_KEY`
- `REVORNIX_URL_PREFIX` and `API_KEY`

Fail fast if credentials are missing.

## Entry Point

Run:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py --help
```

If the skill is installed under a different root, keep using the bundled script from the skill folder and adjust the path.

## Workflow

1. Determine whether the user wants to list, inspect, create, update, delete, search, publish, or republish.
2. Resolve section IDs and label IDs before creating or updating documents when the user only provides names.
3. Prefer listing existing sections or labels before creating new ones when duplication is possible.
4. For file and audio documents:
   - If the user provides a local file, prefer `upload-and-create-file-document` or `upload-and-create-audio-document`.
   - If the file is already present in Revornix storage, use `create-file-document` or `create-audio-document`.
5. Use repeated `--section`, `--label`, or `--label-id` flags for multiple values.
6. For search and publish style commands, pass explicit boolean text such as `true` or `false`.
7. Return the JSON result and call out created or updated IDs in the final reply.

## Common Commands

List sections:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py list-sections
```

Get section detail:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py section-detail --section-id 12
```

Search my sections:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py search-mine-sections \
  --keyword digest \
  --label 10 \
  --desc true
```

Create a section:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-section \
  --title "AI Notes" \
  --description "Knowledge base for AI" \
  --process-task-trigger-type 1
```

Update a section:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py update-section \
  --section-id 12 \
  --title "Weekly Digest" \
  --auto-podcast true \
  --auto-illustration false
```

Publish or unpublish a section:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py publish-section --section-id 12 --status true
python3 skills/revornix-publisher/scripts/revornix_api.py publish-section --section-id 12 --status false
```

Get section publish status:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py get-section-publish --section-id 12
```

Republish a section:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py republish-section --section-id 12
```

List document labels:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py list-document-labels
```

List section labels:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py list-section-labels
```

Create a document label:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-document-label --name research
```

Delete document labels:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py delete-document-label \
  --label-id 10 \
  --label-id 11
```

Create a quick note document:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-quick-note \
  --content "hello world" \
  --section 1 \
  --label 10
```

Get document detail:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py document-detail --document-id 123
```

Search my documents:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py search-mine-documents \
  --keyword notes \
  --label 10 \
  --desc true
```

Update document metadata:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py update-document \
  --document-id 123 \
  --title "Updated Title" \
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

- Do not invent section IDs, document IDs, or label IDs.
- Do not create duplicate labels or sections when an existing one already matches the user intent.
- Do not expose API keys in responses.
- Prefer reading detail or list endpoints before update or publish operations when the target object is ambiguous.

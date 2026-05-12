---
name: revornix-publisher
description: Create, search, inspect, update, delete, publish, comment on, and organize Revornix sections, day sections, labels, documents, notes, AI tasks, reading states, and knowledge graphs from OpenClaw. Use when the user asks to create Revornix 专栏 or section, 标签 or label, quick note, website document, file document, audio document, upload files, inspect document or section detail, ask document or section AI, search mine/unread/recent/starred documents, search sections, manage section comments, run vector or graph search, update or delete metadata objects, trigger summaries/embeddings/transcription/podcast/PPT/graph/process tasks, or publish or republish documents or sections in Revornix.
version: 1.4.0
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

Require these environment variables before making API calls:

- `REVORNIX_BASE_URL`
- `REVORNIX_API_KEY`

Fail fast if credentials are missing.

## Entry Point

Run:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py --help
```

If the skill is installed under a different root, keep using the bundled script from the skill folder and adjust the path.

## Workflow

1. Determine whether the user wants to list, inspect, create, update, delete, search, vector-search, graph-search, ask AI, set read/star state, manage notes, trigger processing tasks, publish, or republish.
2. Resolve section IDs and label IDs before creating or updating documents when the user only provides names.
3. Prefer listing existing sections or labels before creating new ones when duplication is possible.
4. For file and audio documents:
   - If the user provides a local file, prefer `upload-and-create-file-document` or `upload-and-create-audio-document`.
   - If the file is already present in Revornix storage, use `create-file-document` or `create-audio-document`.
5. Use repeated `--section`, `--label`, or `--label-id` flags for multiple values.
   Use repeated `--document-id` flags when deleting multiple documents.
6. For search and publish style commands, pass explicit boolean text such as `true` or `false`.
7. For document vector search and graph commands, remind the user that results depend on embeddings or graph tasks already being generated on the server side.
8. Return the JSON result and call out created or updated IDs in the final reply.

## Common Commands

List sections:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py list-sections
```

Get section detail:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py section-detail --section-id 12
```

Get day section info:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py section-date --date 2026-05-13
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

Delete a section:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py delete-section --section-id 12
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

Manage section comments:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-section-comment \
  --section-id 12 \
  --content "Great update"
python3 skills/revornix-publisher/scripts/revornix_api.py search-section-comments --section-id 12
python3 skills/revornix-publisher/scripts/revornix_api.py delete-section-comments --comment-id 45
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
python3 skills/revornix-publisher/scripts/revornix_api.py document-detail --url https://example.com/article
```

Search my documents:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py search-mine-documents \
  --keyword notes \
  --label 10 \
  --desc true
```

Search documents by vector similarity:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py search-document-vector \
  --query "向量数据库与检索增强生成" \
  --mode vector \
  --limit 10
```

Ask document or section AI:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py ask-document \
  --document-id 123 \
  --question "Summarize the key decisions"

python3 skills/revornix-publisher/scripts/revornix_api.py ask-section \
  --section-id 12 \
  --question "What themes connect these documents?"
```

Search unread, recent, or starred documents:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py search-unread-documents --limit 10
python3 skills/revornix-publisher/scripts/revornix_api.py search-recent-documents --keyword architecture
python3 skills/revornix-publisher/scripts/revornix_api.py search-star-documents --label 10
```

Set read or star status:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py read-document --document-id 123 --status true
python3 skills/revornix-publisher/scripts/revornix_api.py star-document --document-id 123 --status true
```

Publish or unpublish a document:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py publish-document --document-id 123 --status true
python3 skills/revornix-publisher/scripts/revornix_api.py get-document-publish --document-id 123
```

Manage document notes:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-document-note \
  --document-id 123 \
  --content "Follow up next week"
python3 skills/revornix-publisher/scripts/revornix_api.py search-document-notes --document-id 123
python3 skills/revornix-publisher/scripts/revornix_api.py delete-document-notes --note-id 45
```

Trigger document tasks:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py create-document-summary --document-id 123
python3 skills/revornix-publisher/scripts/revornix_api.py create-document-embedding --document-id 123
python3 skills/revornix-publisher/scripts/revornix_api.py generate-document-graph --document-id 123
python3 skills/revornix-publisher/scripts/revornix_api.py transcribe-document --document-id 123
python3 skills/revornix-publisher/scripts/revornix_api.py generate-document-podcast --document-id 123
```

Search graphs:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py search-graph
python3 skills/revornix-publisher/scripts/revornix_api.py document-graph --document-id 123
python3 skills/revornix-publisher/scripts/revornix_api.py section-graph --section-id 12
```

Trigger section tasks:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py generate-section-podcast --section-id 12
python3 skills/revornix-publisher/scripts/revornix_api.py generate-section-ppt --section-id 12
python3 skills/revornix-publisher/scripts/revornix_api.py trigger-section-process --section-id 12
python3 skills/revornix-publisher/scripts/revornix_api.py retry-section-document --section-id 12 --document-id 123
```

Update document metadata:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py update-document \
  --document-id 123 \
  --title "Updated Title" \
  --section 1 \
  --label 10
```

Delete documents:

```bash
python3 skills/revornix-publisher/scripts/revornix_api.py delete-document \
  --document-id 123 \
  --document-id 124
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
- Before deleting when the target is ambiguous, fetch detail or search results first to confirm the correct object.
- Do not expose API keys in responses.
- Prefer reading detail or list endpoints before update or publish operations when the target object is ambiguous.

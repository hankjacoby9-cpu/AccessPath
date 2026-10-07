# AccessPath backend

Django 5 + Django REST Framework, Celery + Redis for background jobs, PostgreSQL, and one
private S3 bucket with a folder per class.

## Run it

### Option 1. Without Docker (fastest)

Uses a local SQLite file instead of Postgres. Fine for working on models, endpoints and tests.

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Option 2. With Docker (the full stack)

Runs Django, a Celery worker, Postgres, Redis and MinIO (a local stand-in for S3).

```bash
cd backend
cp .env.example .env
docker compose up
```

Then open:
- http://localhost:8000/api/docs/ for every endpoint, with a "try it out" button
- http://localhost:8000/admin/ for the Django admin
- http://localhost:9001/ for the MinIO file browser (login `minioadmin` / `minioadmin`)

## Before you push

```bash
ruff check .
pytest
python manage.py makemigrations --check
python manage.py spectacular --file openapi.yaml
```

CI runs the same checks on every pull request, against real Postgres.

## How the code is organized

Each app belongs to one engineer's lane. Apps talk to each other only through the public
functions listed here, never by reaching into another app's internals.

| App | Lane | What it holds | Public functions |
|---|---|---|---|
| `accounts` | A | User (email login), onboarding answers | |
| `classes` | A | Class, ClassMembership, Invite, Lecture, permissions | `services.create_class`, `change_role`, `remove_member` |
| `storage` | A | The only code that talks to S3 | `s3.class_key`, `presign_upload`, `presign_download`, `put_bytes`, `get_bytes` |
| `uploads` | B | SourceFile, ProcessingJob, ParsedDocument, file routing | `tasks.convert_source_file` |
| `pipeline` | C | Prompts, model router, node XML schema, LLMCall cost log | `service.revise`, `tasks.process_document` |
| `review` | D | Node, NodeVersion, Comment, ReviewAction, state machine | `state_machine.transition`, `bulk_approve` |
| `exports` | E | Accessible HTML export (MathML, figures, tables), accessibility checks | `tasks.build_html_export` |

## Rules baked into the code

- **A class always has at least one active professor.** Enforced in `classes/services.py`.
- **Role is per class.** `ClassMembership.role` is the real permission, not anything on User.
- **Node versions are append only.** Saving an existing `NodeVersion` raises an error.
- **State changes go through `review/state_machine.py`.** No endpoint sets `Node.state` directly.
- **Bulk approve is all or nothing**, only works on nodes the TA already approved, and writes
  one audit row per node.
- **Models are settings.** `LLM_STRONG_MODEL` and `LLM_CHEAP_MODEL` in `.env`.

## What is built and what is a stub

Built and tested: login, logout, me, onboarding, create and list classes, list members, change
roles and remove members (with the last professor rule), lectures, every model in the plan,
the review state machine with bulk approve, file routing, the S3 handler, Docker, CI.

Stubs marked `TODO (Engineer X)`: the convert task (B), process and revise (C), HTML export (E),
invites and Purdue email verification (A), and all upload, review and export endpoints.

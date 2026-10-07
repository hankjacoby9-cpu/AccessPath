# Start here

Read this whole page first. It takes about 10 minutes. Then open the guide for your lane.

| You are | Read next |
|---|---|
| Engineer A, platform and identity | [engineer-a.md](engineer-a.md) |
| Engineer B, ingestion | [engineer-b.md](engineer-b.md) |
| Engineer C, AI processing | [engineer-c.md](engineer-c.md) |
| Engineer D, review | [engineer-d.md](engineer-d.md) |
| Engineer E, export and accessibility | [engineer-e.md](engineer-e.md) |

## What we are building, in one paragraph

A TA uploads lecture files. We turn each file into small pieces called **nodes** (a paragraph,
an equation, a picture, a graph, a table, a bit of code). AI writes a first draft of the
accessible version of each node, like a description of a picture or the LaTeX for an equation.
A TA checks every node, then a professor checks them. When everything is approved we produce
one clean HTML page that a blind or low-vision student can use with a screen reader.

## How one lecture moves through the code

Follow this once with the code open and the whole project will make sense.

```
1. Professor makes a class            apps/classes/services.py      create_class()        Engineer A
2. TA makes a lecture                 apps/classes/models.py        Lecture               Engineer A
3. TA uploads a PDF to S3             apps/storage/s3.py            presign_upload()      Engineer A builds, B uses
4. We convert the PDF to Markdown     apps/uploads/tasks.py         convert_source_file   Engineer B
5. AI splits it into nodes            apps/pipeline/tasks.py        process_document      Engineer C
6. TA and professor review nodes      apps/review/state_machine.py  transition()          Engineer D
7. We build the accessible HTML       apps/exports/tasks.py         build_html_export     Engineer E
```

Steps 1, 2, 3 and 6 work today. Steps 4, 5 and 7 are empty functions marked
`TODO (Engineer X)`. Filling them in is most of the job.

## Words you will see everywhere

| Word | What it means here |
|---|---|
| **Django** | The Python framework the whole backend is built on. |
| **App** | One folder inside `apps/`. Each engineer owns one or two. |
| **Model** | A Python class in `models.py` that becomes a database table. `Node` is a model. |
| **Migration** | A file Django writes that changes the database to match your models. Run `python manage.py makemigrations` after changing a model. |
| **Serializer** | Turns a model into JSON for the frontend, and checks JSON coming in. Lives in `serializers.py`. |
| **View** | The function that runs when the frontend calls a URL. Lives in `views.py`. |
| **URL** | Connects a web address to a view. Lives in `urls.py`. |
| **Celery task** | A function that runs in the background so the website does not freeze. Lives in `tasks.py`. |
| **S3** | Amazon's file storage. Locally we use MinIO, which acts the same. |
| **Presigned URL** | A temporary link that lets the browser upload or download one file directly. |
| **Node** | One piece of a lecture that someone reviews. |
| **NodeVersion** | One saved draft of a node. We never edit old versions, we only add new ones. |
| **State** | Where a node is in review, like `ta_review`, `prof_review` or `approved`. |

## Your first hour

1. Get it running. Follow "Run it" in [../README.md](../README.md). Option 1 needs no Docker.
2. Load the demo data.
   ```bash
   python manage.py seed_demo
   ```
3. Open http://localhost:8000/admin/ and log in as `prof@demo.edu` with password `demo-password-123`.
   Click around. Look at Classes, Lectures and Nodes. This is the data you will be working with.
4. Open http://localhost:8000/api/docs/ and try `POST /api/v1/auth/login`, then `GET /api/v1/classes`.
   This is exactly what the frontend will do.
5. Run the tests. All of them should pass.
   ```bash
   pytest
   ```
6. Read your lane's guide and pick your first task.

## Team rules

- **Stay in your folder.** If you need something from another lane, call its public function
  (listed in the README) or ask that engineer. Do not import another app's internals.
- **Small pull requests.** Make a branch, finish one thing, open a pull request, get one review.
  Branches should not live more than two days.
- **Tests come with the code.** Every pull request adds or updates a test.
- **Ask early.** If you are stuck for more than 30 minutes, post in the team chat. Being confused
  in week 1 is normal. Staying confused quietly is the only real problem.

## Where the bigger picture lives

The full team plan, with the week by week timeline and every decision explained:
https://claude.ai/artifact/5GkNuvBh5HFiTBqueF1JFM

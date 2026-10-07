# Engineer B. Ingestion

**Your job in one sentence.** Take any file a TA uploads and turn it into clean Markdown plus a list of the pictures and equations inside it.

## Your folder
`apps/uploads/`

## Already done
- The models. `SourceFile` (the upload), `ProcessingJob` (progress), `ParsedDocument` (your output).
- Routing by file extension (`apps/uploads/routing.py`).
- An empty task waiting for you, `convert_source_file` in `apps/uploads/tasks.py`.

## Read these first, in order
1. `apps/uploads/models.py`. Especially the comment on `ParsedDocument`. That is your contract with Engineer C.
2. `apps/uploads/routing.py`.
3. `apps/storage/s3.py`. You will use `presign_upload`, `get_bytes` and `put_bytes`.

## Your first tasks
1. **The MarkItDown test (week 1, most important).** Collect 10 real lecture files (PDFs and slides).
   Run them through MarkItDown in a small script. Write down what comes out right and what breaks.
   We already expect it to drop images and scramble equations. Find out how badly.
   ```python
   from markitdown import MarkItDown
   print(MarkItDown().convert("lecture.pdf").text_content)
   ```
   Save a few good outputs in `apps/pipeline/fixtures/` so Engineer C can start without waiting for you.
2. **Upload endpoints.** `POST /lectures/:id/uploads` returns a presigned URL. `POST /uploads/:id/complete`
   checks the file landed, checks its real type, and starts `convert_source_file`.
3. **Pull out images.** Use PyMuPDF (`import fitz`) to save every image in a PDF to S3 with its page number.

## Who you work with most
Engineer C, who takes your `ParsedDocument`. Agree on its exact shape in week 1.

"""Lane B. Celery tasks on the convert queue."""

from celery import shared_task


@shared_task
def convert_source_file(source_file_id: str) -> None:
    """
    TODO (Engineer B):
    1. Download the file from S3 and confirm its real type from its first bytes.
    2. Run MarkItDown and save the Markdown to S3.
    3. Extract figures and equation crops (PyMuPDF for PDF, python-pptx for slides).
    4. Create the ParsedDocument, then queue apps.pipeline.tasks.process_document.
    """
    raise NotImplementedError

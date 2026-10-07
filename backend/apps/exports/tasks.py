"""Lane E. Celery tasks on the export queue."""

from celery import shared_task


@shared_task
def build_html_export(export_id: str) -> None:
    """
    TODO (Engineer E): refuse unless every node in the lecture is approved, then build HTML
    with real headings, MathML for equations (from LaTeX), and <figure> with alt text for
    images and graphs. Strip all node metadata. Save to S3 and record version_ids.
    """
    raise NotImplementedError

"""Lane C. Celery tasks on the llm queue."""

from celery import shared_task


@shared_task
def process_document(parsed_document_id: str) -> None:
    """
    TODO (Engineer C):
    1. Build the prompt (fixed system prompt + lecture ta_context + Markdown chunk).
    2. Call the strong model with structured output, then build node XML from the result.
    3. Validate the XML against pipeline/schema, save it to S3.
    4. Create one Node and its first NodeVersion per node. Send images and graphs to the cheap model.
    5. Log every call in LLMCall.
    """
    raise NotImplementedError

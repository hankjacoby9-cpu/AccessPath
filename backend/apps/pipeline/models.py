from django.db import models

from apps.common import BaseModel


class LLMCall(BaseModel):
    """One call to a model. Used to track cost per class and per prompt version."""

    klass = models.ForeignKey("classes.Class", on_delete=models.CASCADE, related_name="llm_calls")
    node = models.ForeignKey("review.Node", on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    source_file = models.ForeignKey("uploads.SourceFile", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="+")
    purpose = models.CharField(max_length=50)  # "process", "describe_image", "equation", "revise"
    model = models.CharField(max_length=100)
    prompt_version = models.CharField(max_length=50)
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    cache_read_tokens = models.IntegerField(default=0)
    cost_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    latency_ms = models.IntegerField(default=0)

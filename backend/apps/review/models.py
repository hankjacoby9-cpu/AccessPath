from django.conf import settings
from django.db import models

from apps.common import BaseModel


class Node(BaseModel):
    """One piece of a lecture (a paragraph, an equation, a figure). The unit people review."""

    class Kind(models.TextChoices):
        TEXT = "text", "Text"
        CODE = "code", "Code snippet"
        EQUATION = "equation", "Equation"
        IMAGE = "image", "Image"
        GRAPH = "graph", "Graph"
        TABLE = "table", "Table"
        VIDEO = "video", "Video"
        AUDIO = "audio", "Audio"

    class State(models.TextChoices):
        PROCESSING = "processing", "Processing"
        FAILED = "failed", "Failed"
        TA_REVIEW = "ta_review", "Waiting for TA"
        FLAGGED = "flagged", "Flagged"
        PROF_REVIEW = "prof_review", "Waiting for professor"
        REVISING = "revising", "AI revising"
        APPROVED = "approved", "Approved"
        EXPORTED = "exported", "Exported"

    klass = models.ForeignKey("classes.Class", on_delete=models.CASCADE, related_name="nodes")
    lecture = models.ForeignKey("classes.Lecture", on_delete=models.CASCADE, related_name="nodes")
    document = models.ForeignKey("uploads.ParsedDocument", on_delete=models.CASCADE, related_name="nodes")
    order = models.PositiveIntegerField()
    kind = models.CharField(max_length=20, choices=Kind.choices)
    state = models.CharField(max_length=20, choices=State.choices, default=State.PROCESSING, db_index=True)
    confidence = models.FloatField(null=True, blank=True)  # 0 to 1, lower means a TA should look closer
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="assigned_nodes")
    current_version = models.ForeignKey("NodeVersion", on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name="+")
    flag_reason = models.TextField(blank=True)
    # Where it came from: {"page": 3, "box": [x0, y0, x1, y1], "asset_key": "classes/.../fig_003.png"}
    source_ref = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["lecture", "order"]
        indexes = [models.Index(fields=["klass", "state", "confidence"])]


class NodeVersion(BaseModel):
    """
    One saved version of a node's content. Never edited or deleted, only added to.
    History, diffs and the audit trail all come from this table.
    """

    class AuthorType(models.TextChoices):
        AI = "ai", "AI"
        PERSON = "person", "Person"

    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="versions")
    number = models.PositiveIntegerField()
    content = models.TextField()  # text, LaTeX, image description or code, depending on node kind
    extra = models.JSONField(default=dict, blank=True)  # e.g. {"language": "python"} or {"long_description": "..."}
    author_type = models.CharField(max_length=10, choices=AuthorType.choices)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="+")
    model = models.CharField(max_length=100, blank=True)
    prompt_version = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["node", "number"]
        constraints = [models.UniqueConstraint(fields=["node", "number"], name="unique_version_number")]

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise ValueError("Node versions are append only. Create a new version instead.")
        super().save(*args, **kwargs)


class Comment(BaseModel):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="comments")
    version = models.ForeignKey(NodeVersion, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    text = models.TextField()
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]


class ReviewAction(BaseModel):
    """Every approve, edit, flag, send back or regenerate. This is the audit trail."""

    class Action(models.TextChoices):
        APPROVE = "approve", "Approve"
        EDIT = "edit", "Edit"
        FLAG = "flag", "Flag"
        UNFLAG = "unflag", "Unflag"
        SEND_BACK = "send_back", "Send back"
        REGENERATE = "regenerate", "Regenerate"

    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="actions")
    version = models.ForeignKey(NodeVersion, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    role = models.CharField(max_length=20)  # role in the class at the time, "professor" or "ta"
    action = models.CharField(max_length=20, choices=Action.choices)
    comment = models.TextField(blank=True)
    from_state = models.CharField(max_length=20)
    to_state = models.CharField(max_length=20)

    class Meta:
        ordering = ["created_at"]

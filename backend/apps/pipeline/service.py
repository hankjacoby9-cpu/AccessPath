"""
Lane C's public functions. Other apps call these and nothing else in apps.pipeline.
"""


def revise(node_id, comment: str, *, requested_by) -> None:
    """
    Send a node back through the model with a professor's or TA's comment.

    TODO (Engineer C): build the revision prompt from the node's current version,
    the comment and the lecture's ta_context, then save the result as a new
    NodeVersion (author_type "ai") and move the node back to ta_review.
    """
    raise NotImplementedError

"""
The one place that decides which state changes are allowed. No endpoint changes
Node.state directly. Everything goes through transition().
"""

from django.db import transaction

from .models import Node, ReviewAction

S = Node.State
A = ReviewAction.Action
PROFESSOR, TA = "professor", "ta"

# (from_state, action) -> (to_state, roles allowed)
TRANSITIONS = {
    (S.TA_REVIEW, A.APPROVE): (S.PROF_REVIEW, {TA, PROFESSOR}),
    (S.TA_REVIEW, A.EDIT): (S.TA_REVIEW, {TA, PROFESSOR}),
    (S.TA_REVIEW, A.FLAG): (S.FLAGGED, {TA, PROFESSOR}),
    (S.TA_REVIEW, A.REGENERATE): (S.PROCESSING, {TA, PROFESSOR}),
    (S.FLAGGED, A.UNFLAG): (S.TA_REVIEW, {TA, PROFESSOR}),
    (S.PROF_REVIEW, A.APPROVE): (S.APPROVED, {PROFESSOR}),
    (S.PROF_REVIEW, A.EDIT): (S.PROF_REVIEW, {PROFESSOR}),
    (S.PROF_REVIEW, A.SEND_BACK): (S.REVISING, {PROFESSOR}),
}


class TransitionError(Exception):
    pass


def transition(node: Node, action: str, *, actor, role: str, comment: str = "") -> ReviewAction:
    key = (node.state, action)
    if key not in TRANSITIONS:
        raise TransitionError(f"Can't {action} a node that is {node.get_state_display().lower()}.")
    to_state, roles = TRANSITIONS[key]
    if role not in roles:
        raise TransitionError(f"Only a {' or '.join(sorted(roles))} can do that.")
    if action == A.SEND_BACK and not comment.strip():
        raise TransitionError("Sending a node back needs a comment.")

    record = ReviewAction(node=node, version=node.current_version, actor=actor, role=role,
                          action=action, comment=comment, from_state=node.state, to_state=to_state)
    node.state = to_state
    if action == A.FLAG:
        node.flag_reason = comment
    node.save(update_fields=["state", "flag_reason", "updated_at"])
    record.save()
    return record


def bulk_approve(nodes: list[Node], *, actor) -> list[ReviewAction]:
    """Professor approves many nodes at once. All succeed or none do."""
    with transaction.atomic():
        not_ready = [n for n in nodes if n.state != S.PROF_REVIEW]
        if not_ready:
            raise TransitionError(f"{len(not_ready)} of these nodes are not waiting for a professor yet.")
        return [transition(n, A.APPROVE, actor=actor, role=PROFESSOR) for n in nodes]

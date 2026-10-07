import pytest

from apps.classes import services
from apps.classes.models import Lecture
from apps.review.models import Node, NodeVersion
from apps.review.state_machine import TransitionError, bulk_approve, transition
from apps.uploads.models import ParsedDocument, SourceFile

S = Node.State


@pytest.fixture
def setup(make_user):
    prof = make_user("prof@purdue.edu")
    ta = make_user("ta@purdue.edu")
    klass = services.create_class(user=prof, name="Dynamics")
    lecture = Lecture.objects.create(klass=klass, title="Work and Energy")
    sf = SourceFile.objects.create(klass=klass, lecture=lecture, uploaded_by=ta, original_name="l4.pdf",
                                   extension="pdf", s3_key="k")
    doc = ParsedDocument.objects.create(source_file=sf, markdown_s3_key="m")

    def node(state=S.TA_REVIEW):
        n = Node.objects.create(klass=klass, lecture=lecture, document=doc, order=0, kind="text", state=state)
        n.current_version = NodeVersion.objects.create(node=n, number=1, content="hi", author_type="ai")
        n.save()
        return n

    return prof, ta, node


def test_ta_approve_goes_to_professor(setup):
    prof, ta, node = setup
    n = node()
    transition(n, "approve", actor=ta, role="ta")
    assert n.state == S.PROF_REVIEW


def test_ta_cannot_give_final_approval(setup):
    prof, ta, node = setup
    with pytest.raises(TransitionError):
        transition(node(S.PROF_REVIEW), "approve", actor=ta, role="ta")


def test_send_back_needs_comment(setup):
    prof, ta, node = setup
    with pytest.raises(TransitionError):
        transition(node(S.PROF_REVIEW), "send_back", actor=prof, role="professor")


def test_bulk_approve_is_all_or_nothing(setup):
    prof, ta, node = setup
    ready, not_ready = node(S.PROF_REVIEW), node(S.TA_REVIEW)
    with pytest.raises(TransitionError):
        bulk_approve([ready, not_ready], actor=prof)
    ready.refresh_from_db()
    assert ready.state == S.PROF_REVIEW


def test_bulk_approve_writes_one_audit_row_per_node(setup):
    prof, ta, node = setup
    nodes = [node(S.PROF_REVIEW) for _ in range(3)]
    actions = bulk_approve(nodes, actor=prof)
    assert len(actions) == 3
    assert all(n.state == S.APPROVED for n in nodes)


def test_versions_cannot_be_edited(setup):
    prof, ta, node = setup
    v = node().current_version
    v.content = "changed"
    with pytest.raises(ValueError):
        v.save()

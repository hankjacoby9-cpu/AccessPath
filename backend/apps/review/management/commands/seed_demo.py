"""
Fills an empty database with demo data so you can see the app working.

    python manage.py seed_demo

Creates a professor, a TA, one class, one lecture and six nodes in different
review states. Safe to run more than once. It deletes the old demo class first.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import User
from apps.classes import services
from apps.classes.models import Class, ClassMembership, Lecture
from apps.review.models import Node, NodeVersion
from apps.uploads.models import ParsedDocument, SourceFile

PASSWORD = "demo-password-123"
COURSE_CODE = "DEMO 101"

NODES = [
    ("text", "ta_review", 0.96, "Work is the integral of force along a path."),
    ("equation", "ta_review", 0.62, r"W = \int_{s_1}^{s_2} F \cos\theta \, ds"),
    ("graph", "ta_review", 0.41, "Force on the y axis against displacement on the x axis. "
                                 "The area under the curve is the work done."),
    ("image", "prof_review", 0.78, "A block being pulled up a ramp by a rope at a 30 degree angle."),
    ("code", "prof_review", 0.93, "work = sum(f * dx for f, dx in zip(forces, steps))"),
    ("table", "approved", 0.88, "| Object | Mass (kg) | Work (J) |\n|---|---|---|\n| Block A | 2 | 40 |"),
]


class Command(BaseCommand):
    help = "Create demo users, a class, a lecture and nodes."

    @transaction.atomic
    def handle(self, *args, **options):
        prof = self._user("prof@demo.edu", "Demo Professor")
        ta = self._user("ta@demo.edu", "Demo TA")

        Class.objects.filter(course_code=COURSE_CODE).delete()
        klass = services.create_class(user=prof, name="Dynamics", course_code=COURSE_CODE, term="Fall 2026",
                                      subject="Mechanical Engineering")
        ClassMembership.objects.create(user=ta, klass=klass, role=ClassMembership.Role.TA, invited_by=prof)

        lecture = Lecture.objects.create(klass=klass, title="Lecture 4. Work and Energy", order=4,
                                         ta_context="Introduces work as force times distance and the work energy "
                                                    "theorem. Students should be able to compute work from a graph.")
        source = SourceFile.objects.create(klass=klass, lecture=lecture, uploaded_by=ta,
                                           original_name="lecture4_work_energy.pdf", extension="pdf",
                                           s3_key=f"classes/{klass.id}/uploads/demo/lecture4_work_energy.pdf",
                                           status=SourceFile.Status.DONE)
        doc = ParsedDocument.objects.create(source_file=source, markdown_s3_key="demo/lecture4.md")

        for order, (kind, state, confidence, content) in enumerate(NODES):
            node = Node.objects.create(klass=klass, lecture=lecture, document=doc, order=order, kind=kind,
                                       state=state, confidence=confidence, source_ref={"page": order + 1})
            node.current_version = NodeVersion.objects.create(
                node=node, number=1, content=content, author_type=NodeVersion.AuthorType.AI,
                model="demo", prompt_version="demo")
            node.save()

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        self.stdout.write(f"  Professor login  prof@demo.edu / {PASSWORD}")
        self.stdout.write(f"  TA login         ta@demo.edu / {PASSWORD}")
        self.stdout.write("  See it at        http://localhost:8000/admin/ and http://localhost:8000/api/docs/")

    def _user(self, email, name):
        user, _ = User.objects.get_or_create(email=email, defaults={"name": name})
        user.name = name
        user.is_staff = True  # so demo users can open the Django admin
        user.set_password(PASSWORD)
        user.save()
        return user

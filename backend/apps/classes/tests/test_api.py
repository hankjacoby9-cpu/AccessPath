import pytest


@pytest.mark.django_db
def test_create_class_and_block_removing_last_professor(api, make_user):
    make_user("prof@purdue.edu")
    res = api.post("/api/v1/auth/login", {"email": "prof@purdue.edu", "password": "a-good-password-123"})
    assert res.status_code == 200

    res = api.post("/api/v1/classes", {"name": "Dynamics", "course_code": "ME 27400"})
    assert res.status_code == 201
    assert res.data["my_role"] == "professor"
    class_id = res.data["id"]

    members = api.get(f"/api/v1/classes/{class_id}/members").data
    res = api.delete(f"/api/v1/classes/{class_id}/members/{members[0]['id']}")
    assert res.status_code == 409


@pytest.mark.django_db
def test_outsider_cannot_see_class_lectures(api, make_user):
    make_user("prof@purdue.edu")
    make_user("outsider@purdue.edu")
    api.post("/api/v1/auth/login", {"email": "prof@purdue.edu", "password": "a-good-password-123"})
    class_id = api.post("/api/v1/classes", {"name": "Dynamics"}).data["id"]

    api.post("/api/v1/auth/logout")
    api.post("/api/v1/auth/login", {"email": "outsider@purdue.edu", "password": "a-good-password-123"})
    assert api.get(f"/api/v1/classes/{class_id}/lectures").status_code == 403

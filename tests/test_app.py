def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_reflects_in_activity(client):
    email = "testsignup@mergington.edu"
    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert resp.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_duplicate_signup_fails(client):
    email = "michael@mergington.edu"  # already signed up in initial data
    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert resp.status_code == 400


def test_unregistered_participant_is_removed(client):
    email = "michael@mergington.edu"
    assert email in client.get("/activities").json()["Chess Club"]["participants"]
    resp = client.delete(f"/activities/Chess%20Club/participants?email={email}")
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_delete_nonexistent_returns_404(client):
    email = "doesnotexist@mergington.edu"
    resp = client.delete(f"/activities/Chess%20Club/participants?email={email}")
    assert resp.status_code == 404


def test_signup_nonexistent_activity_returns_404(client):
    resp = client.post("/activities/NoSuchActivity/signup?email=test@ex.com")
    assert resp.status_code == 404

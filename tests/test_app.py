from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_available_activities():
    # Arrange
    expected_activity_names = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()).issuperset(expected_activity_names)


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    chess_club = activities_response.json()[activity_name]
    assert email in chess_club["participants"]

    # Restore state for subsequent tests
    client.delete(f"/activities/{activity_name}/participants?email={email}")


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    chess_club = activities_response.json()[activity_name]
    assert email not in chess_club["participants"]

    # Restore state for subsequent tests
    client.post(f"/activities/{activity_name}/signup?email={email}")

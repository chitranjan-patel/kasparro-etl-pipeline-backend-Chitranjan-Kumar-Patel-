from app.db import models


def test_health(client, db_session):
    # no ETL runs yet
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert "database" in body
    assert "etl_last_run" in body

def test_data_empty(client):
    response = client.get("/data")
    assert response.status_code == 200
    body = response.json()
    assert body["pagination"]["total"] == 0
    assert "meta" in body
    assert "request_id" in body["meta"]
    assert "api_latency_ms" in body["meta"]

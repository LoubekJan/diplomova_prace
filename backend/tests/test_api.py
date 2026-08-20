def test_health_endpoints(client):
    live = client.get("/health/live")
    ready = client.get("/health/ready")

    assert live.status_code == 200
    assert live.json()["version"] == "test"
    assert ready.status_code == 200


def test_task_crud(client):
    created = client.post("/api/tasks", json={"title": "Dokončit praktickou část"})
    assert created.status_code == 201
    task_id = created.json()["id"]

    listed = client.get("/api/tasks")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.patch(f"/api/tasks/{task_id}", json={"completed": True})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "task_app_tasks_total 1" in metrics.text
    assert "task_app_tasks_completed 1" in metrics.text

    deleted = client.delete(f"/api/tasks/{task_id}")
    assert deleted.status_code == 204
    assert client.get("/api/tasks").json() == []


def test_missing_task_returns_404(client):
    response = client.patch("/api/tasks/999", json={"completed": True})
    assert response.status_code == 404

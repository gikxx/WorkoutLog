import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_nfr_02_performance_stats():
    """NFR-02: Время ответа статистики ≤ 2 s"""
    start_time = time.time()
    response = client.get("/stats/")
    end_time = time.time()

    response_time_ms = (end_time - start_time) * 1000
    assert (
        response_time_ms <= 2000
    ), f"Stats response time {response_time_ms:.2f}ms exceeds 2s limit"
    assert response.status_code == 200


def test_nfr_06_workouts_performance():
    """NFR-06: Время запроса тренировок ≤ 300ms"""
    start_time = time.time()
    response = client.get("/workouts/")
    end_time = time.time()

    response_time_ms = (end_time - start_time) * 1000
    assert (
        response_time_ms <= 300
    ), f"Workouts response time {response_time_ms:.2f}ms exceeds 300ms limit"
    assert response.status_code == 200


def test_nfr_04_api_stability():
    """NFR-04: Стабильность API - нет 5xx ошибок"""
    endpoints = ["/workouts/", "/exercises/", "/stats/"]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code != 500, f"Endpoint {endpoint} returned 500 error"

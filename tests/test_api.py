from fastapi.testclient import TestClient

from generative_cinema_ai.api import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json()["status"] == "ok"


def test_analysis_api() -> None:
    response = client.post(
        "/v1/analysis",
        json={
            "tenant_id": "00000000-0000-0000-0000-000000000001",
            "project_id": "00000000-0000-0000-0000-000000000002",
            "screenplay_text": "INT. VAULT - NIGHT\nA guard shouts. Mara sprints.",
            "input_format": "fountain",
        },
    )
    assert response.status_code == 200
    assert response.json()["scenes"][0]["signals"] == ["kinetic"]


def test_blank_rejected() -> None:
    response = client.post(
        "/v1/analysis",
        json={"tenant_id": "00000000-0000-0000-0000-000000000001", "project_id": "00000000-0000-0000-0000-000000000002", "screenplay_text": "   "},
    )
    assert response.status_code == 422


def test_validation_errors_are_bounded_and_do_not_echo_screenplay() -> None:
    secret = "CONFIDENTIAL-SCENE-ALPHA"
    response = client.post(
        "/v1/analysis",
        json={"tenant_id": "not-a-uuid", "project_id": "00000000-0000-0000-0000-000000000002", "screenplay_text": secret, "unexpected": secret},
    )
    assert response.status_code == 422
    assert secret not in response.text
    assert len(response.content) < 4096


def test_malformed_json_error_is_bounded_and_redacted() -> None:
    secret = "CONFIDENTIAL-MALFORMED-GAMMA"
    response = client.post("/v1/analysis", content=f'{{"screenplay_text":"{secret}"', headers={"content-type": "application/json"})
    assert response.status_code == 422
    assert secret not in response.text
    assert len(response.content) < 4096


def test_oversized_body_is_rejected_before_validation_without_echo() -> None:
    secret = "CONFIDENTIAL-SCENE-BETA"
    response = client.post("/v1/analysis", content=(secret + "x" * 525_000), headers={"content-type": "application/json"})
    assert response.status_code == 413
    assert secret not in response.text
    assert len(response.content) < 512


def test_non_loopback_request_is_blocked_by_default() -> None:
    guarded_client = TestClient(app, client=("203.0.113.10", 50000))
    assert guarded_client.get("/health").status_code == 403

from uuid import UUID

from generative_cinema_ai.models import AnalysisRequest
from generative_cinema_ai.service import AnalysisService

TENANT = UUID("00000000-0000-0000-0000-000000000001")
PROJECT = UUID("00000000-0000-0000-0000-000000000002")


def request(text: str) -> AnalysisRequest:
    return AnalysisRequest(tenant_id=TENANT, project_id=PROJECT, screenplay_text=text)


def test_recommendations_change_and_cite_source() -> None:
    service = AnalysisService()
    intimate = service.analyze(request("INT. ROOM - NIGHT\nThey whisper and embrace."))
    action = service.analyze(request("EXT. ROAD - DAY\nA car races, crashes, and explodes."))
    assert intimate.scenes[0].signals == ["intimacy"]
    assert action.scenes[0].signals == ["kinetic"]
    assert intimate.scenes[0].recommendations[0].value != action.scenes[0].recommendations[0].value
    span = action.scenes[0].recommendations[0].evidence[0]
    assert request("x").tenant_id == TENANT
    assert action.scenes[0].scene.source_span.start <= span.start < span.end <= action.scenes[0].scene.source_span.end


def test_five_categories() -> None:
    result = AnalysisService().analyze(request("EXT. CLIFF - SUNRISE\nThe vast ocean reveals itself."))
    assert {rec.category for rec in result.scenes[0].recommendations} == {"frame", "lighting_color", "lens", "movement", "texture"}


def test_neutral_recommendation_labels_context_as_non_evidence() -> None:
    result = AnalysisService().analyze(request("INT. OFFICE - DAY\nPat reads a report."))
    recommendation = result.scenes[0].recommendations[0]
    assert result.scenes[0].signals == ["neutral"]
    assert recommendation.evidence[0].kind == "context"
    assert "No classified cinematic signal" in recommendation.rationale
    assert "supported" not in recommendation.rationale

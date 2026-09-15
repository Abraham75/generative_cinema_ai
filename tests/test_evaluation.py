"""Executable deterministic regression protocol for the baseline engine."""

from uuid import UUID

import pytest

from generative_cinema_ai.models import AnalysisRequest
from generative_cinema_ai.service import AnalysisService

CASES = [
    ("INT. CELLAR - NIGHT\nA threat waits in the dark.", "tension"),
    ("INT. HOME - DAY\nThey whisper, then embrace.", "intimacy"),
    ("EXT. TRACK - DAY\nShe sprints as cars crash.", "kinetic"),
    ("EXT. CLIFF - SUNRISE\nThe vast ocean reveals itself.", "wonder"),
]


@pytest.mark.parametrize(("text", "expected"), CASES)
def test_signal_regression(text: str, expected: str) -> None:
    request = AnalysisRequest(tenant_id=UUID(int=1), project_id=UUID(int=2), screenplay_text=text)
    result = AnalysisService().analyze(request)
    assert result.scenes[0].signals == [expected]
    assert all(rec.evidence and rec.evidence[0].text.casefold() in text.casefold() for rec in result.scenes[0].recommendations)

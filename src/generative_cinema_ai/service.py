from .models import AnalysisRequest, AnalysisResult
from .parser import parse_screenplay
from .providers import CinematicAnalysisProvider, DeterministicCinematicProvider


class AnalysisService:
    def __init__(self, provider: CinematicAnalysisProvider | None = None) -> None:
        self.provider = provider or DeterministicCinematicProvider()

    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        scenes, warnings = parse_screenplay(request.screenplay_text, request.input_format)
        return AnalysisResult(
            tenant_id=request.tenant_id,
            project_id=request.project_id,
            provider=self.provider.name,
            provider_version=self.provider.version,
            scenes=[self.provider.analyze_scene(scene) for scene in scenes],
            warnings=warnings,
        )

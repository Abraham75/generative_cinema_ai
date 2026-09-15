from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol, cast

from .models import EvidenceSpan, Recommendation, RecommendationCategory, Scene, SceneAnalysis


class CinematicAnalysisProvider(Protocol):
    """Interface-level portability boundary; adapters may have different capabilities."""

    name: str
    version: str

    def analyze_scene(self, scene: Scene) -> SceneAnalysis: ...


@dataclass(frozen=True)
class _Rule:
    signal: str
    terms: tuple[str, ...]
    values: tuple[str, str, str, str, str]


_RULES = (
    _Rule(
        "tension",
        ("danger", "threat", "chase", "gun", "blood", "fear", "dark"),
        (
            "Tight medium shot emphasizing constrained space",
            "Low-key contrast with motivated practical light",
            "50mm lens with shallow depth of field",
            "Measured dolly-in to increase pressure",
            "Restrained grain with controlled shadow detail",
        ),
    ),
    _Rule(
        "intimacy",
        ("whisper", "touch", "kiss", "embrace", "confess", "alone"),
        (
            "Close two-shot preserving both performances",
            "Soft side light with gentle falloff",
            "65mm lens for intimate compression",
            "Subtle handheld drift tied to breath",
            "Clean skin tones with fine-grain texture",
        ),
    ),
    _Rule(
        "kinetic",
        ("sprint", "crash", "explodes", "fight", "races", "shouts"),
        (
            "Wide-to-medium coverage preserving action geography",
            "Hard directional sources with readable separation",
            "28mm lens for speed and spatial energy",
            "Motivated tracking movement with stable geography",
            "Crisp contrast with selective motion blur",
        ),
    ),
    _Rule(
        "wonder",
        ("vast", "sunrise", "stars", "temple", "mountain", "ocean", "reveals"),
        (
            "Wide establishing frame emphasizing scale",
            "Layered natural light with luminous highlights",
            "24mm lens for environmental scale",
            "Slow crane or dolly reveal",
            "Atmospheric depth with restrained diffusion",
        ),
    ),
)
_DEFAULT = _Rule(
    "neutral",
    (),
    (
        "Medium-wide master establishing subjects and geography",
        "Motivated naturalistic key with controlled fill",
        "35mm lens for balanced spatial perspective",
        "Static start with movement reserved for a beat change",
        "Natural contrast with subtle film grain",
    ),
)
_CATEGORIES = ("frame", "lighting_color", "lens", "movement", "texture")


class DeterministicCinematicProvider:
    name = "deterministic-rules"
    version = "1.0"

    def analyze_scene(self, scene: Scene) -> SceneAnalysis:
        lowered = scene.text.casefold()
        count, rule = max(
            ((sum(len(re.findall(rf"\b{re.escape(term)}\b", lowered)) for term in item.terms), item) for item in _RULES), key=lambda item: item[0]
        )
        if count == 0:
            rule = _DEFAULT
        evidence = self._evidence(scene, rule)
        confidence = 0.55 if rule is _DEFAULT else min(0.9, 0.62 + count * 0.07)
        rationale = (
            "No classified cinematic signal was found. This continuity-first treatment is an editable fallback heuristic; the cited heading is context only."
            if rule is _DEFAULT
            else f"The {rule.signal} signal is supported by the cited trigger text; this is an editable creative proposal, not a factual requirement."
        )
        recs = [
            Recommendation(
                category=cast(RecommendationCategory, category),
                value=value,
                rationale=rationale,
                evidence=evidence,
                confidence=confidence,
                alternatives=["Use a neutral, continuity-first treatment"],
            )
            for category, value in zip(_CATEGORIES, rule.values, strict=True)
        ]
        return SceneAnalysis(scene=scene, signals=[rule.signal], recommendations=recs)

    @staticmethod
    def _evidence(scene: Scene, rule: _Rule) -> list[EvidenceSpan]:
        lowered = scene.text.casefold()
        evidence: list[EvidenceSpan] = []
        for term in rule.terms:
            for match in re.finditer(rf"\b{re.escape(term)}\b", lowered):
                start = scene.source_span.start + match.start()
                evidence.append(EvidenceSpan(start=start, end=start + len(term), text=scene.text[match.start() : match.end()], kind="trigger"))
                if len(evidence) == 8:
                    return evidence
        if evidence:
            return evidence
        excerpt = scene.heading
        local = scene.text.find(excerpt)
        if local < 0:
            local = len(scene.text) - len(scene.text.lstrip())
            excerpt = scene.text[local : local + 120].rstrip() or scene.text[:1]
        return [EvidenceSpan(start=scene.source_span.start + local, end=scene.source_span.start + local + len(excerpt), text=excerpt, kind="context")]

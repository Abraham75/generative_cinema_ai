from __future__ import annotations

import re
from dataclasses import dataclass
from typing import cast

from .models import EvidenceSpan, InputFormat, InteriorExterior, Scene

_HEADING = re.compile(r"^(?:\.)?(?P<prefix>INT\.?/EXT\.?|EXT\.?/INT\.?|INT\.?|EXT\.?)\s+(?P<body>.+)$", re.IGNORECASE)


@dataclass(frozen=True)
class _Heading:
    start: int
    raw: str
    prefix: str
    body: str


def _headings(text: str) -> list[_Heading]:
    found: list[_Heading] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        raw = line.rstrip("\r\n")
        match = _HEADING.match(raw.strip())
        if match:
            found.append(_Heading(offset, raw.strip().lstrip("."), match.group("prefix").upper().replace(".", ""), match.group("body").strip()))
        offset += len(line)
    return found


def _split_location_time(body: str) -> tuple[str, str | None]:
    parts = re.split(r"\s+-\s+", body, maxsplit=1)
    return parts[0].strip() or "UNSPECIFIED", parts[1].strip() if len(parts) == 2 else None


def parse_screenplay(text: str, input_format: InputFormat = InputFormat.AUTO) -> tuple[list[Scene], list[str]]:
    """Parse Fountain-style headings or return one plain-text fallback scene."""
    if not text.strip():
        raise ValueError("screenplay text must not be blank")
    headings = [] if input_format == InputFormat.PLAIN_TEXT else _headings(text)
    warnings: list[str] = []
    if not headings:
        start, end = 0, len(text)
        excerpt = text
        if input_format == InputFormat.FOUNTAIN:
            warnings.append("No Fountain scene headings were recognized.")
        warnings.append("No standard scene headings detected; review scene boundaries manually.")
        return [
            Scene(
                id="scene-001",
                ordinal=1,
                heading="UNSPECIFIED SCENE",
                interior_exterior="UNKNOWN",
                location="UNSPECIFIED",
                text=excerpt,
                source_span=EvidenceSpan(start=start, end=end, text=excerpt),
            )
        ], warnings
    scenes: list[Scene] = []
    if text[: headings[0].start]:
        preamble = text[: headings[0].start]
        scenes.append(
            Scene(
                id="scene-000",
                ordinal=1,
                heading="UNPARSED PREAMBLE",
                interior_exterior="UNKNOWN",
                location="UNSPECIFIED",
                text=preamble,
                source_span=EvidenceSpan(start=0, end=len(preamble), text=preamble, kind="context"),
            )
        )
        warnings.append("Text before the first scene heading was preserved as an unparsed preamble scene; review it manually.")
    for index, heading in enumerate(headings):
        end = headings[index + 1].start if index + 1 < len(headings) else len(text)
        scene_text = text[heading.start : end]
        location, time_of_day = _split_location_time(heading.body)
        scenes.append(
            Scene(
                id=f"scene-{index + 1:03d}",
                ordinal=len(scenes) + 1,
                heading=heading.raw,
                interior_exterior=cast(InteriorExterior, heading.prefix),
                location=location,
                time_of_day=time_of_day,
                text=scene_text,
                source_span=EvidenceSpan(start=heading.start, end=heading.start + len(scene_text), text=scene_text),
            )
        )
    return scenes, warnings

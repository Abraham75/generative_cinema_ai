from generative_cinema_ai.models import InputFormat
from generative_cinema_ai.parser import parse_screenplay


def test_parses_fountain_scenes_and_offsets() -> None:
    text = "INT. KITCHEN - NIGHT\nMara whispers.\n\nEXT. STREET - DAY\nA car races away.\n"
    scenes, warnings = parse_screenplay(text, InputFormat.FOUNTAIN)
    assert not warnings
    assert [scene.heading for scene in scenes] == ["INT. KITCHEN - NIGHT", "EXT. STREET - DAY"]
    assert scenes[0].location == "KITCHEN"
    assert text[scenes[1].source_span.start : scenes[1].source_span.end] == scenes[1].text


def test_plain_text_falls_back_with_warning() -> None:
    scenes, warnings = parse_screenplay("A room slowly appears.")
    assert scenes[0].interior_exterior == "UNKNOWN"
    assert warnings


def test_explicit_plain_text_never_interprets_headings() -> None:
    text = "INT. KITCHEN - NIGHT\nThis remains one plain-text scene."
    scenes, warnings = parse_screenplay(text, InputFormat.PLAIN_TEXT)
    assert len(scenes) == 1
    assert scenes[0].heading == "UNSPECIFIED SCENE"
    assert scenes[0].text == text
    assert warnings


def test_preamble_and_trailing_whitespace_are_preserved_without_gaps() -> None:
    text = "Title: Owned Test\r\nAuthor: Example\r\n\r\nINT. CAFÉ - DAY\r\nHello, 世界.  \r\n"
    scenes, warnings = parse_screenplay(text, InputFormat.FOUNTAIN)
    assert warnings
    assert scenes[0].heading == "UNPARSED PREAMBLE"
    assert "Title: Owned Test" in scenes[0].text
    assert "".join(scene.text for scene in scenes) == text
    assert scenes[-1].source_span.end == len(text)

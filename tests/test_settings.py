import pytest

from generative_cinema_ai.settings import Settings


def test_nondevelopment_environment_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("ALLOW_NETWORK_API", raising=False)
    with pytest.raises(RuntimeError, match="disabled outside development"):
        Settings.from_env()


def test_network_enablement_must_be_explicit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("ALLOW_NETWORK_API", "true")
    assert Settings.from_env().allow_network_api is True

"""Tests for interactive CLI entry and flows."""

from types import SimpleNamespace
from click.testing import CliRunner

from super_pocket.cli import cli


def test_cli_without_arguments_triggers_interactive(monkeypatch):
    """Running `pocket` without arguments should start interactive mode."""

    called = {"value": False}

    monkeypatch.setattr(
        "super_pocket.interactive.pocket_cmd", lambda: called.__setitem__("value", True)
    )
    monkeypatch.setattr("sys.stdin", SimpleNamespace(isatty=lambda: True))

    result = CliRunner().invoke(cli, [])

    assert result.exit_code == 0
    assert called["value"] is True


def test_pocket_cmd_uses_spinner_and_help(monkeypatch):
    """Ensure interactive help path shows spinner and runs help command."""

    from super_pocket import interactive

    recorded: list[object] = []
    prompt_calls: list[str] = []

    # Speed up and make deterministic
    monkeypatch.setattr(interactive.time, "sleep", lambda *_: None)
    monkeypatch.setattr(interactive, "display_logo", lambda: recorded.append("logo"))

    monkeypatch.setattr(
        interactive,
        "centered_spinner",
        lambda message, style="bold blue": recorded.append(("spinner", message)) or message,
    )

    class DummyLive:
        def __init__(self, spinner, refresh_per_second=None, transient=None):
            recorded.append(("live", spinner))

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            recorded.append("live_exit")

    monkeypatch.setattr(interactive, "Live", DummyLive)

    def fake_prompt(message, **kwargs):
        prompt_calls.append(message)
        return next(prompt_values)

    monkeypatch.setattr(interactive, "Prompt", SimpleNamespace(ask=fake_prompt))

    monkeypatch.setattr(
        interactive,
        "subprocess",
        SimpleNamespace(run=lambda *args, **kwargs: recorded.append(("run", args[0]))),
    )

    prompt_values = iter(["help", "", "exit"])

    interactive.pocket_cmd()

    assert ("spinner", "Loading help...") in recorded
    assert ("run", ["pocket", "--help"]) in recorded
    assert any("Press" in msg or "Appuie" in msg for msg in prompt_calls)

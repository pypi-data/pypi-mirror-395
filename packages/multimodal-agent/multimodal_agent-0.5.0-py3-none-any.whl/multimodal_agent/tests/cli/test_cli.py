import sys as system
import types
from unittest.mock import MagicMock

import pytest

from multimodal_agent import __version__
from multimodal_agent.cli import cli


@pytest.fixture(autouse=True)
def mock_google_client(mocker):
    """Mock genai.Client so no real Google API is touched."""
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = MagicMock(text="mocked")
    mocker.patch(
        "multimodal_agent.agent_core.genai.Client",
        return_value=fake_client,
    )
    return fake_client


# test cli version.
def test_cli_version(monkeypatch, capsys):
    monkeypatch.setattr(system, "argv", ["agent", "--version"])
    cli.main()
    captured = capsys.readouterr().out.strip()
    assert f"multimodal-agent version {__version__}" in captured


def test_cli_ask(monkeypatch, capsys, mocker):
    fake_agent = types.SimpleNamespace(
        ask=lambda prompt, **kwargs: f"ANSWER: {prompt}",
    )
    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)

    monkeypatch.setattr(system, "argv", ["agent", "ask", "hello"])
    cli.main()

    out = capsys.readouterr().out.strip()
    assert "ANSWER: hello" in out


# Test text and image question - image command.
def test_cli_image(monkeypatch, capsys, mocker):
    fake_agent = types.SimpleNamespace(
        ask_with_image=lambda prompt, img, **kwargs: f"IMAGE_ANSWER: {prompt}",
    )

    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)
    mocker.patch.object(cli, "load_image_as_part", return_value="FAKE_PART")

    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "image", "fake.jpg", "describe this"],
    )
    cli.main()
    out = capsys.readouterr().out.strip()
    assert "IMAGE_ANSWER: describe this" in out


# Test invalid image.
def test_cli_image_invalid(monkeypatch, caplog, mocker):
    monkeypatch.setattr(
        system,
        "argv",
        ["agent", "image", "bad.jpg", "prompt"],
    )

    # Do not let MultiModalAgent hit the real Google client
    fake_agent = mocker.Mock()
    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)
    # Force image loader to fail so we trigger InvalidImageError

    mocker.patch.object(
        cli,
        "load_image_as_part",
        side_effect=Exception("boom"),
    )

    # Route CLI l
    # Logger into caplog's handler so we can assert on log output
    logger = cli.logger
    logger.handlers = [caplog.handler]
    logger.setLevel("ERROR")

    with caplog.at_level("ERROR"):
        with pytest.raises(SystemExit) as exit_info:
            cli.main()

    # CLI should exit with code 1
    assert exit_info.value.code == 1

    # Collect log messages
    messages = [rec.getMessage() for rec in caplog.records]

    # The outer AgentError handler logs:
    # "Agent failed: Cannot read image: bad.jpg"
    assert any("Cannot read image: bad.jpg" in msg for msg in messages)


# Test chat command.
def test_cli_chat(monkeypatch, mocker):
    # New chat signature accepts session_id
    fake_agent = types.SimpleNamespace(chat=lambda session_id="default": None)
    mocker.patch.object(cli, "MultiModalAgent", return_value=fake_agent)

    monkeypatch.setattr(system, "argv", ["agent", "chat"])
    cli.main()  # should run without exception


def test_cli_no_command(monkeypatch, capsys):
    monkeypatch.setattr(system, "argv", ["agent"])
    cli.main()
    out = capsys.readouterr().out
    assert "usage:" in out.lower()


def test_cli_version_flag(capsys):
    parser = cli.build_parser()
    args = parser.parse_args(["--version"])
    assert args.version is True


def test_cli_ask_parser():
    parser = cli.build_parser()
    args = parser.parse_args(["ask", "hello"])
    assert args.command == "ask"
    assert args.prompt == "hello"
    assert args.no_rag is False


def test_cli_history_show_parser():
    parser = cli.build_parser()
    args = parser.parse_args(["history", "show"])
    assert args.command == "history"
    assert args.history_cmd == "show"

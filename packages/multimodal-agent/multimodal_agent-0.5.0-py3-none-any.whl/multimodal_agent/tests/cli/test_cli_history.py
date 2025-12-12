import sys as system
import types
from types import SimpleNamespace

import multimodal_agent.utils as utils
from multimodal_agent.cli import cli


def make_fake_store(chunks=None):
    return types.SimpleNamespace(
        get_recent_chunks=lambda limit: chunks or [],
        get_recent_chunk=lambda limit: chunks or [],
        delete_chunk=lambda chunk_id: None,
        clear_all=lambda: None,
        close=lambda: None,
    )


def test_cli_history_show_empty(monkeypatch, capsys):
    fake_store = make_fake_store([])
    monkeypatch.setattr(utils, "SQLiteRAGStore", lambda *a, **k: fake_store)

    monkeypatch.setattr(system, "argv", ["agent", "history", "show"])
    cli.main()
    output = capsys.readouterr().out
    assert "No history" in output


def test_cli_history_delete(monkeypatch, capsys):
    events = {"deleted": None}

    fake_store = make_fake_store()
    fake_store.delete_chunk = lambda chunk_id: events.update(deleted=chunk_id)

    monkeypatch.setattr(utils, "SQLiteRAGStore", lambda *a, **k: fake_store)
    monkeypatch.setattr(system, "argv", ["agent", "history", "delete", "2"])
    cli.main()

    assert events["deleted"] == 2


def test_cli_history_reset(monkeypatch, capsys):
    # reset is now "clear" because memory.json was removed
    fake_store = make_fake_store()
    monkeypatch.setattr(utils, "SQLiteRAGStore", lambda *a, **k: fake_store)

    monkeypatch.setattr(system, "argv", ["agent", "history", "clear"])
    cli.main()

    out = capsys.readouterr().out
    assert "History cleared" in out


def test_cli_history_summary(monkeypatch, capsys, mocker):
    chunk = SimpleNamespace(
        id=1,
        role="user",
        session_id="s1",
        content="hello",
        created_at="2024-01-01",
    )
    fake_store = make_fake_store([chunk])

    monkeypatch.setattr(utils, "SQLiteRAGStore", lambda *a, **k: fake_store)

    # Fake summarizer agent
    class FakeAgent:
        def __init__(self, *a, **k):
            pass

        def safe_generate_content(self, contents):
            class R:
                text = "summary ok"

            return R()

    mocker.patch("multimodal_agent.utils.MultiModalAgent", FakeAgent)

    monkeypatch.setattr(system, "argv", ["agent", "history", "summary"])
    cli.main()
    output = capsys.readouterr().out
    assert "summary ok" in output

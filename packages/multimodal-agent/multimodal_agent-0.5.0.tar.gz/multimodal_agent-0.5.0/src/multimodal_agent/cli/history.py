from multimodal_agent import utils
from multimodal_agent.cli.printing import print_markdown_with_meta
from multimodal_agent.rag.rag_store import default_db_path


#   HISTORY HANDLERS (RAG-Backed, Session-Aware)
def handle_history(args) -> int:
    """
    Dispatch RAG history operations.
    """
    store = utils.SQLiteRAGStore(default_db_path())
    try:
        if args.history_cmd == "show":
            return _show_history(args, store)
        elif args.history_cmd == "delete":
            return _delete_history(args, store)
        elif args.history_cmd == "clear":
            return _clear_history(args, store)
        elif args.history_cmd == "summary":
            return _summary_history(args, store)
        else:
            print(f"unknown history subcommand: {args.history_cmd}")
            return 1
    finally:
        store.close()


def _show_history(args, store: utils.SQLiteRAGStore) -> int:
    """
    Show stored history from RAG SQLite database.
    """
    chunks = store.get_recent_chunks(limit=args.limit)

    # Filter by session
    if getattr(args, "session", None):
        chunks = [c for c in chunks if c.session_id == args.session]

    if not chunks:
        print_markdown_with_meta(
            sections=[("History", "No history found.")],
            meta={
                "type": "history_show",
                "limit": args.limit,
                "session": getattr(args, "session", None),
                "count": 0,
            },
        )
        return 0

    lines: list[str] = []

    # Reverse chunks in chronological order and generate the content
    for chunk in reversed(chunks):
        session_id = chunk.session_id or "-"
        lines.append(
            f"[{chunk.id}] ({session_id}) {chunk.role} @ {chunk.created_at}",
        )
        # filter content length
        preview = chunk.content[:200]
        lines.append(preview)
        if len(chunk.content) > 200:
            print("  ...")
        lines.append("---")

    body = "\n".join(lines)

    # print content.
    print_markdown_with_meta(
        sections=[("History", body)],
        meta={
            "type": "history_show",
            "limit": args.limit,
            "session": getattr(args, "session", None),
            "count": len(chunks),
        },
    )
    return 0


def _clear_history(args, store: utils.SQLiteRAGStore) -> int:
    store.clear_all()
    print_markdown_with_meta(
        sections=[("History", "History cleared.")],
        meta={"type": "history_clear"},
    )
    return 0


def _delete_history(args, store: utils.SQLiteRAGStore) -> int:
    store.delete_chunk(chunk_id=args.chunk_id)
    print_markdown_with_meta(
        sections=[("History", f"Deleted chunk {args.chunk_id}.")],
        meta={
            "type": "history_delete",
            "chunk_id": args.chunk_id,
        },
    )
    return 0


def _summary_history(args, store: utils.SQLiteRAGStore) -> int:
    """
    Summarize recent history using the LLM.
    """
    chunks = store.get_recent_chunks(limit=args.limit)

    # Optional filtering
    if getattr(args, "session", None):
        chunks = [c for c in chunks if c.session_id == args.session]

    if not chunks:
        print_markdown_with_meta(
            sections=[("Summary", "No history to summarize.")],
            meta={
                "type": "history_summary",
                "limit": args.limit,
                "session": getattr(args, "session", None),
            },
        )
        return 0

    # Format history
    text = "\n".join(
        f"{'User' if ch.role=='user' else 'Assistant'}: {ch.content}"
        for ch in reversed(chunks)
    )

    # Use the same model as CLI
    agent = utils.MultiModalAgent(
        enable_rag=False,
        model=getattr(args, "model", "gemini-2.5-flash"),
    )

    # Call safe_generate_content directly so FakeAgent works during tests
    response = agent.safe_generate_content(
        [f"Summarize the following conversation:\n{text}"]
    )

    summary = response.text

    print_markdown_with_meta(
        sections=[("Summary", summary)],
        meta={
            "type": "history_summary",
            "limit": args.limit,
            "session": getattr(args, "session", None),
        },
    )
    return 0

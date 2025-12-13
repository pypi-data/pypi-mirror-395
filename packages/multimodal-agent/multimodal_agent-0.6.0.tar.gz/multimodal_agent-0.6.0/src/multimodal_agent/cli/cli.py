import argparse
import json
import os

import uvicorn
from dotenv import load_dotenv

from multimodal_agent.cli.history import handle_history
from multimodal_agent.cli.printing import print_markdown_with_meta
from multimodal_agent.errors import AgentError, InvalidImageError
from multimodal_agent.logger import get_logger
from multimodal_agent.project_scanner import (
    scan_project,
)
from multimodal_agent.rag.rag_store import SQLiteRAGStore, default_db_path
from multimodal_agent.utils import load_image_as_part
from multimodal_agent.version import __version__

# REMOVE ALL history imports from top-level!


# Load .env from the project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent",
        description="Multimodal Agent powered by Google Gemini",
    )
    # parser debug field
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    # parser model field.
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.5-flash",
        help="Specify which model to use",
    )
    # parser version field.
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )

    subparsers = parser.add_subparsers(dest="command")

    # agent ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a text-only question")
    ask_parser.add_argument("prompt", type=str, help="Your question")
    ask_parser.add_argument(
        "--no-rag",
        action="store_true",
        help="Disable RAG (ignore local memory)",
    )

    # format
    ask_parser.add_argument(
        "--format",
        action="store_true",
        help="Format output syntax.",
    )

    ask_parser.add_argument(
        "--json",
        action="store_true",
        help="Return output as JSON.",
    )

    ask_parser.add_argument(
        "--session", type=str, default=None, help="Session ID for this query"
    )

    # agent image command
    image_parser = subparsers.add_parser("image", help="Ask with image + text")
    image_parser.add_argument(
        "image_path",
        type=str,
        help="Path to local image",
    )
    image_parser.add_argument("prompt", type=str, help="Your question")
    image_parser.add_argument(
        "--session",
        type=str,
        default=None,
        help="Session ID for this query",
    )

    # format
    image_parser.add_argument(
        "--format",
        action="store_true",
        help="Format output syntax.",
    )

    image_parser.add_argument(
        "--json",
        action="store_true",
        help="Return output as JSON.",
    )

    # chat.
    chat_parser = subparsers.add_parser(
        "chat",
        help="Start interactive chat mode",
    )
    chat_parser.add_argument(
        "--no-rag",
        action="store_true",
        help="Disable RAG (ignore local memory)",
    )
    chat_parser.add_argument(
        "--session",
        type=str,
        default=None,
        help="Session ID for this chat session",
    )

    # history parent command
    history_parser = subparsers.add_parser(
        "history",
        help="Manage agent memory / history",
    )

    history_subparsers = history_parser.add_subparsers(
        dest="history_cmd",
        required=True,
    )

    # history show
    show_parser = history_subparsers.add_parser(
        "show",
        help="Show recent chunks stored in memory",
    )

    show_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Number of recent entries to show",
    )

    show_parser.add_argument(
        "--session",
        type=str,
        default=None,
        help="Filter by session id",
    )

    show_parser.add_argument(
        "--clean",
        action="store_true",
        help="Hide noise messages (FAKE_RESPONSE, project_profile, and test messages).",  # noqa
    )

    # history clear
    history_subparsers.add_parser(
        "clear",
        help="Filter by session id",
    )

    # summary parser
    summary_parser = history_subparsers.add_parser(
        "summary",
        help="Summarize memory using the agent",
    )
    summary_parser.add_argument(
        "--session",
        type=str,
        default=None,
        help="Filter by session id",
    )

    summary_parser.add_argument(
        "--limit",
        type=int,
        default=50,
    )

    # delete
    delete_parser = history_subparsers.add_parser(
        "delete",
        help="Delete a specific memory chunk by ID",
    )
    delete_parser.add_argument("chunk_id", type=int)

    # learning
    learning_parser = subparsers.add_parser("learn-project")
    learning_parser.add_argument("path")
    learning_parser.add_argument("--project-id", "-p")
    learning_parser.add_argument("--no-store", action="store_true")

    # list projects
    subparsers.add_parser("list-projects")

    show_parser = subparsers.add_parser("show-project")
    show_parser.add_argument("project_id")

    inspect_parser = subparsers.add_parser("inspect-project")
    inspect_parser.add_argument("path")

    # server
    server_parser = subparsers.add_parser(
        "server",
        help="Run agent API server",
    )
    server_parser.add_argument("--port", type=int, default=8000)

    return parser


def handle_text(agent, question, debug=False, response_format="text"):
    response = agent.ask(question, response_format=response_format)

    if response_format == "json":
        print(json.dumps(response.data, indent=2))
    else:
        print(response.text)

    if response.usage and debug:
        print(
            f"[usage] prompt={response.usage.get('prompt_tokens')} "
            f"response={response.usage.get('response_tokens')} "
            f"total={response.usage.get('total_tokens')}"
        )


def handle_image(agent, image, question, debug=False, response_format="text"):
    response = agent.ask_with_image(
        question,
        image,
        response_format=response_format,
    )

    if response_format == "json":
        print(json.dumps(response.data, indent=2))
    else:
        print(response.text)

    if response.usage and debug:
        print(
            f"[usage] prompt={response.usage.get('prompt_tokens')} "
            f"response={response.usage.get('response_tokens')} "
            f"total={response.usage.get('total_tokens')}"
        )


def test_main(argv=None):
    """
    Wrapper used by tests: behaves like a Click command but delegates to
    argparse.
    """
    parser = build_parser()
    args = parser.parse_args(argv or [])
    return _main(args, parser)


def main():
    parser = build_parser()
    args = parser.parse_args()
    return _main(args, parser)


def _main(args, parser):
    from multimodal_agent.core.agent_core import MultiModalAgent

    if args.version:
        print(f"multimodal-agent version {__version__}")
        return 0

    if args.debug:
        os.environ["LOGLEVEL"] = "DEBUG"
        logger.setLevel("DEBUG")

    if not args.command:
        parser.print_help()
        return 0

    needs_agent = args.command in {
        "ask",
        "image",
        "chat",
        "server",
        "learn-project",
        "list-projects",
        "show-project",
    }
    agent = None

    if needs_agent:
        # Create agent instance
        enable_rag = not getattr(args, "no_rag", False)
        # create agent instance
        agent = MultiModalAgent(model=args.model, enable_rag=enable_rag)

    try:
        # asking question in text.
        if args.command == "ask":
            formatted = getattr(args, "format", False)
            json_mode = getattr(args, "json", False)
            response_format = "json" if json_mode else "text"

            response = agent.ask(
                args.prompt,
                response_format=response_format,
                formatted=formatted,
            )

            # chat output.
            if hasattr(response, "text"):
                text = response.text
            else:
                text = str(response)

            print_markdown_with_meta(
                sections=[
                    ("Question", args.prompt),
                    ("Answer", text),
                ],
                meta={
                    "type": "ask",
                    "command": "ask",
                    "model": args.model,
                    "rag_enabled": enable_rag,
                },
            )

            return 0
        # Image questions.
        elif args.command == "image":
            try:
                image_as_part = load_image_as_part(args.image_path)
            except Exception:
                raise InvalidImageError(
                    f"Cannot read image: {args.image_path}",
                )

            formatted = getattr(args, "format", False)
            json_mode = getattr(args, "json", False)
            response_format = "json" if json_mode else "text"
            response = agent.ask_with_image(
                args.prompt,
                image_as_part,
                response_format=response_format,
                formatted=formatted,
            )

            # chat output.
            if hasattr(response, "text"):
                text = response.text
            else:
                text = str(response)
            print_markdown_with_meta(
                sections=[
                    ("Question", args.prompt),
                    ("Answer", text),
                ],
                meta={
                    "type": "image",
                    "command": "image",
                    "model": args.model,
                    "rag_enabled": enable_rag,
                    "image_path": args.image_path,
                },
            )
            return 0

        # chat mode.
        if args.command == "chat":
            agent.chat(session_id=args.session)
            return 0

        # history mode.
        elif args.command == "history":
            db_path = os.environ.get("MULTIMODAL_AGENT_DB", default_db_path())
            store = SQLiteRAGStore(db_path=db_path)

            return handle_history(args, store)

        # server mode.
        elif args.command == "server":
            uvicorn.run(
                "multimodal_agent.server:app",
                host="127.0.0.1",
                port=args.port,
                reload=False,
            )
            return 0

        # learn project.
        elif args.command == "learn-project":
            profile = scan_project(args.path)
            print(json.dumps(profile.to_dict(), indent=2))

            if not args.no_store:
                project_id = (
                    args.project_id or f"project:{profile.package_name}"
                )  # noqa
                agent.rag_store.add_logical_message(
                    content=json.dumps(profile.to_dict()),
                    role="project_profile",
                    session_id=project_id,
                    source="project-learning",
                )
                print(f"Stored as: {project_id}")
            return 0

        # LIST PROJECTS
        elif args.command == "list-projects":
            rows = agent.rag_store.get_project_profiles()
            print("Stored Project Profiles")
            for row in rows:
                print(f"- {row['session_id']} (created {row['created_at']})")
            return 0

        # SHOW PROJECT
        elif args.command == "show-project":
            db_path = os.environ.get("MULTIMODAL_AGENT_DB", default_db_path())
            store = SQLiteRAGStore(db_path=db_path)

            profile = store.load_project_profile(args.project_id)
            if profile is None:
                print("Profile not found")
                return 0

            print(json.dumps(profile, indent=2))
            return 0

        # INSPECT PROJECT
        elif args.command == "inspect-project":
            profile = scan_project(args.path)
            print(json.dumps(profile.to_dict(), indent=2))
            return 0

    except AgentError as exception:
        logger.error(f"Agent failed: {exception}")
        return 1

    return 0

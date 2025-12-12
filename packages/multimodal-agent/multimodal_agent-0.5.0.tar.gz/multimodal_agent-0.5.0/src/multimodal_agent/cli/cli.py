import argparse
import json
import os
import sys as system

import uvicorn
from dotenv import load_dotenv

from multimodal_agent import __version__
from multimodal_agent.cli.history import (
    handle_history,
    print_markdown_with_meta,
)
from multimodal_agent.core.agent_core import MultiModalAgent
from multimodal_agent.errors import AgentError, InvalidImageError
from multimodal_agent.logger import get_logger
from multimodal_agent.utils import (
    load_image_as_part,
)

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

    # agent command.
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

    # history clear
    history_subparsers.add_parser(
        "clear",
        help="Filter by session id",
    )

    # history delete
    delete_parser = history_subparsers.add_parser(
        "delete",
        help="Delete a specific chunk by id",
    )

    delete_parser.add_argument("chunk_id", type=int)

    # history summary

    history_parser = history_subparsers.add_parser(
        "summary",
        help="Summarize conversation history",
    )
    history_parser.add_argument(
        "--limit",
        type=int,
        default=50,
    )
    history_parser.add_argument(
        "--session",
        type=str,
        default=None,
    )

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


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"multimodal-agent version {__version__}")
        return

    if args.debug:
        os.environ["LOGLEVEL"] = "DEBUG"
        logger.setLevel("DEBUG")

    if not args.command:
        parser.print_help()
        return

    enable_rag = not getattr(args, "no_rag", False)

    # create agent instance
    agent = MultiModalAgent(
        model=args.model,
        enable_rag=enable_rag,
    )

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

            return
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
            return
        # chat mode.
        elif args.command == "chat":
            agent.chat(session_id=args.session)
            return

        # history mode.
        elif args.command == "history":
            return handle_history(args=args)

        elif args.command == "server":
            uvicorn.run(
                "multimodal_agent.server:app",
                host="127.0.0.1",
                port=args.port,
                reload=False,
            )

    except AgentError as exception:
        logger.error(f"Agent failed: {exception}")
        system.exit(1)

#!/usr/bin/env python3
"""
04 - Interactive Demo: Meet Jake, Your Dakora Support Agent

An interactive demo showcasing a conversational AI agent with documentation
retrieval capabilities. Perfect for recordings and demonstrations.

WHAT THIS SHOWS:
- Interactive conversational agent with personality
- Real-time documentation retrieval
- Beautiful terminal UI with colors and animations
- Continuous conversation loop
- Full observability with trace tracking

PREREQUISITES:
    pip install 'dakora-instrumentation[maf]' rich

ENVIRONMENT VARIABLES:
    DAKORA_API_KEY - Your Dakora project API key
    OPENAI_API_KEY - Your OpenAI API key
    DAKORA_BASE_URL - Optional: Dakora server URL (default: https://api.dakora.io/)
    DAKORA_STUDIO_URL - Optional: Dakora Studio URL (default: https://playground.dakora.io/)
    DAKORA_WEBSITE_URL - Optional: Dakora website URL (default: https://dakora.io)
    DAKORA_DOCS_URL - Optional: Dakora docs URL (default: https://docs.dakora.io)

USAGE:
    # Interactive mode (default)
    python 04_interactive_demo.py

    # Demo mode with pre-scripted questions (great for recordings!)
    python 04_interactive_demo.py --demo

DEMO FLOW:
    1. Jake introduces himself with a cool banner
    2. Ask questions about Dakora (or let demo mode auto-type them)
    3. Jake fetches docs and responds with helpful info
    4. See response metrics (latency, tokens)
    5. Get trace IDs to view in Dakora Studio
    6. Continue the conversation or type 'exit' to quit
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, AsyncIterator

# Platform-specific keyboard input
if sys.platform == "win32":
    import msvcrt

    _WINDOWS = True
else:
    import termios
    import tty

    _WINDOWS = False

if TYPE_CHECKING:
    from collections.abc import Callable

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from dakora_instrumentation.frameworks.maf import DakoraIntegration
from dotenv import load_dotenv
from pydantic import Field
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from dakora import Dakora

load_dotenv()

logger = logging.getLogger(__name__)


class ExitCommand(Enum):
    """Valid exit commands for the conversation loop."""

    EXIT = "exit"
    QUIT = "quit"
    BYE = "bye"
    GOODBYE = "goodbye"

    @classmethod
    def is_exit_command(cls, text: str) -> bool:
        """Check if the given text is an exit command."""
        return text.lower() in {cmd.value for cmd in cls}


class KeyInput(Enum):
    """Keyboard input types for interactive menu."""

    UP = "up"
    DOWN = "down"
    ENTER = "enter"
    QUIT = "quit"
    OTHER = "other"


@dataclass(frozen=True)
class FollowupOption:
    """Represents a follow-up option in the interactive menu."""

    icon: str
    title: str
    subtitle: str


@dataclass
class DemoConfig:
    """Configuration for the demo session."""

    demo_mode: bool = False
    dakora_api_key: str = field(default_factory=lambda: os.getenv("DAKORA_API_KEY", ""))
    dakora_base_url: str = field(
        default_factory=lambda: os.getenv("DAKORA_BASE_URL", "https://api.dakora.io/")
    )
    dakora_studio_url: str = field(
        default_factory=lambda: os.getenv(
            "DAKORA_STUDIO_URL", "https://playground.dakora.io/"
        )
    )
    dakora_website_url: str = field(
        default_factory=lambda: os.getenv("DAKORA_WEBSITE_URL", "https://dakora.io")
    )
    dakora_docs_url: str = field(
        default_factory=lambda: os.getenv("DAKORA_DOCS_URL", "https://docs.dakora.io")
    )
    openai_model: str = field(
        default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    docs_path: Path = field(
        default_factory=lambda: Path(__file__).parent.parent.parent.parent.parent
        / "docs"
    )

    # Fast timing values (always used)
    typing_delay: float = 0.005
    pause_delay: float = 0.1
    banner_delay: float = 0.02

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors: list[str] = []
        if not self.dakora_api_key:
            errors.append("DAKORA_API_KEY environment variable is required")
        if not os.getenv("OPENAI_API_KEY"):
            errors.append("OPENAI_API_KEY environment variable is required")
        if not self.docs_path.exists():
            errors.append(f"Documentation path not found: {self.docs_path}")
        return errors


@dataclass
class ConversationState:
    """Tracks state for a conversation session."""

    trace_id: str | None = None
    last_doc_fetched: str | None = None
    conversation_count: int = 0
    demo_question_index: int = 0

    def new_turn(self) -> None:
        """Reset state for a new conversation turn."""
        self.last_doc_fetched = None
        self.trace_id = f"trace_{uuid.uuid4().hex[:12]}"
        self.conversation_count += 1


DEMO_QUESTIONS: tuple[str, ...] = ("What is Dakora and why should I use it?",)


def get_followup_options(config: DemoConfig) -> tuple[FollowupOption, ...]:
    """Get follow-up options with URLs from config."""
    return (
        FollowupOption(
            "1.",
            "Sign up for free",
            f"[link={config.dakora_website_url}]{config.dakora_website_url}[/link]",
        ),
        FollowupOption("2.", "Install the package", "pip install dakora-client"),
        FollowupOption(
            "3.",
            "Try the Playground",
            f"Test prompts interactively in [link={config.dakora_studio_url}]Studio[/link]",
        ),
        FollowupOption("4.", "Ask another question", "Learn something new"),
        FollowupOption("5.", "Exit", "End conversation"),
    )


DOCS_MAPPING: dict[str, str] = {
    "quickstart": "getting-started/quickstart.mdx",
    "getting started": "getting-started/quickstart.mdx",
    "introduction": "getting-started/introduction.mdx",
    "overview": "getting-started/introduction.mdx",
    "what is dakora": "getting-started/introduction.mdx",
    "templates": "concepts/templates.mdx",
    "prompts": "concepts/templates.mdx",
    "inputs": "concepts/inputs.mdx",
    "versioning": "concepts/versioning.mdx",
    "logging": "features/logging.mdx",
    "tracking": "features/logging.mdx",
    "observability": "features/logging.mdx",
    "cli": "features/cli.mdx",
    "integrations": "features/integrations.mdx",
    "playground": "features/playground.mdx",
    "model comparison": "features/model-comparison.mdx",
    "compare models": "features/model-comparison.mdx",
    "api keys": "guides/api-keys.mdx",
    "authentication": "guides/authentication.mdx",
    "budgets": "guides/project-budgets.mdx",
}

MAX_DOC_CONTENT_LENGTH = 3000
MENU_HEADER_LINES = 3
MENU_LINES_PER_OPTION = 3

JAKE_BANNER = """
    ╔═════════════════════════════════════════════════════╗
    ║                                                     ║
    ║        ██╗ █████╗ ██╗  ██╗███████╗                  ║
    ║        ██║██╔══██╗██║ ██╔╝██╔════╝                  ║
    ║        ██║███████║█████╔╝ █████╗                    ║
    ║   ██   ██║██╔══██║██╔═██╗ ██╔══╝                    ║
    ║   ╚█████╔╝██║  ██║██║  ██╗███████╗                  ║
    ║    ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝                  ║
    ║                                                     ║
    ║           Your Dakora Support Agent                 ║
    ║                                                     ║
    ╚═════════════════════════════════════════════════════╝
"""


def _find_doc_file(topic_lower: str) -> str | None:
    """Find documentation file for a given topic using exact or partial matching."""
    doc_file = DOCS_MAPPING.get(topic_lower)
    if doc_file:
        return doc_file

    for key, value in DOCS_MAPPING.items():
        if topic_lower in key or key in topic_lower:
            return value

    return None


def create_docs_tool(
    config: DemoConfig, state: ConversationState
) -> Callable[[str], str]:
    """
    Create a documentation retrieval tool with injected dependencies.

    This factory pattern allows the tool to access config and state without
    relying on global variables.
    """

    def get_docs(
        topic: Annotated[
            str,
            Field(
                description="The documentation topic to retrieve. Available topics: "
                "quickstart, getting started, introduction, overview, templates, "
                "inputs, versioning, logging, cli, integrations, playground, "
                "model comparison, api keys, authentication, budgets"
            ),
        ],
    ) -> str:
        """
        Retrieve Dakora documentation for a specific topic.

        This tool reads documentation from the local docs folder to provide
        accurate, up-to-date information about Dakora features and usage.
        """
        topic_lower = topic.lower().strip()

        doc_file = _find_doc_file(topic_lower)
        if not doc_file:
            available = ", ".join(sorted(set(DOCS_MAPPING.keys())))
            return f"Topic '{topic}' not found. Available topics: {available}"

        doc_path = config.docs_path / doc_file

        if not doc_path.exists():
            logger.warning("Documentation file not found: %s", doc_file)
            return f"Documentation file not found: {doc_file}"

        try:
            content = doc_path.read_text(encoding="utf-8")
            state.last_doc_fetched = doc_file
            if len(content) > MAX_DOC_CONTENT_LENGTH:
                content = content[:MAX_DOC_CONTENT_LENGTH] + "\n\n... (truncated)"
            return f"# Documentation: {topic}\n\nSource: {doc_file}\n\n{content}"
        except OSError as e:
            logger.exception("Error reading documentation file: %s", doc_file)
            return f"Error reading documentation: {e}"

    return get_docs


class TerminalUI:
    """Handles all terminal UI interactions with proper encapsulation."""

    def __init__(self, config: DemoConfig) -> None:
        self.config = config
        self.console = Console()
        self._followup_options = get_followup_options(config)

    def clear(self) -> None:
        """Clear the terminal screen."""
        self.console.clear()

    def print_banner(self) -> None:
        """Display the Jake ASCII banner with fade-in effect."""
        lines = JAKE_BANNER.split("\n")
        for line in lines:
            self.console.print(line, style="bold #FF896B")
            time.sleep(self.config.banner_delay)

    def print_jake_intro(self, message: str) -> None:
        """Print Jake's intro messages with typing effect."""
        self.console.print("\n[bold #FF896B]Jake:[/bold #FF896B] ", end="")
        for char in message:
            self.console.print(char, style="white", end="")
            sys.stdout.flush()
            time.sleep(self.config.typing_delay)
        self.console.print("\n")

    def print_jake_response(self, message: str) -> None:
        """Print Jake's AI response with markdown rendering."""
        self.console.print("\n[bold #FF896B]Jake:[/bold #FF896B]")
        self.console.print(Markdown(message))
        self.console.print()

    def print_jake_quick(self, message: str) -> None:
        """Print Jake's message without animation (for fast mode)."""
        self.console.print(f"\n[bold #FF896B]Jake:[/bold #FF896B] {message}\n")

    def get_user_input(self) -> str:
        """Print the user input prompt and get input."""
        self.console.print("[bold yellow]You:[/bold yellow] ", end="")
        try:
            return input().strip()
        except EOFError:
            return "exit"

    def auto_type_question(self, question: str) -> None:
        """Auto-type a question for demo mode."""
        self.console.print("[bold yellow]You:[/bold yellow] ", end="")
        for char in question:
            self.console.print(char, style="white", end="")
            sys.stdout.flush()
            time.sleep(0.02)
        self.console.print()
        time.sleep(self.config.pause_delay)

    def print_response_metrics(
        self,
        tokens_in: int,
        tokens_out: int,
        doc_fetched: str | None,
    ) -> None:
        """Print response metrics after Jake's response."""
        metrics_parts = [
            f"tokens in: {tokens_in}",
            f"tokens out: {tokens_out}",
        ]
        if doc_fetched:
            metrics_parts.append(f"doc: {doc_fetched}")
        metrics_parts.append(
            f"[link={self.config.dakora_studio_url}/project/default/executions]View in Studio[/link]"
        )

        metrics_line = "  |  ".join(metrics_parts)
        self.console.print(f"[dim]{metrics_line}[/dim]")

    def print_template_info(self, template_name: str, version: int | str) -> None:
        """Print template usage info."""
        self.console.print(f"[dim]   Using template: {template_name} v{version}[/dim]")

    def print_template_fallback_warning(self) -> None:
        """Print warning when falling back to default instructions."""
        self.console.print(
            "[dim]   Template not found, using default instructions[/dim]"
        )

    def print_error(self, message: str, details: str | None = None) -> None:
        """Print an error message."""
        self.console.print(f"\n[red]Error: {message}[/red]\n")
        if details:
            self.console.print(f"[dim]{details}[/dim]\n")

    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        self.console.print(f"[yellow]Warning: {message}[/yellow]")

    def print_tip(self, message: str) -> None:
        """Print a helpful tip."""
        self.console.print(f"[dim]   Tip: {message}[/dim]\n")

    def print_status(self, message: str) -> None:
        """Print a status message."""
        self.console.print(f"\n[dim]{message}[/dim]")

    def show_spinner(self, message: str) -> Any:
        """Show a spinner with the given message. Returns context manager."""
        return self.console.status(f"[#FF896B]{message}", spinner="dots")

    def print_session_summary(self, conversation_count: int) -> None:
        """Print the session summary panel."""
        self.console.print(
            Panel(
                f"[#FF896B]Session Complete![/#FF896B]\n\n"
                f"Questions answered: {conversation_count}\n"
                f"View traces: [link={self.config.dakora_studio_url}]"
                f"{self.config.dakora_studio_url}[/link]\n\n"
                f"[dim]All conversations were traced and sent to Dakora![/dim]",
                title="Demo Stats",
                border_style="#FF896B",
            )
        )

    def print_goodbye(self) -> None:
        """Print goodbye message on interrupt."""
        self.console.print("\n\n[yellow]Interrupted. See you next time![/yellow]")

    def _get_key(self) -> KeyInput:
        """Get a single keypress from the user."""
        if _WINDOWS:
            key = msvcrt.getch()
            if key == b"\xe0":
                key = msvcrt.getch()
                if key == b"H":
                    return KeyInput.UP
                elif key == b"P":
                    return KeyInput.DOWN
            elif key == b"\r":
                return KeyInput.ENTER
            elif key in (b"q", b"\x03"):
                return KeyInput.QUIT
            return KeyInput.OTHER
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == "\x1b":
                    ch2 = sys.stdin.read(1)
                    ch3 = sys.stdin.read(1)
                    if ch2 == "[" and ch3 == "A":
                        return KeyInput.UP
                    elif ch2 == "[" and ch3 == "B":
                        return KeyInput.DOWN
                elif ch in ("\r", "\n"):
                    return KeyInput.ENTER
                elif ch in ("q", "\x03"):
                    return KeyInput.QUIT
                return KeyInput.OTHER
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _render_options(self, selected_index: int) -> list[str]:
        """Render the options menu with the selected item highlighted."""
        lines: list[str] = []
        lines.append(
            "[dim]-------------------------------------------------------[/dim]"
        )
        lines.append("[bold #FF896B]What would you like to do next?[/bold #FF896B]")
        lines.append("")

        for i, option in enumerate(self._followup_options):
            if i == selected_index:
                lines.append(
                    f"   [bold #FF896B]> {option.icon}  {option.title}[/bold #FF896B]"
                )
                lines.append(f"       [#FF896B]{option.subtitle}[/#FF896B]")
            else:
                lines.append(f"   [dim]  {option.icon}  {option.title}[/dim]")
                lines.append(f"       [dim]{option.subtitle}[/dim]")
            lines.append("")

        return lines

    def interactive_option_selector(self) -> int:
        """Display interactive option selector with arrow key navigation."""
        selected_index = 0
        num_options = len(self._followup_options)
        menu_height = MENU_HEADER_LINES + (num_options * MENU_LINES_PER_OPTION)

        lines = self._render_options(selected_index)
        for line in lines:
            self.console.print(line)

        while True:
            key = self._get_key()

            if key == KeyInput.UP:
                selected_index = (selected_index - 1) % num_options
            elif key == KeyInput.DOWN:
                selected_index = (selected_index + 1) % num_options
            elif key == KeyInput.ENTER:
                self.console.print()
                return selected_index
            elif key == KeyInput.QUIT:
                return -1
            else:
                continue

            sys.stdout.write(f"\033[{menu_height}A")
            sys.stdout.write("\033[J")
            sys.stdout.flush()

            lines = self._render_options(selected_index)
            for line in lines:
                self.console.print(line)

    def print_followup_options(self) -> None:
        """Print follow-up option buttons with interactive selection."""
        selected = self.interactive_option_selector()

        if selected >= 0:
            option = self._followup_options[selected]
            self.console.print(f"[bold #FF896B]Selected: {option.title}[/bold #FF896B]")
            self.console.print(f"[dim]  -> {option.subtitle}[/dim]\n")


class JakeAgentFactory:
    """Factory for creating Jake agent instances."""

    def __init__(
        self,
        config: DemoConfig,
        state: ConversationState,
        dakora: Dakora,
        middleware: Any,
        ui: TerminalUI,
    ) -> None:
        self.config = config
        self.state = state
        self.dakora = dakora
        self.middleware = middleware
        self.ui = ui
        self._docs_tool = create_docs_tool(config, state)

    def _get_default_instructions(self, question: str) -> str:
        """Get default instructions template with config values."""
        return f"""You are Jake, a friendly and knowledgeable Dakora support agent.
You're enthusiastic about helping developers get the most out of Dakora.

Current question: {question}

When users ask questions:
1. Use the get_docs tool to retrieve accurate documentation
2. Provide SHORT, high-level answers (1-2 paragraphs, 3-4 sentences max)
3. DO NOT include code examples or detailed code snippets
4. Focus on explaining WHAT something does and WHY it's useful
5. Always direct users to {self.config.dakora_docs_url} for full details and code examples
6. End with asking if they have more questions

Your personality:
- Friendly and approachable (like a helpful colleague)
- Enthusiastic about Dakora's features
- Patient and understanding with beginners
- Professional but not stuffy
- Concise and to-the-point

You have access to the get_docs tool to retrieve official documentation.
Use it to understand the topic, but provide only a concise summary in your response."""

    def _get_response_guidelines(self) -> str:
        """Get response guidelines with config values."""
        return f"""
IMPORTANT RESPONSE GUIDELINES:
- Keep responses SHORT and high-level (1-2 paragraphs max, 3-4 sentences)
- DO NOT include code examples or detailed code snippets
- Focus on explaining WHAT something does and WHY it's useful
- Always end by directing users to visit {self.config.dakora_docs_url} for full details and code examples
- End by asking if they have more questions
- Be enthusiastic about Dakora's features

You have access to the get_docs tool to retrieve official documentation.
Use it to understand the topic, but provide only a concise summary in your response."""

    async def create(self, user_question: str) -> ChatAgent:
        """Create and configure Jake, the support agent."""
        instructions = await self._get_instructions(user_question)

        jake = ChatAgent(
            id="jake-support-agent-v1",
            name="Jake",
            chat_client=OpenAIChatClient(model_id=self.config.openai_model),
            instructions=instructions,
            middleware=[self.middleware],
            tools=[self._docs_tool],
        )

        return jake

    async def _get_instructions(self, user_question: str) -> str:
        """Get agent instructions, trying template first, then fallback."""
        try:
            faq_instructions = await self.dakora.prompts.render(
                "faq_responder",
                {
                    "question": user_question,
                    "knowledge_base": self._get_knowledge_base_description(),
                    "tone": "friendly and enthusiastic, like a helpful colleague named Jake",
                    "include_sources": True,
                },
            )

            self.ui.print_template_info("faq_responder", faq_instructions.version)

            return f"""You are Jake, a friendly and knowledgeable Dakora support agent.

{faq_instructions.text}

{self._get_response_guidelines()}"""

        except Exception as e:
            logger.debug("Template rendering failed: %s", e)
            self.ui.print_template_fallback_warning()
            return self._get_default_instructions(user_question)

    @staticmethod
    def _get_knowledge_base_description() -> str:
        """Get the knowledge base description for the agent."""
        return """Use the get_docs tool to fetch the latest Dakora documentation.
The documentation contains accurate, up-to-date information about:
- Getting started with Dakora
- Templates and prompt management
- API keys and authentication
- Logging and observability features
- Integrations and SDK usage"""


class InteractiveDemo:
    """Main demo application orchestrating all components."""

    def __init__(self, config: DemoConfig) -> None:
        self.config = config
        self.state = ConversationState()
        self.ui = TerminalUI(config)
        self._dakora: Dakora | None = None
        self._middleware: Any = None
        self._agent_factory: JakeAgentFactory | None = None

    @asynccontextmanager
    async def _setup_dakora(self) -> AsyncIterator[Dakora]:
        """Set up and tear down Dakora client with proper resource management."""
        dakora = Dakora(
            api_key=self.config.dakora_api_key,
            base_url=self.config.dakora_base_url,
        )
        try:
            yield dakora
        finally:
            DakoraIntegration.force_flush()
            await dakora.close()

    def _show_intro(self) -> None:
        """Display the intro sequence."""
        self.ui.clear()
        self.ui.print_banner()
        time.sleep(self.config.pause_delay)

        self.ui.print_jake_quick(
            "Hey! I'm Jake, your Dakora support agent. Ask me anything!"
        )

        time.sleep(self.config.pause_delay)

        if not self.config.demo_mode:
            self.ui.print_tip("Type 'exit' or 'quit' to end the conversation")

    def _get_next_question(self) -> str | None:
        """Get the next question from user or demo script."""
        if self.config.demo_mode:
            if self.state.demo_question_index >= len(DEMO_QUESTIONS):
                return None
            question = DEMO_QUESTIONS[self.state.demo_question_index]
            self.state.demo_question_index += 1
            self.ui.auto_type_question(question)
            return question
        else:
            return self.ui.get_user_input()

    async def _process_question(
        self, user_message: str, agent_factory: JakeAgentFactory
    ) -> bool:
        """Process a single question. Returns False if conversation should end."""
        if ExitCommand.is_exit_command(user_message):
            self._show_goodbye()
            return False

        if not user_message:
            return True

        self.state.new_turn()

        try:
            with self.ui.show_spinner("Jake is thinking and checking the docs..."):
                jake = await agent_factory.create(user_message)
                result = await jake.run(user_message)

            if not result or not result.messages:
                self.ui.print_error("No response received from Jake")
                return True

            response_text = result.messages[-1].text
            if not response_text:
                self.ui.print_error("Empty response from Jake")
                return True

            self.ui.print_jake_response(response_text)

            tokens_in = len(user_message.split()) * 2 + 150
            tokens_out = len(response_text.split()) + 50
            self.ui.print_response_metrics(
                tokens_in,
                tokens_out,
                self.state.last_doc_fetched,
            )

            if self.config.demo_mode and self.state.conversation_count == 1:
                self.ui.print_followup_options()

        except Exception as e:
            logger.exception("Error processing question")
            self.ui.print_error(f"Something went wrong: {e}")
            self.ui.print_jake_intro(
                "Sorry about that! Could you try asking your question again?"
            )

        time.sleep(self.config.pause_delay)

        if self.config.demo_mode:
            time.sleep(1.0)

        return True

    def _show_goodbye(self) -> None:
        """Show the goodbye message."""
        self.ui.print_jake_intro(
            "Thanks for chatting! Feel free to come back anytime you need help "
            "with Dakora. Happy coding!"
        )

    async def run(self) -> None:
        """Run the interactive demo."""
        errors = self.config.validate()
        if errors:
            for error in errors:
                self.ui.print_error(error)
            sys.exit(1)

        async with self._setup_dakora() as dakora:
            middleware = DakoraIntegration.setup(dakora, enable_sensitive_data=True)
            agent_factory = JakeAgentFactory(
                self.config, self.state, dakora, middleware, self.ui
            )

            self._show_intro()

            while True:
                user_message = self._get_next_question()
                if user_message is None:
                    break

                should_continue = await self._process_question(
                    user_message, agent_factory
                )
                if not should_continue:
                    break

            self.ui.print_session_summary(self.state.conversation_count)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Jake - Your Dakora Support Agent Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python 04_interactive_demo.py              # Interactive mode
  python 04_interactive_demo.py --demo       # Auto-type demo questions
        """,
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode with pre-scripted questions that auto-type",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for the demo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    args = parse_args()
    config = DemoConfig(demo_mode=args.demo)
    demo = InteractiveDemo(config)

    try:
        asyncio.run(demo.run())
    except KeyboardInterrupt:
        demo.ui.print_goodbye()
        sys.exit(0)


if __name__ == "__main__":
    main()

"""Chat command for ThreatWinds Pentest CLI.

Allows users to ask questions about completed pentest results using AI.
"""

import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from twpt_cli.config import load_credentials, get_api_endpoint
from twpt_cli.sdk import HTTPClient

console = Console()


@click.command()
@click.argument('pentest_id')
@click.argument('question', required=False)
@click.option(
    '--interactive', '-i',
    is_flag=True,
    help='Start an interactive chat session'
)
def chat(pentest_id: str, question: str, interactive: bool):
    """Ask questions about a completed pentest using AI.

    The AI analyzes the evidence files and provides explanations about
    vulnerabilities, exploitation results, and remediation recommendations.

    PENTEST_ID: The unique identifier of the pentest to query (e.g., swift-falcon-strikes).
    QUESTION: Your question about the pentest results (optional if using -i).

    Examples:
        twpt-cli chat swift-falcon-strikes "What vulnerabilities were found?"
        twpt-cli chat dark-storm-rises "Explain the SQL injection"
        twpt-cli chat cyber-hawk-hunts -i  # Interactive mode
    """
    # Load credentials
    creds = load_credentials()
    if not creds:
        console.print("✗ Not configured. Please run: twpt-cli configure", style="red")
        sys.exit(1)

    # Create client
    try:
        client = HTTPClient(get_api_endpoint(), creds)
    except Exception as e:
        console.print(f"✗ Failed to connect: {e}", style="red")
        sys.exit(1)

    if interactive:
        # Interactive chat mode
        run_interactive_chat(client, pentest_id)
    elif question:
        # Single question mode
        ask_question(client, pentest_id, question)
    else:
        console.print("✗ Please provide a question or use -i for interactive mode", style="red")
        console.print("Example: twpt-cli chat swift-falcon-strikes \"What vulnerabilities were found?\"", style="dim")
        sys.exit(1)


def ask_question(client: HTTPClient, pentest_id: str, question: str):
    """Ask a single question about a pentest.

    Args:
        client: HTTP client instance
        pentest_id: Pentest identifier
        question: Question to ask
    """
    console.print(f"\n[cyan]Analyzing pentest {pentest_id}...[/cyan]\n")

    try:
        # Show a spinner while waiting for AI response
        with console.status("[bold cyan]AI is analyzing evidence files..."):
            result = client.chat_with_pentest(pentest_id, question, timeout=180)

        if result.get('success'):
            # Display the answer
            answer = result.get('answer', 'No answer provided')

            console.print(Panel(
                Markdown(answer),
                title="[bold cyan]AI Analysis[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            ))
        else:
            error_msg = result.get('error', 'Unknown error')
            console.print(f"✗ {error_msg}", style="red")
            sys.exit(1)

    except Exception as e:
        console.print(f"✗ Failed to get response: {e}", style="red")
        sys.exit(1)


def run_interactive_chat(client: HTTPClient, pentest_id: str):
    """Run an interactive chat session.

    Args:
        client: HTTP client instance
        pentest_id: Pentest identifier
    """
    console.print("\n╔══════════════════════════════════════════════╗", style="cyan")
    console.print("║        Interactive Pentest Chat              ║", style="cyan")
    console.print("╚══════════════════════════════════════════════╝\n", style="cyan")

    console.print(f"Pentest ID: [bold]{pentest_id}[/bold]")
    console.print("Type your questions below. Type 'exit' or 'quit' to end.\n", style="dim")

    # Example questions
    console.print("[dim]Example questions:[/dim]")
    console.print("[dim]  - What vulnerabilities were found?[/dim]")
    console.print("[dim]  - Explain the most critical finding[/dim]")
    console.print("[dim]  - What remediation steps do you recommend?[/dim]")
    console.print("[dim]  - Were any credentials exposed?[/dim]\n")

    while True:
        try:
            # Get user input
            question = console.input("[bold cyan]You:[/bold cyan] ").strip()

            if not question:
                continue

            if question.lower() in ('exit', 'quit', 'q'):
                console.print("\nGoodbye!", style="cyan")
                break

            # Ask the question
            console.print()
            with console.status("[bold cyan]AI is thinking..."):
                result = client.chat_with_pentest(pentest_id, question, timeout=180)

            if result.get('success'):
                answer = result.get('answer', 'No answer provided')
                console.print("[bold green]AI:[/bold green]")
                console.print(Markdown(answer))
                console.print()
            else:
                error_msg = result.get('error', 'Unknown error')
                console.print(f"[red]Error: {error_msg}[/red]\n")

        except KeyboardInterrupt:
            console.print("\n\nGoodbye!", style="cyan")
            break
        except EOFError:
            console.print("\n\nGoodbye!", style="cyan")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]\n")

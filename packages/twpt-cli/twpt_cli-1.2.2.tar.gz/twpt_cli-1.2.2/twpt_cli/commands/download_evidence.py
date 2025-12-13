"""Download evidence command for ThreatWinds Pentest CLI."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

from twpt_cli.config import load_credentials, get_api_endpoint, DOWNLOAD_TIMEOUT
from twpt_cli.sdk import HTTPClient

console = Console()


@click.command()
@click.argument('pentest_id')
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    default='.',
    help='Output directory for evidence (default: current directory)'
)
@click.option(
    '--no-extract',
    is_flag=True,
    help='Keep the ZIP file without extracting'
)
@click.option(
    '--task',
    is_flag=True,
    help='Download evidence for a custom task instead of a pentest'
)
def download_evidence(pentest_id: str, output: str, no_extract: bool, task: bool):
    """Download evidence/reports for a completed pentest or custom task.

    PENTEST_ID: The unique identifier of the pentest or custom task (e.g., swift-falcon-strikes).

    The evidence will be downloaded as a ZIP file and extracted by default.
    Use --no-extract to keep the ZIP file without extracting.
    Use --task to download evidence for a custom task.

    Examples:
        twpt-cli download-evidence swift-falcon-strikes
        twpt-cli download-evidence dark-storm-rises --output /tmp/evidence
        twpt-cli download-evidence cyber-hawk-hunts --no-extract
        twpt-cli download-evidence bold-titan-guards --task  # Download custom task evidence
    """
    # Load credentials
    creds = load_credentials()
    if not creds:
        console.print("✗ Not configured. Please run: twpt-cli configure", style="red")
        sys.exit(1)

    # Validate output directory
    output_path = Path(output).resolve()
    if not output_path.exists():
        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            console.print(f"✗ Failed to create output directory: {e}", style="red")
            sys.exit(1)

    # Download evidence
    item_type = "custom task" if task else "pentest"
    console.print(f"\n⚙ Downloading evidence for {item_type} {pentest_id}...\n", style="cyan")

    try:
        client = HTTPClient(get_api_endpoint(), creds)

        with Progress(
            "[progress.description]{task.description}",
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Downloading evidence...", total=None)

            # Download with extraction option
            result_path = client.download_evidence(
                pentest_id=pentest_id,
                output_path=str(output_path),
                extract=not no_extract,
                timeout=DOWNLOAD_TIMEOUT
            )

            progress.update(task, completed=True)

        # Display success message
        console.print("\n✓ Evidence downloaded successfully!", style="green bold")

        if no_extract:
            console.print(f"ZIP file saved to: {result_path}", style="cyan")
        else:
            console.print(f"Evidence extracted to: {result_path}", style="cyan")

        # Show contents if extracted
        if not no_extract:
            show_extracted_contents(Path(result_path))

    except Exception as e:
        console.print(f"\n✗ Failed to download evidence: {e}", style="red")
        console.print("\nPossible reasons:", style="yellow")
        console.print("  • Pentest is not completed yet", style="dim")
        console.print("  • Pentest ID is invalid", style="dim")
        console.print("  • Network or container issues", style="dim")
        sys.exit(1)


def download_pentest_evidence(pentest_id: str, creds, output: str = '.'):
    """Programmatic download function for auto-download feature.

    Args:
        pentest_id: Pentest ID
        creds: API credentials
        output: Output directory
    """
    output_path = Path(output).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    client = HTTPClient(get_api_endpoint(), creds)
    result_path = client.download_evidence(
        pentest_id=pentest_id,
        output_path=str(output_path),
        extract=True,
        timeout=DOWNLOAD_TIMEOUT
    )

    console.print(f"✓ Evidence saved to: {result_path}", style="green")
    return result_path


def show_extracted_contents(evidence_dir: Path):
    """Display the contents of extracted evidence.

    Args:
        evidence_dir: Path to extracted evidence directory
    """
    try:
        # List main directories and files
        contents = list(evidence_dir.iterdir())
        if contents:
            console.print("\nExtracted contents:", style="cyan")

            # Categorize contents
            reports = []
            screenshots = []
            logs = []
            other = []

            for item in contents:
                if item.is_file():
                    if item.suffix in ['.pdf', '.html', '.md', '.txt']:
                        reports.append(item)
                    elif item.suffix in ['.png', '.jpg', '.jpeg', '.gif']:
                        screenshots.append(item)
                    elif item.suffix in ['.log', '.json', '.xml']:
                        logs.append(item)
                    else:
                        other.append(item)
                else:
                    other.append(item)

            # Display categorized contents
            if reports:
                console.print("\n  Reports:", style="yellow")
                for report in reports:
                    console.print(f"    • {report.name}", style="white")

            if screenshots:
                console.print("\n  Screenshots:", style="yellow")
                console.print(f"    • {len(screenshots)} screenshot(s) found", style="white")

            if logs:
                console.print("\n  Logs:", style="yellow")
                for log in logs:
                    console.print(f"    • {log.name}", style="white")

            if other:
                console.print("\n  Other files:", style="yellow")
                for item in other:
                    if item.is_dir():
                        console.print(f"    📁 {item.name}/", style="white")
                    else:
                        console.print(f"    • {item.name}", style="white")

            # Provide opening instructions
            console.print("\nTo view the evidence:", style="dim")
            console.print(f"  cd {evidence_dir}", style="white")

            # Find main report
            for report in reports:
                if 'report' in report.name.lower() and report.suffix == '.html':
                    console.print(f"  open {report.name}  # Main report", style="white")
                    break

    except Exception as e:
        console.print(f"Unable to list extracted contents: {e}", style="yellow")
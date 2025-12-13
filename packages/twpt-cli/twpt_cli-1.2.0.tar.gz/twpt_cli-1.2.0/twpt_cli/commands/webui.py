"""Web UI command for ThreatWinds Pentest CLI."""

import click


@click.command('webui')
@click.option('--host', '-h', default='0.0.0.0', help='Host to bind to')
@click.option('--port', '-p', default=8080, type=int, help='Port to listen on')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
def webui(host: str, port: int, debug: bool):
    """Launch the web-based interface.

    This starts a local web server that provides two graphical interfaces:

    - Advanced UI (http://HOST:PORT/) - Terminal-style interface for technical users
    - Simplified UI (http://HOST:PORT/simple) - Modern, user-friendly interface

    Both interfaces share the same backend and allow you to manage pentests,
    view results, and monitor progress. You can switch between them at any time.

    Example:
        twpt webui
        twpt webui --port 9000
        twpt webui --host 127.0.0.1 --port 8888
    """
    try:
        from ..webui import run_server
    except ImportError as e:
        click.echo(click.style(f"Error: Missing dependencies for web UI: {e}", fg='red'))
        click.echo("Please install Flask: pip install flask flask-cors")
        raise SystemExit(1)

    click.echo(click.style("Starting ThreatWinds Pentest Web UI...", fg='green'))
    click.echo(f"Advanced UI: http://{host}:{port}/")
    click.echo(f"Simplified UI: http://{host}:{port}/simple")
    click.echo("Press Ctrl+C to stop")
    click.echo()

    try:
        run_server(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        click.echo("\nServer stopped.")
    except Exception as e:
        click.echo(click.style(f"Error starting server: {e}", fg='red'))
        raise SystemExit(1)

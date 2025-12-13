"""Flask web server for ThreatWinds Pentest CLI Web UI."""

import os
import json
import socket
import uuid
import asyncio
import threading
import queue
from pathlib import Path
from typing import Optional, Dict, Any, List, Generator

from flask import Flask, render_template, jsonify, request, send_file, send_from_directory, Response

from flask_cors import CORS

from ..sdk.http_client import HTTPClient
from ..sdk.grpc_client import GRPCClient
from ..sdk.models import (
    Credentials,
    HTTPSchedulePentestRequest,
    HTTPTargetRequest,
    HTTPScope,
    HTTPType,
    HTTPStyle,
    UpdateType,
)
from ..config.constants import (
    USER_CONFIG_PATH,
    CONFIG_FILE_NAME,
    ENDPOINT_FILE_NAME,
    DEFAULT_API_HOST,
    DEFAULT_GRPC_HOST,
    API_PORT,
    GRPC_PORT,
)
from ..config.credentials import (
    load_credentials,
    save_credentials,
    get_api_endpoint,
    get_grpc_endpoint,
    save_endpoint_config,
    load_endpoint_config,
    check_configured,
)


# Server profiles storage - use user config path (~/.twpt) instead of /opt/twpt
SERVERS_FILE = USER_CONFIG_PATH / 'servers.json'


def load_servers() -> List[Dict[str, Any]]:
    """Load server profiles from file."""
    try:
        if not SERVERS_FILE.exists():
            return []
        with open(SERVERS_FILE, 'r') as f:
            return json.load(f)
    except (PermissionError, OSError, json.JSONDecodeError):
        return []


def save_servers(servers: List[Dict[str, Any]]) -> None:
    """Save server profiles to file."""
    try:
        SERVERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SERVERS_FILE, 'w') as f:
            json.dump(servers, f, indent=2)
    except (PermissionError, OSError) as e:
        raise RuntimeError(f"Cannot save servers file: {e}")


def get_active_server() -> Optional[Dict[str, Any]]:
    """Get the currently active server."""
    servers = load_servers()
    for server in servers:
        if server.get('active'):
            return server
    return servers[0] if servers else None


def create_app() -> Flask:
    """Create and configure the Flask application."""
    # Get the directory where this file is located
    webui_dir = Path(__file__).parent
    webui_simple_dir = webui_dir.parent / 'webui_simple'

    app = Flask(
        __name__,
        template_folder=str(webui_dir / 'templates'),
        static_folder=str(webui_dir / 'static'),
    )

    # Enable CORS for API endpoints
    CORS(app)

    # Store client instance
    app.http_client = None
    # Use user config path (~/.twpt) for evidence storage instead of /opt/twpt
    app.evidence_base_path = USER_CONFIG_PATH / 'evidence'

    def get_client() -> Optional[HTTPClient]:
        """Get or create HTTP client instance."""
        if app.http_client is not None:
            return app.http_client

        try:
            credentials = load_credentials()
            if credentials is None:
                return None

            api_url = get_api_endpoint()
            app.http_client = HTTPClient(api_url, credentials)
            return app.http_client
        except Exception:
            return None

    def reset_client():
        """Reset the HTTP client to force reconnection."""
        app.http_client = None

    def get_local_ip() -> str:
        """Get the local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def get_country_from_ip(ip: str) -> Optional[str]:
        """Get country name from IP address using ip-api.com."""
        import requests
        try:
            # Skip for localhost/private IPs
            if ip in ('127.0.0.1', 'localhost') or ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                return None

            response = requests.get(f'http://ip-api.com/json/{ip}?fields=status,country', timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return data.get('country')
        except Exception:
            pass
        return None

    def get_geolocation_from_ip(ip: str) -> Optional[Dict[str, Any]]:
        """Get full geolocation data (lat, lon, country, city) from IP address using local GeoLite2 database."""
        try:
            # Return default location for localhost/private IPs (approximate center of US as fallback)
            if ip in ('127.0.0.1', 'localhost') or ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                return {
                    'ip': ip,
                    'lat': 39.8,
                    'lon': -98.5,
                    'country': 'Local Network',
                    'city': 'Private',
                    'isp': 'Local'
                }

            # Use local GeoLite2 database for IP geolocation
            from geolite2 import geolite2
            reader = geolite2.reader()
            match = reader.get(ip)

            if match:
                location = match.get('location', {})
                country_data = match.get('country', {})
                city_data = match.get('city', {})

                lat = location.get('latitude')
                lon = location.get('longitude')
                country = country_data.get('names', {}).get('en', 'Unknown')
                city = city_data.get('names', {}).get('en', 'Unknown')

                if lat is not None and lon is not None:
                    return {
                        'ip': ip,
                        'lat': lat,
                        'lon': lon,
                        'country': country,
                        'city': city,
                        'isp': 'Unknown'
                    }
        except ImportError:
            # Fall back to ip-api.com if geolite2 is not installed
            import requests
            try:
                response = requests.get(
                    f'http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon,isp,query',
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        return {
                            'ip': data.get('query', ip),
                            'lat': data.get('lat'),
                            'lon': data.get('lon'),
                            'country': data.get('country'),
                            'city': data.get('city'),
                            'isp': data.get('isp')
                        }
            except Exception:
                pass
        except Exception:
            pass
        return None

    def resolve_hostname_to_ip(hostname: str) -> Optional[str]:
        """Resolve a hostname/domain to its public IP address (fast, no ping)."""
        try:
            # Use socket resolution only (fast, no ping fallback)
            ip = socket.gethostbyname(hostname)
            # Check if it's not a private IP
            if not (ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.') or ip == '127.0.0.1'):
                return ip
        except socket.gaierror:
            pass
        except Exception:
            pass
        return None

    # Routes
    @app.route('/')
    def index():
        """Serve the main page (advanced UI)."""
        return render_template('index.html')

    @app.route('/simple')
    def simple_ui():
        """Serve the simplified UI."""
        return send_file(webui_simple_dir / 'templates' / 'index.html')

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """Serve static files for advanced UI."""
        return send_from_directory(app.static_folder, filename)

    @app.route('/simple/static/<path:subpath>/<path:filename>')
    def serve_simple_static(subpath, filename):
        """Serve static files for simplified UI."""
        static_path = webui_simple_dir / 'static' / subpath
        return send_from_directory(static_path, filename)

    # API Routes
    @app.route('/api/status')
    def api_status():
        """Get connection status."""
        has_credentials = check_configured()
        client = get_client()
        connected = client is not None

        try:
            api_url = get_api_endpoint()
            server = api_url.replace('http://', '').replace('https://', '')
        except Exception:
            server = f"{DEFAULT_API_HOST}:{API_PORT}"

        # Extract server host IP for geolocation
        server_host = server.split(':')[0] if ':' in server else server
        country = get_country_from_ip(server_host)

        return jsonify({
            'connected': connected,
            'server': server,
            'ip': get_local_ip(),
            'has_credentials': has_credentials,
            'country': country,
        })

    @app.route('/api/credentials', methods=['POST'])
    def api_save_credentials():
        """Save API credentials and initial server config."""
        try:
            data = request.get_json()
            api_key = data.get('api_key', '').strip()
            api_secret = data.get('api_secret', '').strip()
            host = data.get('host', 'localhost').strip()
            port = data.get('port', '9741').strip()

            if not api_key or not api_secret:
                return jsonify({'success': False, 'error': 'API key and secret required'}), 400

            # Save credentials
            save_credentials(api_key, api_secret)

            # Save endpoint config
            save_endpoint_config(host, port)

            # Create initial server profile
            servers = load_servers()
            if not servers:
                server_id = str(uuid.uuid4())
                servers.append({
                    'id': server_id,
                    'name': 'Default Server',
                    'host': host,
                    'port': port,
                    'grpc_port': '9742',
                    'active': True,
                })
                save_servers(servers)

            # Reset client to use new credentials
            reset_client()

            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/servers', methods=['GET'])
    def api_list_servers():
        """List all configured servers."""
        servers = load_servers()
        active_server = get_active_server()

        return jsonify({
            'servers': servers,
            'active_server': active_server,
        })

    @app.route('/api/servers', methods=['POST'])
    def api_add_server():
        """Add a new server."""
        try:
            data = request.get_json()
            name = data.get('name', '').strip()
            host = data.get('host', '').strip()
            port = data.get('port', '9741').strip()
            grpc_port = data.get('grpc_port', '9742').strip()
            use_existing = data.get('use_existing_credentials', True)

            if not name or not host:
                return jsonify({'success': False, 'error': 'Name and host required'}), 400

            servers = load_servers()
            server_id = str(uuid.uuid4())

            new_server = {
                'id': server_id,
                'name': name,
                'host': host,
                'port': port,
                'grpc_port': grpc_port,
                'active': False,
            }

            # If using different credentials, store them separately
            if not use_existing:
                api_key = data.get('api_key', '').strip()
                api_secret = data.get('api_secret', '').strip()
                if api_key and api_secret:
                    new_server['api_key'] = api_key
                    new_server['api_secret'] = api_secret

            servers.append(new_server)
            save_servers(servers)

            return jsonify({'success': True, 'server_id': server_id})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/servers/<server_id>', methods=['DELETE'])
    def api_remove_server(server_id: str):
        """Remove a server."""
        try:
            servers = load_servers()
            servers = [s for s in servers if s.get('id') != server_id]
            save_servers(servers)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/servers/switch', methods=['POST'])
    def api_switch_server():
        """Switch to a different server."""
        try:
            data = request.get_json()
            server_id = data.get('server_id')

            if not server_id:
                return jsonify({'success': False, 'error': 'Server ID required'}), 400

            servers = load_servers()
            target_server = None

            for server in servers:
                if server.get('id') == server_id:
                    server['active'] = True
                    target_server = server
                else:
                    server['active'] = False

            if not target_server:
                return jsonify({'success': False, 'error': 'Server not found'}), 404

            save_servers(servers)

            # Update endpoint config
            save_endpoint_config(
                target_server['host'],
                target_server['port'],
                target_server['host'],
                target_server.get('grpc_port', '9742')
            )

            # If server has custom credentials, use them
            if target_server.get('api_key') and target_server.get('api_secret'):
                save_credentials(target_server['api_key'], target_server['api_secret'])

            # Reset client to reconnect
            reset_client()

            return jsonify({
                'success': True,
                'server_name': target_server['name'],
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/version')
    def api_version():
        """Get version information."""
        client = get_client()
        version = "1.0.0"

        if client:
            try:
                version = client.get_current_version()
            except Exception:
                pass

        return jsonify({'version': version})

    @app.route('/api/pentests')
    def api_list_pentests():
        """List all pentests."""
        client = get_client()
        if not client:
            return jsonify({'error': 'Not connected', 'pentests': []}), 503

        try:
            page = request.args.get('page', 1, type=int)
            page_size = request.args.get('page_size', 50, type=int)

            result = client.list_pentests(page=page, page_size=page_size)

            # Convert to dict format
            pentests = []
            for p in result.pentests:
                pentest_dict = {
                    'id': p.id,
                    'status': p.status,
                    'style': p.style,
                    'exploit': p.exploit,
                    'created_at': p.created_at.isoformat() if p.created_at else None,
                    'started_at': p.started_at.isoformat() if p.started_at else None,
                    'finished_at': p.finished_at.isoformat() if p.finished_at else None,
                    'severity': p.severity,
                    'findings': p.findings,
                    'targets': []
                }

                for t in p.targets:
                    pentest_dict['targets'].append({
                        'target': t.target,
                        'scope': t.scope,
                        'type': t.type,
                        'status': t.status,
                        'phase': t.phase,
                        'severity': t.severity,
                        'findings': t.findings,
                    })

                pentests.append(pentest_dict)

            return jsonify({
                'pentests': pentests,
                'total': result.total,
                'page': result.page,
                'page_size': result.page_size,
                'total_pages': result.total_pages,
            })
        except Exception as e:
            return jsonify({'error': str(e), 'pentests': []}), 500

    @app.route('/api/pentests/<pentest_id>')
    def api_get_pentest(pentest_id: str):
        """Get a specific pentest."""
        client = get_client()
        if not client:
            return jsonify({'error': 'Not connected'}), 503

        try:
            p = client.get_pentest(pentest_id)

            pentest_dict = {
                'id': p.id,
                'status': p.status,
                'style': p.style,
                'exploit': p.exploit,
                'created_at': p.created_at.isoformat() if p.created_at else None,
                'started_at': p.started_at.isoformat() if p.started_at else None,
                'finished_at': p.finished_at.isoformat() if p.finished_at else None,
                'severity': p.severity,
                'findings': p.findings,
                'targets': []
            }

            for t in p.targets:
                pentest_dict['targets'].append({
                    'target': t.target,
                    'scope': t.scope,
                    'type': t.type,
                    'status': t.status,
                    'phase': t.phase,
                    'severity': t.severity,
                    'findings': t.findings,
                })

            return jsonify(pentest_dict)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/pentests/<pentest_id>/chat', methods=['POST'])
    def api_chat_with_pentest(pentest_id: str):
        """Chat about a pentest's results using AI analysis."""
        client = get_client()
        if not client:
            return jsonify({'success': False, 'error': 'Not connected', 'pentest_id': pentest_id}), 503

        try:
            data = request.get_json()
            question = data.get('question', '').strip()

            if not question:
                return jsonify({
                    'success': False,
                    'error': 'Question is required',
                    'pentest_id': pentest_id
                }), 400

            # Call the backend chat API
            result = client.chat_with_pentest(pentest_id, question)

            return jsonify(result)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'pentest_id': pentest_id
            }), 500

    @app.route('/api/pentests/schedule', methods=['POST'])
    def api_schedule_pentest():
        """Schedule a new pentest with optional playbook and memory support."""
        client = get_client()
        if not client:
            return jsonify({'error': 'Not connected'}), 503

        try:
            data = request.get_json()

            # Build targets
            targets = []
            for t in data.get('targets', []):
                scope = HTTPScope(t.get('scope', 'TARGETED'))
                ptype = HTTPType(t.get('type', 'BLACK_BOX'))

                target = HTTPTargetRequest(
                    target=t['target'],
                    scope=scope,
                    type=ptype,
                    credentials=t.get('credentials'),
                )
                targets.append(target)

            if not targets:
                return jsonify({'error': 'No targets provided'}), 400

            style = HTTPStyle(data.get('style', 'AGGRESSIVE'))
            exploit = data.get('exploit', True)

            req = HTTPSchedulePentestRequest(
                style=style,
                exploit=exploit,
                targets=targets,
            )

            # Handle playbook if provided
            playbook_name = data.get('playbook')
            if playbook_name:
                from ..config.playbooks import resolve_playbook_reference, get_playbook_metadata
                try:
                    plan_content = resolve_playbook_reference(playbook_name)
                    plan_meta = get_playbook_metadata(playbook_name)
                    req.custom_plan_content = plan_content
                    req.is_custom_plan = True
                    req.plan_metadata = plan_meta
                except (FileNotFoundError, ValueError) as e:
                    return jsonify({'error': f'Playbook error: {e}'}), 400

            # Handle memory items if provided
            memory_names = data.get('memory', [])
            inline_memory = data.get('inline_memory', [])
            include_default = data.get('include_default_memory', True) and not playbook_name

            if memory_names or inline_memory or include_default:
                from ..config.memory import get_memory_for_pentest
                memory_items = get_memory_for_pentest(
                    memory_names=memory_names if memory_names else None,
                    inline_memory=inline_memory if inline_memory else None,
                    include_default=include_default,
                )
                if memory_items:
                    req.memory_items = memory_items

            pentest_id = client.schedule_pentest(req)

            return jsonify({
                'pentest_id': pentest_id,
                'message': 'Pentest scheduled successfully',
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/pentests/<pentest_id>/download')
    def api_download_evidence(pentest_id: str):
        """Download evidence for a pentest."""
        client = get_client()
        if not client:
            return jsonify({'error': 'Not connected'}), 503

        try:
            # Create evidence directory
            evidence_dir = app.evidence_base_path / pentest_id
            evidence_dir.mkdir(parents=True, exist_ok=True)

            # Download evidence
            result_path = client.download_evidence(
                pentest_id=pentest_id,
                output_path=str(evidence_dir),
                extract=False,
            )

            return send_file(
                result_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f'pentest_{pentest_id}_evidence.zip'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/pentests/stream', methods=['POST'])
    def api_stream_pentest():
        """Schedule a pentest and stream real-time updates via SSE.

        This endpoint uses Server-Sent Events to stream gRPC updates
        to the client in real-time.
        """
        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured'}), 503

            data = request.get_json()

            # Build targets
            targets = []
            for t in data.get('targets', []):
                targets.append({
                    'target': t['target'],
                    'scope': t.get('scope', 'TARGETED'),
                    'type': t.get('type', 'BLACK_BOX'),
                    'credentials': t.get('credentials'),
                })

            if not targets:
                return jsonify({'error': 'No targets provided'}), 400

            request_dict = {
                'style': data.get('style', 'AGGRESSIVE'),
                'exploit': data.get('exploit', True),
                'targets': targets,
            }

            def generate_events() -> Generator[str, None, None]:
                """Generate SSE events from gRPC stream."""
                event_queue = queue.Queue()
                stop_event = threading.Event()

                def run_stream():
                    """Run the async gRPC stream in a separate thread."""
                    async def stream_handler():
                        grpc_client = None
                        try:
                            grpc_address = get_grpc_endpoint()
                            grpc_client = GRPCClient(grpc_address, credentials)
                            # Explicitly connect before streaming
                            await grpc_client.connect()

                            async for response in grpc_client.schedule_pentest_stream(request_dict):
                                if stop_event.is_set():
                                    break
                                event_queue.put(('data', response))

                            event_queue.put(('done', None))
                        except Exception as e:
                            event_queue.put(('error', str(e)))
                        finally:
                            if grpc_client:
                                try:
                                    await grpc_client.close()
                                except Exception:
                                    pass

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    # Suppress BlockingIOError from gRPC's PollerCompletionQueue
                    # This is a known issue when mixing Flask threads with gRPC async
                    def handle_exception(loop, context):
                        exc = context.get('exception')
                        if isinstance(exc, BlockingIOError):
                            return  # Silently ignore
                        loop.default_exception_handler(context)
                    loop.set_exception_handler(handle_exception)
                    try:
                        # Initialize gRPC async for this thread's event loop
                        from grpc import aio as grpc_aio
                        grpc_aio.init_grpc_aio()
                        loop.run_until_complete(stream_handler())
                    finally:
                        loop.close()

                # Start streaming in background thread
                stream_thread = threading.Thread(target=run_stream, daemon=True)
                stream_thread.start()

                try:
                    while True:
                        try:
                            event_type, data = event_queue.get(timeout=60)

                            if event_type == 'done':
                                yield f"event: done\ndata: {json.dumps({'message': 'Stream completed'})}\n\n"
                                break
                            elif event_type == 'error':
                                yield f"event: error\ndata: {json.dumps({'error': data})}\n\n"
                                break
                            elif event_type == 'data':
                                yield f"event: message\ndata: {json.dumps(data)}\n\n"

                        except queue.Empty:
                            # Send keepalive
                            yield f"event: keepalive\ndata: {json.dumps({'timestamp': 'ping'})}\n\n"
                except GeneratorExit:
                    stop_event.set()

            return Response(
                generate_events(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no',
                }
            )

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/pentests/<pentest_id>/watch')
    def api_watch_pentest(pentest_id: str):
        """Watch a pentest's real-time updates via SSE using gRPC streaming.

        This endpoint uses gRPC streaming to receive real-time updates
        for an existing pentest, including detailed progress messages.
        """
        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured'}), 503

            def generate_events() -> Generator[str, None, None]:
                """Generate SSE events from gRPC stream."""
                event_queue = queue.Queue()
                stop_event = threading.Event()

                def run_stream():
                    """Run the async gRPC stream in a separate thread."""
                    async def stream_handler():
                        grpc_client = None
                        try:
                            grpc_address = get_grpc_endpoint()
                            grpc_client = GRPCClient(grpc_address, credentials)
                            # Explicitly connect before streaming
                            await grpc_client.connect()

                            async for response in grpc_client.watch_pentest_stream(pentest_id):
                                if stop_event.is_set():
                                    break
                                event_queue.put(('data', response))

                            event_queue.put(('done', None))
                        except Exception as e:
                            event_queue.put(('error', str(e)))
                        finally:
                            if grpc_client:
                                try:
                                    await grpc_client.close()
                                except Exception:
                                    pass

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    # Suppress BlockingIOError from gRPC's PollerCompletionQueue
                    def handle_exception(loop, context):
                        exc = context.get('exception')
                        if isinstance(exc, BlockingIOError):
                            return  # Silently ignore
                        loop.default_exception_handler(context)
                    loop.set_exception_handler(handle_exception)
                    try:
                        # Initialize gRPC async for this thread's event loop
                        from grpc import aio as grpc_aio
                        grpc_aio.init_grpc_aio()
                        loop.run_until_complete(stream_handler())
                    finally:
                        loop.close()

                # Start streaming in background thread
                stream_thread = threading.Thread(target=run_stream, daemon=True)
                stream_thread.start()

                try:
                    while True:
                        try:
                            event_type, data = event_queue.get(timeout=60)

                            if event_type == 'done':
                                yield f"event: done\ndata: {json.dumps({'message': 'Stream completed'})}\n\n"
                                break
                            elif event_type == 'error':
                                yield f"event: error\ndata: {json.dumps({'error': data})}\n\n"
                                break
                            elif event_type == 'data':
                                # Determine event type based on response
                                response_type = data.get('type', 'message')
                                if response_type == 'status_update':
                                    yield f"event: status\ndata: {json.dumps(data)}\n\n"
                                elif response_type == 'pentest_data':
                                    yield f"event: message\ndata: {json.dumps(data)}\n\n"
                                    # Check for completion
                                    status_val = data.get('status', '')
                                    if status_val in ['COMPLETED', 'FAILED']:
                                        done_msg = {'message': f'Pentest {status_val.lower()}'}
                                        yield f"event: done\ndata: {json.dumps(done_msg)}\n\n"
                                        stop_event.set()
                                        break
                                else:
                                    yield f"event: message\ndata: {json.dumps(data)}\n\n"

                        except queue.Empty:
                            # Send keepalive
                            yield f"event: keepalive\ndata: {json.dumps({'timestamp': 'ping'})}\n\n"
                except GeneratorExit:
                    stop_event.set()

            return Response(
                generate_events(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no',
                }
            )

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/pentests/<pentest_id>/attach')
    def api_attach_pentest(pentest_id: str):
        """Attach to a running pentest stream via SSE with late-join support.

        This endpoint uses the subscribe_pentest_stream gRPC method to:
        1. Connect to a running pentest
        2. Optionally replay historical events (use ?include_history=false to skip)
        3. Stream real-time updates as they happen

        This allows clients to reconnect to a pentest stream at any time,
        even after closing the browser and returning later.
        """
        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured'}), 503

            include_history = request.args.get('include_history', 'true').lower() == 'true'

            def generate_events() -> Generator[str, None, None]:
                """Generate SSE events from gRPC subscribe stream."""
                event_queue = queue.Queue()
                stop_event = threading.Event()

                def run_stream():
                    """Run the async gRPC stream in a separate thread."""
                    async def stream_handler():
                        grpc_client = None
                        try:
                            grpc_address = get_grpc_endpoint()
                            grpc_client = GRPCClient(grpc_address, credentials)
                            # Explicitly connect before streaming
                            await grpc_client.connect()

                            async for response in grpc_client.subscribe_pentest_stream(
                                pentest_id,
                                include_history=include_history
                            ):
                                if stop_event.is_set():
                                    break
                                event_queue.put(('data', response))

                            event_queue.put(('done', None))
                        except Exception as e:
                            event_queue.put(('error', str(e)))
                        finally:
                            if grpc_client:
                                try:
                                    await grpc_client.close()
                                except Exception:
                                    pass

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    # Suppress BlockingIOError from gRPC's PollerCompletionQueue
                    def handle_exception(loop, context):
                        exc = context.get('exception')
                        if isinstance(exc, BlockingIOError):
                            return  # Silently ignore
                        loop.default_exception_handler(context)
                    loop.set_exception_handler(handle_exception)
                    try:
                        # Initialize gRPC async for this thread's event loop
                        from grpc import aio as grpc_aio
                        grpc_aio.init_grpc_aio()
                        loop.run_until_complete(stream_handler())
                    finally:
                        loop.close()

                # Start streaming in background thread
                stream_thread = threading.Thread(target=run_stream, daemon=True)
                stream_thread.start()

                try:
                    while True:
                        try:
                            event_type, data = event_queue.get(timeout=60)

                            if event_type == 'done':
                                yield f"event: done\ndata: {json.dumps({'message': 'Stream completed'})}\n\n"
                                break
                            elif event_type == 'error':
                                yield f"event: error\ndata: {json.dumps({'error': data})}\n\n"
                                break
                            elif event_type == 'data':
                                # Determine event type based on response
                                response_type = data.get('type', 'message')

                                if response_type == 'subscribe_response':
                                    # Initial subscription confirmation
                                    yield f"event: subscribed\ndata: {json.dumps(data)}\n\n"
                                elif response_type == 'status_update':
                                    yield f"event: status\ndata: {json.dumps(data)}\n\n"
                                elif response_type == 'pentest_data':
                                    yield f"event: message\ndata: {json.dumps(data)}\n\n"
                                    # Check for completion
                                    status_val = data.get('status', '')
                                    if status_val in ['COMPLETED', 'FAILED']:
                                        done_msg = {'message': f'Pentest {status_val.lower()}'}
                                        yield f"event: done\ndata: {json.dumps(done_msg)}\n\n"
                                        stop_event.set()
                                        break
                                else:
                                    yield f"event: message\ndata: {json.dumps(data)}\n\n"

                        except queue.Empty:
                            # Send keepalive
                            yield f"event: keepalive\ndata: {json.dumps({'timestamp': 'ping'})}\n\n"
                except GeneratorExit:
                    stop_event.set()

            return Response(
                generate_events(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no',
                }
            )

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/pentests/<pentest_id>/files')
    def api_list_evidence_files(pentest_id: str):
        """List evidence files for a pentest."""
        evidence_dir = app.evidence_base_path / pentest_id

        try:
            if not evidence_dir.exists():
                return jsonify({'files': {}})
        except PermissionError:
            return jsonify({'files': {}, 'error': 'Permission denied accessing evidence directory'})

        def build_tree(path: Path) -> Dict[str, Any]:
            """Build a file tree structure."""
            result = {}
            try:
                for item in sorted(path.iterdir()):
                    if item.is_dir():
                        result[item.name] = {
                            'type': 'directory',
                            'children': build_tree(item)
                        }
                    else:
                        result[item.name] = {
                            'type': 'file',
                            'size': item.stat().st_size,
                        }
            except PermissionError:
                pass
            return result

        files = build_tree(evidence_dir)
        return jsonify({'files': files})

    @app.route('/api/pentests/<pentest_id>/download-and-extract', methods=['POST'])
    def api_download_and_extract(pentest_id: str):
        """Download and extract evidence for a pentest."""
        import shutil

        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured', 'success': False}), 503

            api_address = get_api_endpoint()
            http_client = HTTPClient(api_address, credentials)

            # Create evidence directory for this pentest
            evidence_dir = app.evidence_base_path / pentest_id
            evidence_dir.mkdir(parents=True, exist_ok=True)

            # download_evidence expects a directory path and handles extraction itself
            # It returns the path to the extracted folder
            extracted_path = http_client.download_evidence(
                pentest_id,
                str(evidence_dir),
                extract=True
            )

            # Move extracted contents to evidence_dir root if nested
            extracted_dir = Path(extracted_path)
            if extracted_dir != evidence_dir and extracted_dir.exists():
                # Move all files from extracted subfolder to evidence_dir
                for item in extracted_dir.iterdir():
                    dest = evidence_dir / item.name
                    if dest.exists():
                        if dest.is_dir():
                            shutil.rmtree(dest)
                        else:
                            dest.unlink()
                    shutil.move(str(item), str(evidence_dir))
                # Remove the now-empty extracted subfolder
                if extracted_dir.exists() and extracted_dir != evidence_dir:
                    try:
                        extracted_dir.rmdir()
                    except OSError:
                        pass  # Directory not empty, leave it

            return jsonify({
                'success': True,
                'message': 'Evidence downloaded and extracted',
                'path': str(evidence_dir)
            })

        except Exception as e:
            return jsonify({'error': str(e), 'success': False}), 500

    @app.route('/api/files/preview')
    def api_preview_file():
        """Preview a file's content."""
        file_path = request.args.get('path', '')
        if not file_path:
            return jsonify({'error': 'No path provided'}), 400

        # Security: ensure the path is within evidence directory
        try:
            full_path = (app.evidence_base_path / file_path).resolve()
            if not str(full_path).startswith(str(app.evidence_base_path.resolve())):
                return jsonify({'error': 'Invalid path'}), 400

            if not full_path.exists():
                return jsonify({'error': 'File not found'}), 404

            if not full_path.is_file():
                return jsonify({'error': 'Not a file'}), 400

            # Read file content (limit to 100KB)
            max_size = 100 * 1024
            file_size = full_path.stat().st_size

            if file_size > max_size:
                content = full_path.read_bytes()[:max_size].decode('utf-8', errors='replace')
                content += f"\n\n... [Truncated, file size: {file_size} bytes]"
            else:
                content = full_path.read_text(errors='replace')

            return jsonify({'content': content, 'size': file_size})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/geolocation/server')
    def api_server_geolocation():
        """Get geolocation of the connected server."""
        try:
            api_url = get_api_endpoint()
            server_host = api_url.replace('http://', '').replace('https://', '').split(':')[0]

            # Resolve server host if it's a hostname
            ip = server_host
            if not server_host.replace('.', '').isdigit():
                resolved = resolve_hostname_to_ip(server_host)
                if resolved:
                    ip = resolved

            geo = get_geolocation_from_ip(ip)
            if geo:
                return jsonify({
                    'success': True,
                    'host': server_host,
                    **geo
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Could not determine server location',
                    'host': server_host,
                    # Default to center of US
                    'lat': 39.8,
                    'lon': -98.5,
                })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'lat': 39.8,
                'lon': -98.5,
            })

    @app.route('/api/geolocation/resolve', methods=['POST'])
    def api_resolve_target():
        """Resolve a hostname/domain to IP and get its geolocation."""
        try:
            data = request.get_json()
            target = data.get('target', '').strip()

            if not target:
                return jsonify({'success': False, 'error': 'No target provided'}), 400

            # Check if target is already an IP
            ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
            import re
            if re.match(ip_pattern, target):
                ip = target
            else:
                # Resolve hostname to IP
                ip = resolve_hostname_to_ip(target)
                if not ip:
                    return jsonify({
                        'success': False,
                        'error': 'Could not resolve hostname',
                        'target': target,
                    })

            # Get geolocation for the IP
            geo = get_geolocation_from_ip(ip)
            if geo:
                return jsonify({
                    'success': True,
                    'target': target,
                    'resolved_ip': ip,
                    **geo
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Could not get geolocation',
                    'target': target,
                    'resolved_ip': ip,
                })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # ===========================================
    # Custom Task API Endpoints
    # ===========================================

    @app.route('/api/tasks', methods=['GET'])
    def api_list_custom_tasks():
        """List all custom task sessions."""
        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured', 'tasks': []}), 503

            async def get_tasks():
                grpc_address = get_grpc_endpoint()
                grpc_client = GRPCClient(grpc_address, credentials)
                await grpc_client.connect()

                try:
                    page = request.args.get('page', 1, type=int)
                    page_size = request.args.get('page_size', 20, type=int)
                    result = await grpc_client.list_custom_tasks(page=page, page_size=page_size)
                    return result
                finally:
                    await grpc_client.close()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(get_tasks())
                return jsonify(result)
            finally:
                loop.close()

        except Exception as e:
            return jsonify({'error': str(e), 'tasks': []}), 500

    @app.route('/api/tasks/<task_id>', methods=['GET'])
    def api_get_custom_task(task_id: str):
        """Get a specific custom task session."""
        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured'}), 503

            async def get_task():
                grpc_address = get_grpc_endpoint()
                grpc_client = GRPCClient(grpc_address, credentials)
                await grpc_client.connect()

                try:
                    result = await grpc_client.get_custom_task(task_id)
                    return result
                finally:
                    await grpc_client.close()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(get_task())
                return jsonify(result)
            finally:
                loop.close()

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/tasks/<task_id>', methods=['DELETE'])
    def api_close_custom_task(task_id: str):
        """Close a custom task session."""
        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured'}), 503

            async def close_task():
                grpc_address = get_grpc_endpoint()
                grpc_client = GRPCClient(grpc_address, credentials)
                await grpc_client.connect()

                try:
                    result = await grpc_client.close_custom_task(task_id)
                    return result
                finally:
                    await grpc_client.close()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(close_task())
                return jsonify(result)
            finally:
                loop.close()

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/tasks/submit', methods=['POST'])
    def api_submit_custom_task():
        """Submit a custom task and stream real-time updates via SSE."""
        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured'}), 503

            data = request.get_json()
            description = data.get('description', '').strip()
            target = data.get('target', '').strip()
            parameters = data.get('parameters', [])
            task_id = data.get('task_id')  # Optional: reuse session

            if not description or not target:
                return jsonify({'error': 'Description and target required'}), 400

            def generate_events() -> Generator[str, None, None]:
                """Generate SSE events from gRPC stream."""
                event_queue = queue.Queue()
                stop_event = threading.Event()

                def run_stream():
                    """Run the async gRPC stream in a separate thread."""
                    async def stream_handler():
                        grpc_client = None
                        try:
                            grpc_address = get_grpc_endpoint()
                            grpc_client = GRPCClient(grpc_address, credentials)
                            await grpc_client.connect()

                            async for response in grpc_client.submit_custom_task_stream(
                                description=description,
                                target=target,
                                parameters=parameters,
                                task_id=task_id
                            ):
                                if stop_event.is_set():
                                    break
                                event_queue.put(('data', response))

                            event_queue.put(('done', None))
                        except Exception as e:
                            event_queue.put(('error', str(e)))
                        finally:
                            if grpc_client:
                                try:
                                    await grpc_client.close()
                                except Exception:
                                    pass

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    def handle_exception(loop, context):
                        exc = context.get('exception')
                        if isinstance(exc, BlockingIOError):
                            return
                        loop.default_exception_handler(context)
                    loop.set_exception_handler(handle_exception)
                    try:
                        from grpc import aio as grpc_aio
                        grpc_aio.init_grpc_aio()
                        loop.run_until_complete(stream_handler())
                    finally:
                        loop.close()

                stream_thread = threading.Thread(target=run_stream, daemon=True)
                stream_thread.start()

                try:
                    while True:
                        try:
                            event_type, data = event_queue.get(timeout=120)

                            if event_type == 'done':
                                yield f"event: done\ndata: {json.dumps({'message': 'Task completed'})}\n\n"
                                break
                            elif event_type == 'error':
                                yield f"event: error\ndata: {json.dumps({'error': data})}\n\n"
                                break
                            elif event_type == 'data':
                                response_type = data.get('type', 'message')
                                if response_type == 'custom_task_response':
                                    yield f"event: task_started\ndata: {json.dumps(data)}\n\n"
                                elif response_type == 'status_update':
                                    yield f"event: update\ndata: {json.dumps(data)}\n\n"
                                elif response_type == 'custom_task_data':
                                    yield f"event: task_data\ndata: {json.dumps(data)}\n\n"
                                else:
                                    yield f"event: message\ndata: {json.dumps(data)}\n\n"

                        except queue.Empty:
                            yield f"event: keepalive\ndata: {json.dumps({'timestamp': 'ping'})}\n\n"
                except GeneratorExit:
                    stop_event.set()

            return Response(
                generate_events(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no',
                }
            )

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/tasks/<task_id>/attach')
    def api_attach_custom_task(task_id: str):
        """Attach to a running custom task stream via SSE."""
        try:
            credentials = load_credentials()
            if credentials is None:
                return jsonify({'error': 'Not configured'}), 503

            include_history = request.args.get('include_history', 'true').lower() == 'true'

            def generate_events() -> Generator[str, None, None]:
                """Generate SSE events from gRPC stream."""
                event_queue = queue.Queue()
                stop_event = threading.Event()

                def run_stream():
                    async def stream_handler():
                        grpc_client = None
                        try:
                            grpc_address = get_grpc_endpoint()
                            grpc_client = GRPCClient(grpc_address, credentials)
                            await grpc_client.connect()

                            async for response in grpc_client.subscribe_custom_task_stream(
                                task_id,
                                include_history=include_history
                            ):
                                if stop_event.is_set():
                                    break
                                event_queue.put(('data', response))

                            event_queue.put(('done', None))
                        except Exception as e:
                            event_queue.put(('error', str(e)))
                        finally:
                            if grpc_client:
                                try:
                                    await grpc_client.close()
                                except Exception:
                                    pass

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    def handle_exception(loop, context):
                        exc = context.get('exception')
                        if isinstance(exc, BlockingIOError):
                            return
                        loop.default_exception_handler(context)
                    loop.set_exception_handler(handle_exception)
                    try:
                        from grpc import aio as grpc_aio
                        grpc_aio.init_grpc_aio()
                        loop.run_until_complete(stream_handler())
                    finally:
                        loop.close()

                stream_thread = threading.Thread(target=run_stream, daemon=True)
                stream_thread.start()

                try:
                    while True:
                        try:
                            event_type, data = event_queue.get(timeout=120)

                            if event_type == 'done':
                                yield f"event: done\ndata: {json.dumps({'message': 'Stream completed'})}\n\n"
                                break
                            elif event_type == 'error':
                                yield f"event: error\ndata: {json.dumps({'error': data})}\n\n"
                                break
                            elif event_type == 'data':
                                response_type = data.get('type', 'message')
                                if response_type == 'subscribe_custom_task_response':
                                    yield f"event: subscribed\ndata: {json.dumps(data)}\n\n"
                                elif response_type == 'status_update':
                                    yield f"event: update\ndata: {json.dumps(data)}\n\n"
                                elif response_type == 'custom_task_data':
                                    yield f"event: task_data\ndata: {json.dumps(data)}\n\n"
                                else:
                                    yield f"event: message\ndata: {json.dumps(data)}\n\n"

                        except queue.Empty:
                            yield f"event: keepalive\ndata: {json.dumps({'timestamp': 'ping'})}\n\n"
                except GeneratorExit:
                    stop_event.set()

            return Response(
                generate_events(),
                mimetype='text/event-stream',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no',
                }
            )

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/tasks/<task_id>/download')
    def api_download_task_evidence(task_id: str):
        """Download evidence for a custom task."""
        client = get_client()
        if not client:
            return jsonify({'error': 'Not connected'}), 503

        try:
            # Create evidence directory
            evidence_dir = app.evidence_base_path / f"custom_task_{task_id}"
            evidence_dir.mkdir(parents=True, exist_ok=True)

            # Download evidence
            result_path = client.download_evidence(
                pentest_id=task_id,
                output_path=str(evidence_dir),
                extract=False,
            )

            return send_file(
                result_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f'task_{task_id}_evidence.zip'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ===========================================
    # Geolocation API Endpoints
    # ===========================================

    @app.route('/api/geolocation/batch', methods=['POST'])
    def api_batch_resolve():
        """Batch resolve multiple targets to get their geolocations (concurrent)."""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import re

        def resolve_single_target(target: str) -> Dict[str, Any]:
            """Resolve a single target to geolocation."""
            target = target.strip()
            result = {'target': target, 'success': False}

            if not target:
                return result

            ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

            try:
                # Check if target is already an IP
                if re.match(ip_pattern, target):
                    ip = target
                else:
                    ip = resolve_hostname_to_ip(target)

                if ip:
                    result['resolved_ip'] = ip
                    geo = get_geolocation_from_ip(ip)
                    if geo:
                        result.update(geo)
                        result['success'] = True
            except Exception:
                pass

            return result

        try:
            data = request.get_json()
            targets = data.get('targets', [])

            if not targets:
                return jsonify({'success': True, 'results': []})

            # Limit to 50 targets
            targets = targets[:50]

            # Use ThreadPoolExecutor for concurrent resolution
            results = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                # Submit all tasks
                future_to_target = {executor.submit(resolve_single_target, t): t for t in targets}

                # Collect results as they complete
                for future in as_completed(future_to_target):
                    result = future.result()
                    results.append(result)

            # Sort results to maintain original order
            target_order = {t: i for i, t in enumerate(targets)}
            results.sort(key=lambda r: target_order.get(r.get('target', ''), 999))

            return jsonify({'success': True, 'results': results})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # ===========================================
    # Playbook Management API Endpoints
    # ===========================================

    @app.route('/api/playbooks', methods=['GET'])
    def api_list_playbooks():
        """List all saved playbooks."""
        try:
            from ..config.playbooks import list_playbooks, get_playbooks_dir
            items = list_playbooks()
            return jsonify({
                'success': True,
                'playbooks': items,
                'path': str(get_playbooks_dir())
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e), 'playbooks': []}), 500

    @app.route('/api/playbooks/<name>', methods=['GET'])
    def api_get_playbook(name: str):
        """Get a specific playbook's content."""
        try:
            from ..config.playbooks import get_playbook
            playbook = get_playbook(name)
            if not playbook:
                return jsonify({'success': False, 'error': 'Playbook not found'}), 404
            return jsonify({'success': True, 'playbook': playbook})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/playbooks/<name>', methods=['PUT'])
    def api_save_playbook(name: str):
        """Save or update a playbook."""
        try:
            from ..config.playbooks import save_playbook
            data = request.get_json()
            content = data.get('content', '')
            if not content:
                return jsonify({'success': False, 'error': 'Content is required'}), 400
            result = save_playbook(name=name, content=content)
            return jsonify({'success': True, **result})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/playbooks/<name>', methods=['DELETE'])
    def api_delete_playbook(name: str):
        """Delete a playbook."""
        try:
            from ..config.playbooks import delete_playbook
            if delete_playbook(name):
                return jsonify({'success': True, 'message': f'Playbook {name} deleted'})
            return jsonify({'success': False, 'error': 'Failed to delete playbook'}), 500
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # ===========================================
    # Memory Management API Endpoints
    # ===========================================

    @app.route('/api/memory', methods=['GET'])
    def api_list_memory():
        """List all saved memory items."""
        try:
            from ..config.memory import list_memory, get_memory_dir
            items = list_memory()
            return jsonify({
                'success': True,
                'items': items,
                'path': str(get_memory_dir())
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e), 'items': []}), 500

    @app.route('/api/memory/<name>', methods=['GET'])
    def api_get_memory(name: str):
        """Get a specific memory item's content."""
        try:
            from ..config.memory import get_memory
            item = get_memory(name)
            if not item:
                return jsonify({'success': False, 'error': 'Memory item not found'}), 404
            return jsonify({'success': True, 'item': item})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/memory/<name>', methods=['PUT'])
    def api_save_memory(name: str):
        """Save or update a memory item."""
        try:
            from ..config.memory import save_memory
            data = request.get_json()
            content = data.get('content', '')
            if not content:
                return jsonify({'success': False, 'error': 'Content is required'}), 400
            result = save_memory(name=name, content=content)
            return jsonify({'success': True, **result})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/memory/<name>', methods=['DELETE'])
    def api_delete_memory(name: str):
        """Delete a memory item."""
        try:
            from ..config.memory import delete_memory
            if delete_memory(name):
                return jsonify({'success': True, 'message': f'Memory item {name} deleted'})
            return jsonify({'success': False, 'error': 'Failed to delete memory item'}), 500
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    return app


def run_server(host: str = '0.0.0.0', port: int = 8080, debug: bool = False):
    """Run the web server.

    Args:
        host: Host to bind to
        port: Port to listen on
        debug: Enable debug mode
    """
    app = create_app()
    print(f"Starting ThreatWinds Pentest Web UI on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    run_server(debug=True)

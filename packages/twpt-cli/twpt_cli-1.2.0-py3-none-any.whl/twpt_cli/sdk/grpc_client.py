"""gRPC client for ThreatWinds Pentest API."""

import asyncio
import threading
from typing import Optional, AsyncIterator, Dict, Any
from contextlib import asynccontextmanager

import grpc
from grpc import aio

from .models import Credentials


class GRPCClient:
    """gRPC client for ThreatWinds Pentest API streaming operations."""

    def __init__(self, address: str, credentials: Credentials):
        """Initialize gRPC client.

        Args:
            address: gRPC server address (e.g., "localhost:9742")
            credentials: API credentials for authentication
        """
        self.address = address
        self.credentials = credentials
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub = None
        self._lock = threading.Lock()

    def _get_metadata(self) -> list:
        """Get authentication metadata for gRPC calls."""
        return [
            ('api-key', self.credentials.api_key),
            ('api-secret', self.credentials.api_secret),
        ]

    async def connect(self):
        """Establish connection to gRPC server."""
        if not self.channel:
            # Create an insecure channel (matching Go implementation)
            self.channel = grpc.aio.insecure_channel(self.address)

            # Dynamically import generated protobuf code
            # This will be generated from the .proto file
            try:
                from . import pentest_pb2_grpc
                self.stub = pentest_pb2_grpc.PentestServiceStub(self.channel)
            except ImportError:
                # If protobuf files aren't generated yet, provide instructions
                raise ImportError(
                    "gRPC protobuf files not generated. Run:\n"
                    "python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "
                    "twpt_cli/sdk/pentest.proto"
                )

    async def close(self):
        """Close the gRPC connection."""
        if self.channel:
            await self.channel.close()
            self.channel = None
            self.stub = None

    @asynccontextmanager
    async def pentest_stream(self):
        """Create a bidirectional streaming connection.

        Yields:
            A tuple of (request_queue, response_iterator) for bidirectional streaming

        Example:
            async with client.pentest_stream() as (request_queue, response_stream):
                # Send requests
                await request_queue.put(schedule_request)

                # Receive responses
                async for response in response_stream:
                    handle_response(response)
        """
        if not self.stub:
            await self.connect()

        # Create a queue for outgoing requests
        request_queue = asyncio.Queue()

        async def request_iterator():
            """Generate requests from the queue."""
            while True:
                request = await request_queue.get()
                if request is None:  # Sentinel to close stream
                    break
                yield request

        # Start the bidirectional stream
        response_stream = self.stub.PentestStream(
            request_iterator(),
            metadata=self._get_metadata()
        )

        try:
            yield (request_queue, response_stream)
        finally:
            # Send sentinel to close the request stream
            await request_queue.put(None)

    async def schedule_pentest_stream(self, request_dict: Dict[str, Any]) -> AsyncIterator:
        """Schedule a pentest and stream real-time updates.

        Args:
            request_dict: Dictionary with pentest configuration

        Yields:
            Response messages from the server

        Example:
            request = {
                'style': 'AGGRESSIVE',
                'exploit': True,
                'targets': [
                    {'target': 'example.com', 'scope': 'TARGETED', 'type': 'BLACK_BOX'}
                ]
            }

            async for response in client.schedule_pentest_stream(request):
                print(response)
        """
        try:
            from . import pentest_pb2

            # Convert dict to protobuf message
            targets = []
            for target_dict in request_dict.get('targets', []):
                target = pentest_pb2.TargetRequest(
                    target=target_dict['target'],
                    scope=getattr(pentest_pb2.Scope, target_dict.get('scope', 'TARGETED')),
                    type=getattr(pentest_pb2.Type, target_dict.get('type', 'BLACK_BOX'))
                )
                if 'credentials' in target_dict:
                    target.credentials = str(target_dict['credentials'])
                targets.append(target)

            schedule_request = pentest_pb2.SchedulePentestRequest(
                style=getattr(pentest_pb2.Style, request_dict.get('style', 'AGGRESSIVE')),
                exploit=request_dict.get('exploit', True),
                targets=targets
            )

            # Wrap in ClientRequest
            client_request = pentest_pb2.ClientRequest(
                schedule_pentest=schedule_request
            )

            async with self.pentest_stream() as (request_queue, response_stream):
                # Send the schedule request
                await request_queue.put(client_request)

                # Yield responses as they come
                async for response in response_stream:
                    yield self._parse_response(response)

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated. Run:\n"
                "python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "
                "twpt_cli/sdk/pentest.proto"
            )

    async def watch_pentest_stream(self, pentest_id: str) -> AsyncIterator:
        """Watch an existing pentest and stream real-time updates.

        Args:
            pentest_id: ID of the pentest to watch

        Yields:
            Response messages from the server

        Example:
            async for response in client.watch_pentest_stream("swift-falcon-strikes"):
                print(response)
        """
        try:
            from . import pentest_pb2

            # Create GetPentestRequest
            get_request = pentest_pb2.GetPentestRequest(
                pentest_id=pentest_id
            )

            # Wrap in ClientRequest
            client_request = pentest_pb2.ClientRequest(
                get_pentest=get_request
            )

            async with self.pentest_stream() as (request_queue, response_stream):
                # Send the get request to subscribe to updates
                await request_queue.put(client_request)

                # Yield responses as they come
                async for response in response_stream:
                    yield self._parse_response(response)

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated. Run:\n"
                "python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "
                "twpt_cli/sdk/pentest.proto"
            )

    async def subscribe_pentest_stream(self, pentest_id: str, include_history: bool = True) -> AsyncIterator:
        """Subscribe to an existing/running pentest and stream real-time updates.

        This is the late-join streaming method that allows connecting to a pentest
        that is already running. It provides:
        - Current state snapshot immediately upon connection
        - Historical events replay (if include_history=True)
        - Live updates as the pentest progresses

        Args:
            pentest_id: ID of the pentest to subscribe to
            include_history: If True, replay historical events from memory

        Yields:
            Response messages from the server

        Example:
            async for response in client.subscribe_pentest_stream("swift-falcon-strikes", include_history=True):
                if response['type'] == 'subscribe_response':
                    print(f"Subscribed! Running: {response['is_running']}")
                elif response['type'] == 'status_update':
                    print(f"Update: {response['message']}")
        """
        try:
            from . import pentest_pb2

            # Create SubscribePentestRequest
            subscribe_request = pentest_pb2.SubscribePentestRequest(
                pentest_id=pentest_id,
                include_history=include_history
            )

            # Wrap in ClientRequest
            client_request = pentest_pb2.ClientRequest(
                subscribe_pentest=subscribe_request
            )

            async with self.pentest_stream() as (request_queue, response_stream):
                # Send the subscribe request
                await request_queue.put(client_request)

                # Yield responses as they come
                async for response in response_stream:
                    yield self._parse_response(response)

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated. Run:\n"
                "python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "
                "twpt_cli/sdk/pentest.proto"
            )

    async def subscribe_pentest_stream_interactive(
        self,
        pentest_id: str,
        include_history: bool = True
    ) -> tuple:
        """Subscribe to an existing/running pentest with bidirectional streaming.

        This method enables user context injection during watch mode by returning
        both the response iterator AND the request queue for sending additional
        messages (like InjectContextRequest).

        Args:
            pentest_id: ID of the pentest to subscribe to
            include_history: If True, replay historical events from memory

        Returns:
            Tuple of (request_queue, response_iterator, cleanup_func)
            - request_queue: asyncio.Queue to send additional requests
            - response_iterator: AsyncIterator for responses
            - cleanup_func: Coroutine to call for cleanup

        Example:
            request_queue, responses, cleanup = await client.subscribe_pentest_stream_interactive("swift-falcon-strikes")
            try:
                async for response in responses:
                    print(response)
                    # User can inject context by putting to request_queue
                    await request_queue.put(inject_request)
            finally:
                await cleanup()
        """
        try:
            from . import pentest_pb2

            if not self.stub:
                await self.connect()

            # Create a queue for outgoing requests
            request_queue = asyncio.Queue()

            async def request_iterator():
                """Generate requests from the queue."""
                # First, send the subscribe request
                subscribe_request = pentest_pb2.SubscribePentestRequest(
                    pentest_id=pentest_id,
                    include_history=include_history
                )
                client_request = pentest_pb2.ClientRequest(
                    subscribe_pentest=subscribe_request
                )
                yield client_request

                # Then yield any additional requests from the queue
                while True:
                    request = await request_queue.get()
                    if request is None:  # Sentinel to close stream
                        break
                    yield request

            # Start the bidirectional stream
            response_stream = self.stub.PentestStream(
                request_iterator(),
                metadata=self._get_metadata()
            )

            async def response_generator():
                async for response in response_stream:
                    yield self._parse_response(response)

            async def cleanup():
                await request_queue.put(None)

            return request_queue, response_generator(), cleanup

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated. Run:\n"
                "python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "
                "twpt_cli/sdk/pentest.proto"
            )

    def create_inject_context_request(
        self,
        pentest_id: str,
        context: str,
        priority: str = "NORMAL",
        target_id: str = None
    ):
        """Create an InjectContextRequest protobuf message.

        Args:
            pentest_id: ID of the pentest
            context: Context/hint text to inject
            priority: Priority level ("NORMAL", "HIGH", "IMMEDIATE")
            target_id: Optional target-specific context

        Returns:
            ClientRequest with InjectContextRequest
        """
        from . import pentest_pb2

        priority_map = {
            "NORMAL": pentest_pb2.CONTEXT_PRIORITY_NORMAL,
            "HIGH": pentest_pb2.CONTEXT_PRIORITY_HIGH,
            "IMMEDIATE": pentest_pb2.CONTEXT_PRIORITY_IMMEDIATE,
        }

        inject_request = pentest_pb2.InjectContextRequest(
            pentest_id=pentest_id,
            context=context,
            priority=priority_map.get(priority.upper(), pentest_pb2.CONTEXT_PRIORITY_NORMAL)
        )

        if target_id:
            inject_request.target_id = target_id

        return pentest_pb2.ClientRequest(inject_context=inject_request)

    def _parse_response(self, response) -> Dict[str, Any]:
        """Parse a ServerResponse protobuf message into a dictionary.

        Args:
            response: ServerResponse protobuf message

        Returns:
            Dictionary with parsed response data
        """
        from . import pentest_pb2

        response_type = response.WhichOneof('response_type')

        if response_type == 'schedule_response':
            return {
                'type': 'schedule_response',
                'pentest_id': response.schedule_response.pentest_id,
                'message': response.schedule_response.message
            }

        elif response_type == 'pentest_data':
            data = response.pentest_data
            return self._parse_pentest_data(data)

        elif response_type == 'status_update':
            update = response.status_update
            return {
                'type': 'status_update',
                'update_type': update.type,
                'pentest_id': update.pentest_id,
                'message': update.message if update.HasField('message') else None,
                'data': self._parse_pentest_data(update.data)
                        if update.HasField('data') else None,
                'task_complete': update.task_complete if update.HasField('task_complete') else False
            }

        elif response_type == 'error':
            return {
                'type': 'error',
                'error': response.error.error,
                'details': response.error.details
            }

        elif response_type == 'subscribe_response':
            return {
                'type': 'subscribe_response',
                'pentest_id': response.subscribe_response.pentest_id,
                'message': response.subscribe_response.message,
                'is_running': response.subscribe_response.is_running
            }

        elif response_type == 'pong':
            return {
                'type': 'pong',
                'message': response.pong.message
            }

        # Custom task response types
        elif response_type == 'custom_task_response':
            return {
                'type': 'custom_task_response',
                'task_id': response.custom_task_response.task_id,
                'message': response.custom_task_response.message
            }

        elif response_type == 'close_custom_task_response':
            return {
                'type': 'close_custom_task_response',
                'task_id': response.close_custom_task_response.task_id,
                'message': response.close_custom_task_response.message
            }

        elif response_type == 'custom_task_data':
            return self._parse_custom_task_data(response.custom_task_data)

        elif response_type == 'custom_task_list':
            return {
                'type': 'custom_task_list',
                'tasks': [self._parse_custom_task_data(t) for t in response.custom_task_list.tasks],
                'total': response.custom_task_list.total,
                'page': response.custom_task_list.page,
                'page_size': response.custom_task_list.page_size
            }

        elif response_type == 'subscribe_custom_task_response':
            return {
                'type': 'subscribe_custom_task_response',
                'task_id': response.subscribe_custom_task_response.task_id,
                'is_running': response.subscribe_custom_task_response.is_running,
                'message': response.subscribe_custom_task_response.message
            }

        elif response_type == 'context_ack':
            ack = response.context_ack
            result = {
                'type': 'context_ack',
                'pentest_id': ack.pentest_id,
                'message': ack.message,
                'accepted': ack.accepted
            }
            if ack.HasField('context_id'):
                result['context_id'] = ack.context_id
            return result

        return {'type': 'unknown', 'data': str(response)}

    def _parse_pentest_data(self, data) -> Dict[str, Any]:
        """Parse a PentestData protobuf message into a dictionary.

        Args:
            data: PentestData protobuf message

        Returns:
            Dictionary with parsed pentest data
        """
        from . import pentest_pb2

        result = {
            'type': 'pentest_data',
            'id': data.id,
            'status': pentest_pb2.Status.Name(data.status),
            'style': pentest_pb2.Style.Name(data.style),
            'exploit': data.exploit,
            'created_at': data.created_at if data.HasField('created_at') else None,
            'started_at': data.started_at if data.HasField('started_at') else None,
            'finished_at': data.finished_at if data.HasField('finished_at') else None,
            'severity': pentest_pb2.Severity.Name(data.severity) if data.HasField('severity') else None,
            'findings': data.findings if data.HasField('findings') else 0,
            'targets': [self._parse_target(t) for t in data.targets]
        }
        # Include summary and description for guided pentests
        if data.HasField('summary'):
            result['summary'] = data.summary
        if data.HasField('description'):
            result['description'] = data.description
        return result

    def _parse_target(self, target) -> Dict[str, Any]:
        """Parse a TargetData protobuf message.

        Args:
            target: TargetData protobuf message

        Returns:
            Dictionary with parsed target data
        """
        from . import pentest_pb2

        return {
            'id': target.id,
            'pentest_id': target.pentest_id,
            'target': target.target,
            'scope': pentest_pb2.Scope.Name(target.scope),
            'type': pentest_pb2.Type.Name(target.type),
            'status': pentest_pb2.Status.Name(target.status),
            'phase': pentest_pb2.Phase.Name(target.phase) if target.HasField('phase') else None,
            'severity': pentest_pb2.Severity.Name(target.severity) if target.HasField('severity') else None,
            'findings': target.findings if target.HasField('findings') else 0,
        }

    def _parse_custom_task_data(self, data) -> Dict[str, Any]:
        """Parse a CustomTaskData protobuf message.

        Args:
            data: CustomTaskData protobuf message

        Returns:
            Dictionary with parsed custom task data
        """
        from . import pentest_pb2

        result = {
            'type': 'custom_task_data',
            'id': data.id,
            'status': pentest_pb2.Status.Name(data.status),
            'target': data.target,
            'description': data.description,
            'request_count': data.request_count,
        }

        if data.HasField('created_at'):
            result['created_at'] = data.created_at
        if data.HasField('started_at'):
            result['started_at'] = data.started_at
        if data.HasField('finished_at'):
            result['finished_at'] = data.finished_at
        if data.HasField('summary'):
            result['summary'] = data.summary
        if data.HasField('severity'):
            result['severity'] = pentest_pb2.Severity.Name(data.severity)
        if data.HasField('findings'):
            result['findings'] = data.findings

        return result

    # ===========================================
    # Custom Task Methods
    # ===========================================

    async def submit_custom_task_stream(
        self,
        description: str,
        target: str,
        parameters: list = None,
        task_id: str = None
    ) -> AsyncIterator:
        """Submit a custom task and stream real-time updates.

        Args:
            description: What to do (e.g., "port scan", "web vulnerability scan")
            target: Target to test (e.g., "192.168.1.1", "example.com")
            parameters: Additional parameters
            task_id: Optional existing task session ID to reuse

        Yields:
            Response messages from the server

        Example:
            async for response in client.submit_custom_task_stream(
                description="port scan",
                target="192.168.1.1",
                parameters=["-p-", "--script=vuln"]
            ):
                if response['type'] == 'status_update':
                    print(response['message'])
        """
        try:
            from . import pentest_pb2

            # Create CustomTaskTarget
            task_target = pentest_pb2.CustomTaskTarget(
                description=description,
                target=target,
                parameters=parameters or []
            )

            # Create SubmitCustomTaskRequest
            submit_request = pentest_pb2.SubmitCustomTaskRequest(
                task=task_target
            )
            if task_id:
                submit_request.task_id = task_id

            # Wrap in ClientRequest
            client_request = pentest_pb2.ClientRequest(
                submit_custom_task=submit_request
            )

            async with self.pentest_stream() as (request_queue, response_stream):
                await request_queue.put(client_request)

                async for response in response_stream:
                    parsed = self._parse_response(response)
                    yield parsed

                    # Exit stream when task is complete
                    if parsed.get('type') == 'status_update' and parsed.get('task_complete'):
                        break

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated. Run:\n"
                "python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "
                "twpt_cli/sdk/pentest.proto"
            )

    async def close_custom_task(self, task_id: str) -> Dict[str, Any]:
        """Close a custom task session.

        Args:
            task_id: The task session ID to close

        Returns:
            Response dictionary
        """
        try:
            from . import pentest_pb2

            close_request = pentest_pb2.CloseCustomTaskRequest(
                task_id=task_id
            )

            client_request = pentest_pb2.ClientRequest(
                close_custom_task=close_request
            )

            async with self.pentest_stream() as (request_queue, response_stream):
                await request_queue.put(client_request)

                async for response in response_stream:
                    return self._parse_response(response)

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated."
            )

    async def get_custom_task(self, task_id: str) -> Dict[str, Any]:
        """Get a custom task by ID.

        Args:
            task_id: The task session ID

        Returns:
            Response dictionary with task data
        """
        try:
            from . import pentest_pb2

            get_request = pentest_pb2.GetCustomTaskRequest(
                task_id=task_id
            )

            client_request = pentest_pb2.ClientRequest(
                get_custom_task=get_request
            )

            async with self.pentest_stream() as (request_queue, response_stream):
                await request_queue.put(client_request)

                async for response in response_stream:
                    return self._parse_response(response)

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated."
            )

    async def list_custom_tasks(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """List custom tasks with pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Response dictionary with task list
        """
        try:
            from . import pentest_pb2

            list_request = pentest_pb2.ListCustomTasksRequest(
                page=page,
                page_size=page_size
            )

            client_request = pentest_pb2.ClientRequest(
                list_custom_tasks=list_request
            )

            async with self.pentest_stream() as (request_queue, response_stream):
                await request_queue.put(client_request)

                async for response in response_stream:
                    return self._parse_response(response)

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated."
            )

    async def subscribe_custom_task_stream(
        self,
        task_id: str,
        include_history: bool = True
    ) -> AsyncIterator:
        """Subscribe to an existing custom task and stream updates.

        Args:
            task_id: The task session ID to subscribe to
            include_history: If True, replay historical events

        Yields:
            Response messages from the server
        """
        try:
            from . import pentest_pb2

            subscribe_request = pentest_pb2.SubscribeCustomTaskRequest(
                task_id=task_id,
                include_history=include_history
            )

            client_request = pentest_pb2.ClientRequest(
                subscribe_custom_task=subscribe_request
            )

            async with self.pentest_stream() as (request_queue, response_stream):
                await request_queue.put(client_request)

                async for response in response_stream:
                    yield self._parse_response(response)

        except ImportError:
            raise ImportError(
                "gRPC protobuf files not generated."
            )


# Synchronous wrapper for easier CLI usage
class SyncGRPCClient:
    """Synchronous wrapper for the async gRPC client."""

    def __init__(self, address: str, credentials: Credentials):
        """Initialize synchronous gRPC client wrapper.

        Args:
            address: gRPC server address
            credentials: API credentials
        """
        self.async_client = GRPCClient(address, credentials)
        self._loop = None
        self._thread = None

    def _ensure_loop(self):
        """Ensure event loop is running in a separate thread."""
        if self._loop is None:
            import threading

            self._loop = asyncio.new_event_loop()

            def run_loop():
                asyncio.set_event_loop(self._loop)
                self._loop.run_forever()

            self._thread = threading.Thread(target=run_loop, daemon=True)
            self._thread.start()

    def schedule_pentest_stream(self, request_dict: Dict[str, Any], callback):
        """Schedule a pentest and stream updates via callback.

        Args:
            request_dict: Pentest configuration
            callback: Function to call with each response

        Example:
            def handle_response(response):
                print(f"Got response: {response}")

            client.schedule_pentest_stream(request, handle_response)
        """
        self._ensure_loop()

        async def stream_handler():
            async for response in self.async_client.schedule_pentest_stream(request_dict):
                callback(response)

        future = asyncio.run_coroutine_threadsafe(stream_handler(), self._loop)
        return future

    def subscribe_pentest_stream(self, pentest_id: str, callback, include_history: bool = True):
        """Subscribe to an existing/running pentest and stream updates via callback.

        This is the late-join streaming method for synchronous usage.

        Args:
            pentest_id: ID of the pentest to subscribe to
            callback: Function to call with each response
            include_history: If True, replay historical events from memory

        Example:
            def handle_response(response):
                if response['type'] == 'subscribe_response':
                    print(f"Subscribed! Running: {response['is_running']}")
                elif response['type'] == 'status_update':
                    print(f"Update: {response['message']}")

            client.subscribe_pentest_stream("swift-falcon-strikes", handle_response)
        """
        self._ensure_loop()

        async def stream_handler():
            async for response in self.async_client.subscribe_pentest_stream(pentest_id, include_history):
                callback(response)

        future = asyncio.run_coroutine_threadsafe(stream_handler(), self._loop)
        return future

    def close(self):
        """Close the client and cleanup resources."""
        if self._loop:
            future = asyncio.run_coroutine_threadsafe(
                self.async_client.close(),
                self._loop
            )
            future.result()
            self._loop.call_soon_threadsafe(self._loop.stop)
            if self._thread:
                self._thread.join(timeout=5)
            self._loop = None
            self._thread = None

    # ===========================================
    # Custom Task Sync Wrappers
    # ===========================================

    def submit_custom_task_stream(
        self,
        description: str,
        target: str,
        callback,
        parameters: list = None,
        task_id: str = None
    ):
        """Submit a custom task and stream updates via callback.

        Args:
            description: What to do
            target: Target to test
            callback: Function to call with each response
            parameters: Additional parameters
            task_id: Optional existing session ID

        Example:
            def handle_response(response):
                print(response['message'])

            client.submit_custom_task_stream("port scan", "192.168.1.1", handle_response)
        """
        self._ensure_loop()

        async def stream_handler():
            async for response in self.async_client.submit_custom_task_stream(
                description, target, parameters, task_id
            ):
                callback(response)

        future = asyncio.run_coroutine_threadsafe(stream_handler(), self._loop)
        return future

    def subscribe_custom_task_stream(
        self,
        task_id: str,
        callback,
        include_history: bool = True
    ):
        """Subscribe to an existing custom task and stream updates via callback.

        Args:
            task_id: Task session ID to subscribe to
            callback: Function to call with each response
            include_history: If True, replay historical events
        """
        self._ensure_loop()

        async def stream_handler():
            async for response in self.async_client.subscribe_custom_task_stream(
                task_id, include_history
            ):
                callback(response)

        future = asyncio.run_coroutine_threadsafe(stream_handler(), self._loop)
        return future
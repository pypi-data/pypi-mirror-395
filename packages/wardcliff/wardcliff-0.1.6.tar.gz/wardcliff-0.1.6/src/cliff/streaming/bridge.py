"""
JSON-RPC 2.0 bridge for Python <-> Ink UI communication.

Routes StreamEvents to the Ink subprocess via stdio and handles
incoming user actions via JSON-RPC requests.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from typing import Any, Callable, Dict, IO, Optional

from .events import StreamEvent

logger = logging.getLogger(__name__)


class StdioBridge:
    """
    Bridges StreamHandler events to Ink UI via stdio JSON-RPC.

    This replaces RichDisplay as the event subscriber. Events from the
    simulation are serialized as JSON-RPC notifications and written to
    the Ink subprocess stdin. User actions from Ink are read from the
    subprocess stdout and dispatched to registered handlers.
    """

    def __init__(
        self,
        output_stream: Optional[IO[bytes]] = None,
        market_id: str = "default",
    ):
        """
        Initialize the stdio bridge.

        Args:
            output_stream: Stream to write events to (default: Ink subprocess stdin)
            market_id: Identifier for the current market context
        """
        self._output = output_stream
        self.market_id = market_id
        self._request_handlers: Dict[str, Callable[..., Any]] = {}
        self._request_id = 0
        self._running = False
        self._pending_responses: Dict[int, asyncio.Future] = {}

    def set_output(self, stream: IO[bytes]) -> None:
        """Set the output stream (Ink subprocess stdin)."""
        self._output = stream

    def handle_event(self, event: StreamEvent) -> None:
        """
        StreamHandler subscriber - converts events to JSON-RPC notifications.

        This is the key interface that replaces RichDisplay.handle_event().
        Called by StreamHandler.emit() for each event.
        """
        notification = {
            "jsonrpc": "2.0",
            "method": "event",
            "params": {
                "market_id": self.market_id,
                **event.to_dict(),
            },
        }
        self._write_message(notification)

    def _write_message(self, msg: dict) -> None:
        """Write a JSON-RPC message to the output stream."""
        if self._output is None:
            logger.warning("No output stream configured for bridge")
            return

        try:
            line = json.dumps(msg, default=str) + "\n"
            if hasattr(self._output, "write"):
                self._output.write(line.encode("utf-8"))
                self._output.flush()
        except Exception as e:
            logger.error("Failed to write message: %s", e)

    def register_handler(self, method: str, handler: Callable[..., Any]) -> None:
        """
        Register a handler for incoming JSON-RPC requests from Ink.

        Args:
            method: The JSON-RPC method name (e.g., "create_market", "inject_news")
            handler: Async or sync function to handle the request
        """
        self._request_handlers[method] = handler

    async def handle_request(self, request: dict) -> dict:
        """
        Process an incoming JSON-RPC request from Ink.

        Args:
            request: The parsed JSON-RPC request

        Returns:
            JSON-RPC response dict
        """
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method not in self._request_handlers:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}",
                },
            }

        try:
            handler = self._request_handlers[method]
            if asyncio.iscoroutinefunction(handler):
                result = await handler(**params)
            else:
                result = handler(**params)

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result,
            }
        except Exception as e:
            logger.error("Handler error for %s: %s", method, e)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32000,
                    "message": str(e),
                },
            }

    async def read_loop(self, input_stream: IO[bytes]) -> None:
        """
        Read JSON-RPC messages from Ink subprocess stdout.

        Runs in a loop, parsing messages and dispatching to handlers.
        Should be started as an asyncio task.

        Args:
            input_stream: The stream to read from (Ink subprocess stdout)
        """
        self._running = True
        loop = asyncio.get_event_loop()

        while self._running:
            try:
                # Read line from subprocess stdout in executor to avoid blocking
                line = await loop.run_in_executor(None, input_stream.readline)

                if not line:
                    # EOF - subprocess closed
                    logger.info("Ink subprocess closed connection")
                    break

                # Decode and parse
                text = line.decode("utf-8").strip() if isinstance(line, bytes) else line.strip()
                if not text:
                    continue

                try:
                    msg = json.loads(text)
                except json.JSONDecodeError as e:
                    logger.warning("Invalid JSON from Ink: %s", e)
                    continue

                # Handle request or response
                if "id" in msg and "method" in msg:
                    # Request from Ink - needs response
                    response = await self.handle_request(msg)
                    self._write_message(response)
                elif "id" in msg and ("result" in msg or "error" in msg):
                    # Response to our request
                    request_id = msg["id"]
                    if request_id in self._pending_responses:
                        self._pending_responses[request_id].set_result(msg)
                # Notifications (no id) can be logged but don't need response

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error in read loop: %s", e)

        self._running = False

    async def send_request(self, method: str, params: Optional[dict] = None) -> dict:
        """
        Send a JSON-RPC request to Ink and wait for response.

        Args:
            method: The method name
            params: Optional parameters

        Returns:
            The response result or raises on error
        """
        self._request_id += 1
        request_id = self._request_id

        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {},
        }

        # Create future for response
        future: asyncio.Future = asyncio.get_event_loop().create_future()
        self._pending_responses[request_id] = future

        try:
            self._write_message(request)
            response = await asyncio.wait_for(future, timeout=30.0)

            if "error" in response:
                raise Exception(response["error"].get("message", "Unknown error"))

            return response.get("result", {})
        finally:
            self._pending_responses.pop(request_id, None)

    def shutdown(self) -> None:
        """Send shutdown notification to Ink and stop the read loop."""
        self._write_message({
            "jsonrpc": "2.0",
            "method": "shutdown",
            "params": {},
        })
        self._running = False

    def emit_ready(self) -> None:
        """Signal to Ink that the backend is ready."""
        self._write_message({
            "jsonrpc": "2.0",
            "method": "ready",
            "params": {
                "market_id": self.market_id,
            },
        })


class MultiBridge:
    """
    Manages multiple StdioBridges for concurrent markets.

    Each market gets its own bridge instance with a unique market_id.
    All bridges share the same subprocess I/O.
    """

    def __init__(self, output_stream: Optional[IO[bytes]] = None):
        """
        Initialize the multi-bridge.

        Args:
            output_stream: Shared stream to write to Ink subprocess
        """
        self._output = output_stream
        self._bridges: Dict[str, StdioBridge] = {}

    def get_or_create(self, market_id: str) -> StdioBridge:
        """
        Get or create a bridge for a specific market.

        Args:
            market_id: Unique identifier for the market

        Returns:
            StdioBridge instance for that market
        """
        if market_id not in self._bridges:
            bridge = StdioBridge(
                output_stream=self._output,
                market_id=market_id,
            )
            self._bridges[market_id] = bridge

        return self._bridges[market_id]

    def remove(self, market_id: str) -> None:
        """Remove a bridge when a market is closed."""
        self._bridges.pop(market_id, None)

    def all_bridges(self) -> list[StdioBridge]:
        """Get all active bridges."""
        return list(self._bridges.values())

    def shutdown_all(self) -> None:
        """Shutdown all bridges."""
        for bridge in self._bridges.values():
            bridge.shutdown()
        self._bridges.clear()

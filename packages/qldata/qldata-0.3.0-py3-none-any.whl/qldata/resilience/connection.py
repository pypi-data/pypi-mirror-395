"""Connection state management for resilient streaming."""

import logging
from collections.abc import Callable
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class ConnectionState(Enum):
    """WebSocket connection states."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    FAILED = "failed"


class ConnectionStateManager:
    """Manages WebSocket connection state transitions.

    Tracks connection state and provides callbacks for state changes.
    """

    def __init__(self) -> None:
        self._state = ConnectionState.DISCONNECTED
        self._state_callbacks: dict[ConnectionState, list[Callable]] = {
            state: [] for state in ConnectionState
        }
        self._transition_callbacks: list[Callable] = []
        self._last_state_change = datetime.now(timezone.utc)
        self._reconnect_attempts = 0

    @property
    def state(self) -> ConnectionState:
        """Get current connection state."""
        return self._state

    @property
    def reconnect_attempts(self) -> int:
        """Get number of reconnection attempts."""
        return self._reconnect_attempts

    @property
    def time_in_state(self) -> float:
        """Get time in current state (seconds)."""
        return (datetime.now(timezone.utc) - self._last_state_change).total_seconds()

    def transition(self, new_state: ConnectionState) -> None:
        """Transition to a new state.

        Args:
            new_state: Target state
        """
        if new_state == self._state:
            return

        old_state = self._state
        self._state = new_state
        self._last_state_change = datetime.now(timezone.utc)

        logger.info(f"Connection state: {old_state.value} -> {new_state.value}")

        # Update reconnect counter
        if new_state == ConnectionState.RECONNECTING:
            self._reconnect_attempts += 1
        elif new_state == ConnectionState.CONNECTED:
            self._reconnect_attempts = 0

        # Trigger callbacks
        self._notify_state_callbacks(new_state)
        self._notify_transition_callbacks(old_state, new_state)

    def on_state(self, state: ConnectionState, callback: Callable) -> None:
        """Register callback for entering a specific state.

        Args:
            state: State to watch
            callback: Function to call when entering state
        """
        self._state_callbacks[state].append(callback)

    def on_transition(self, callback: Callable[[ConnectionState, ConnectionState], None]) -> None:
        """Register callback for any state transition.

        Args:
            callback: Function(old_state, new_state) to call
        """
        self._transition_callbacks.append(callback)

    def on_reconnect(self, callback: Callable) -> None:
        """Register callback for reconnection events.

        Convenience method for on_state(RECONNECTING, callback).

        Args:
            callback: Function to call when reconnecting
        """
        self.on_state(ConnectionState.RECONNECTING, callback)

    def on_connected(self, callback: Callable) -> None:
        """Register callback for successful connection.

        Args:
            callback: Function to call when connected
        """
        self.on_state(ConnectionState.CONNECTED, callback)

    def on_failed(self, callback: Callable) -> None:
        """Register callback for connection failure.

        Args:
            callback: Function to call when failed
        """
        self.on_state(ConnectionState.FAILED, callback)

    def reset(self) -> None:
        """Reset state to DISCONNECTED."""
        self.transition(ConnectionState.DISCONNECTED)

    def _notify_state_callbacks(self, state: ConnectionState) -> None:
        """Notify callbacks registered for a specific state."""
        for callback in self._state_callbacks.get(state, []):
            try:
                callback()
            except Exception as e:
                logger.error(f"Error in state callback: {e}")

    def _notify_transition_callbacks(
        self, old_state: ConnectionState, new_state: ConnectionState
    ) -> None:
        """Notify callbacks registered for transitions."""
        for callback in self._transition_callbacks:
            try:
                callback(old_state, new_state)
            except Exception as e:
                logger.error(f"Error in transition callback: {e}")

    def __repr__(self) -> str:
        return f"ConnectionStateManager(state={self._state.value}, attempts={self._reconnect_attempts})"

"""Connection metrics data models for Pipecat framework.

This module extends the core metrics system with connection-specific metrics
including connection establishment times, retry attempts, and network latencies.
"""

from typing import Optional

from pydantic import BaseModel

from pipecat.metrics.metrics import MetricsData


class ConnectionMetricsData(MetricsData):
    """Unified connection and reconnection metrics data.

    Handles both initial connection establishment and reconnection scenarios.
    For initial connections, use connect_time, success, connection_attempts.
    For reconnections, use reconnect_count, downtime, reconnect_success, reason.

    Parameters:
        connect_time: Time taken to establish connection in seconds.
        success: Whether the connection attempt was successful.
        connection_attempts: Number of connection attempts made.
        error_message: Error message if connection failed.
        connection_type: Type of connection (websocket, http, etc.).
        reconnect_count: Number of reconnection attempts (for reconnection scenarios).
        downtime: Time connection was down in seconds (for reconnection scenarios).
        reconnect_success: Whether reconnection was successful (for reconnection scenarios).
        reason: Reason for reconnection (for reconnection scenarios).
    """

    connect_time: Optional[float] = None
    success: bool = True
    connection_attempts: int = 1
    error_message: Optional[str] = None
    connection_type: Optional[str] = None
    
    # Reconnection-specific fields
    reconnect_count: Optional[int] = None
    downtime: Optional[float] = None
    reconnect_success: Optional[bool] = None
    reason: Optional[str] = None



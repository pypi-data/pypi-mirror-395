#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Frame processor metrics collection and reporting."""

import time
from typing import Optional

from loguru import logger

from pipecat.frames.frames import MetricsFrame
from pipecat.metrics.metrics import (
    LLMTokenUsage,
    LLMUsageMetricsData,
    MetricsData,
    ProcessingMetricsData,
    TTFBMetricsData,
    TTSUsageMetricsData,
)
from pipecat.metrics.connection_metrics import (
    ConnectionMetricsData,
)
from pipecat.utils.asyncio.task_manager import BaseTaskManager
from pipecat.utils.base_object import BaseObject


class FrameProcessorMetrics(BaseObject):
    """Metrics collection and reporting for frame processors.

    Provides comprehensive metrics tracking for frame processing operations,
    including timing measurements, resource usage, and performance analytics.
    Supports TTFB tracking, processing duration metrics, and usage statistics
    for LLM and TTS operations.
    """

    def __init__(self):
        """Initialize the frame processor metrics collector.

        Sets up internal state for tracking various metrics including TTFB,
        processing times, and usage statistics.
        """
        super().__init__()
        self._task_manager = None
        self._start_ttfb_time = 0
        self._start_processing_time = 0
        self._last_ttfb_time = 0
        self._should_report_ttfb = True
        self._logger = logger
        
        # Connection metrics state
        self._start_connection_time = 0
        self._connection_attempts = 0
        self._last_connection_error = None
        self._reconnection_start_time = 0
        self._reconnect_count = 0

    async def setup(self, task_manager: BaseTaskManager):
        """Set up the metrics collector with a task manager.

        Args:
            task_manager: The task manager for handling async operations.
        """
        self._task_manager = task_manager

    async def cleanup(self):
        """Clean up metrics collection resources."""
        await super().cleanup()

    @property
    def task_manager(self) -> BaseTaskManager:
        """Get the associated task manager.

        Returns:
            The task manager instance for async operations.
        """
        return self._task_manager

    @property
    def ttfb(self) -> Optional[float]:
        """Get the current TTFB value in seconds.

        Returns:
            The TTFB value in seconds, or None if not measured.
        """
        if self._last_ttfb_time > 0:
            return self._last_ttfb_time

        # If TTFB is in progress, calculate current value
        if self._start_ttfb_time > 0:
            return time.time() - self._start_ttfb_time

        return None

    def _processor_name(self):
        """Get the processor name from core metrics data."""
        return self._core_metrics_data.processor

    def _model_name(self):
        """Get the model name from core metrics data."""
        return self._core_metrics_data.model

    def set_logger(self, logger_instance):
        """Set a custom logger instance for this metrics processor."""
        self._logger = logger_instance

    def set_core_metrics_data(self, data: MetricsData):
        """Set the core metrics data for this collector.

        Args:
            data: The core metrics data containing processor and model information.
        """
        self._core_metrics_data = data

    def set_processor_name(self, name: str):
        """Set the processor name for metrics reporting.

        Args:
            name: The name of the processor to use in metrics.
        """
        self._core_metrics_data = MetricsData(processor=name)

    async def start_ttfb_metrics(self, report_only_initial_ttfb):
        """Start measuring time-to-first-byte (TTFB).

        Args:
            report_only_initial_ttfb: Whether to report only the first TTFB measurement.
        """
        if self._should_report_ttfb:
            self._start_ttfb_time = time.time()
            self._last_ttfb_time = 0
            self._should_report_ttfb = not report_only_initial_ttfb

    async def stop_ttfb_metrics(self):
        """Stop TTFB measurement and generate metrics frame.

        Returns:
            MetricsFrame containing TTFB data, or None if not measuring.
        """
        if self._start_ttfb_time == 0:
            return None

        self._last_ttfb_time = time.time() - self._start_ttfb_time
        self._logger.debug(f"{self._processor_name()} TTFB: {self._last_ttfb_time}")
        ttfb = TTFBMetricsData(
            processor=self._processor_name(), value=self._last_ttfb_time, model=self._model_name()
        )
        self._start_ttfb_time = 0
        return MetricsFrame(data=[ttfb])

    async def start_processing_metrics(self):
        """Start measuring processing time."""
        self._start_processing_time = time.time()

    async def stop_processing_metrics(self):
        """Stop processing time measurement and generate metrics frame.

        Returns:
            MetricsFrame containing processing duration data, or None if not measuring.
        """
        if self._start_processing_time == 0:
            return None

        value = time.time() - self._start_processing_time
        self._logger.debug(f"{self._processor_name()} processing time: {value}")
        processing = ProcessingMetricsData(
            processor=self._processor_name(), value=value, model=self._model_name()
        )
        self._start_processing_time = 0
        return MetricsFrame(data=[processing])

    async def start_llm_usage_metrics(self, tokens: LLMTokenUsage):
        """Record LLM token usage metrics.

        Args:
            tokens: Token usage information including prompt and completion tokens.

        Returns:
            MetricsFrame containing LLM usage data.
        """
        logstr = f"{self._processor_name()} prompt tokens: {tokens.prompt_tokens}, completion tokens: {tokens.completion_tokens}"
        if tokens.cache_read_input_tokens:
            logstr += f", cache read input tokens: {tokens.cache_read_input_tokens}"
        if tokens.reasoning_tokens:
            logstr += f", reasoning tokens: {tokens.reasoning_tokens}"
        self._logger.debug(logstr)
        value = LLMUsageMetricsData(
            processor=self._processor_name(), model=self._model_name(), value=tokens
        )
        return MetricsFrame(data=[value])

    async def start_tts_usage_metrics(self, text: str):
        """Record TTS character usage metrics.

        Args:
            text: The text being processed by TTS.

        Returns:
            MetricsFrame containing TTS usage data.
        """
        characters = TTSUsageMetricsData(
            processor=self._processor_name(), model=self._model_name(), value=len(text)
        )
        self._logger.debug(f"{self._processor_name()} usage characters: {characters.value}")
        return MetricsFrame(data=[characters])

    async def start_connection_metrics(self):
        """Start measuring connection establishment time."""
        self._start_connection_time = time.time()
        self._connection_attempts += 1
        self._last_connection_error = None

    async def stop_connection_metrics(
        self, 
        success: bool = True, 
        error: str = None,
        connection_type: str = None
    ):
        """Stop connection measurement and generate metrics frame.

        Args:
            success: Whether the connection was successful.
            error: Error message if connection failed.
            connection_type: Type of connection (websocket, http, etc.).

        Returns:
            MetricsFrame containing connection data, or None if not measuring.
        """
        if self._start_connection_time == 0:
            return None

        connect_time = time.time() - self._start_connection_time
        
        if not success:
            self._last_connection_error = error
        
        logstr = f"{self._processor_name()} connection "
        logstr += "successful" if success else f"failed: {error}"
        logstr += f" (attempt #{self._connection_attempts}, {connect_time:.3f}s)"
        
        if success:
            self._logger.debug(logstr)
        else:
            self._logger.warning(logstr)
        
        connection_data = ConnectionMetricsData(
            processor=self._processor_name(),
            model=self._model_name(),
            connect_time=round(connect_time, 3),
            success=success,
            connection_attempts=self._connection_attempts,
            error_message=error,
            connection_type=connection_type
        )
        
        self._start_connection_time = 0
        return MetricsFrame(data=[connection_data])


    async def start_reconnection_metrics(self):
        """Start measuring reconnection downtime."""
        self._reconnection_start_time = time.time()
        self._reconnect_count += 1

    async def stop_reconnection_metrics(
        self, 
        success: bool = True, 
        reason: str = None
    ):
        """Stop reconnection measurement and generate metrics frame.

        Args:
            success: Whether the reconnection was successful.
            reason: Reason for reconnection.

        Returns:
            MetricsFrame containing reconnection data, or None if not measuring.
        """
        if self._reconnection_start_time == 0:
            return None

        downtime = time.time() - self._reconnection_start_time
        
        logstr = f"{self._processor_name()} reconnection #{self._reconnect_count} "
        logstr += "successful" if success else "failed"
        logstr += f" (downtime: {downtime:.3f}s)"
        if reason:
            logstr += f" - {reason}"
        
        self._logger.debug(logstr)
        
        reconnection_data = ConnectionMetricsData(
            processor=self._processor_name(),
            model=self._model_name(),
            reconnect_count=self._reconnect_count,
            downtime=round(downtime, 3),
            reconnect_success=success,
            reason=reason
        )
        
        self._reconnection_start_time = 0
        return MetricsFrame(data=[reconnection_data])


#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Deepgram speech-to-text service implementation."""

import asyncio
import logging
import os
import socket
import time
from typing import AsyncGenerator, Callable, Dict, Optional
from urllib.parse import urlparse

from loguru import logger

from pipecat.frames.frames import (
    CancelFrame,
    EndFrame,
    ErrorFrame,
    Frame,
    InterimTranscriptionFrame,
    StartFrame,
    TranscriptionFrame,
    UserStartedSpeakingFrame,
    UserStoppedSpeakingFrame,
)
from pipecat.processors.frame_processor import FrameDirection
from pipecat.services.stt_service import STTService
from pipecat.transcriptions.language import Language
from pipecat.utils.time import time_now_iso8601
from pipecat.utils.tracing.service_decorators import traced_stt

_PROCESS_START_MONOTONIC = time.monotonic()


def _read_first_numeric_file(paths):
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as file:
                value = file.read().strip()
        except FileNotFoundError:
            continue
        except OSError:
            continue

        if not value or value == "max":
            return None

        try:
            return int(value)
        except ValueError:
            continue
    return None


def _read_proc_status_value(key):
    try:
        with open("/proc/self/status", "r", encoding="utf-8") as status_file:
            for line in status_file:
                if line.startswith(key):
                    parts = line.split()
                    if len(parts) >= 2:
                        return int(parts[1]) * 1024  # kB -> bytes
    except FileNotFoundError:
        return None
    except OSError:
        return None
    return None


def _read_cpu_throttling():
    paths = ["/sys/fs/cgroup/cpu.stat", "/sys/fs/cgroup/cpu/cpu.stat"]
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as cpu_file:
                for line in cpu_file:
                    if line.startswith("nr_throttled"):
                        parts = line.split()
                        if len(parts) >= 2:
                            return int(parts[1])
        except FileNotFoundError:
            continue
        except OSError:
            continue
    return None


def _collect_runtime_diagnostics(
    loop: Optional[asyncio.AbstractEventLoop] = None,
    extra_context: Optional[Dict] = None,
    context_provider: Optional[Callable[[], Dict]] = None,
):
    if loop is None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

    uptime_s = round(time.monotonic() - _PROCESS_START_MONOTONIC, 1)
    rss_bytes = _read_proc_status_value("VmRSS:")
    rss_mb = round(rss_bytes / (1024**2), 2) if rss_bytes else None

    cgroup_usage_bytes = _read_first_numeric_file(
        ["/sys/fs/cgroup/memory.current", "/sys/fs/cgroup/memory/memory.usage_in_bytes"]
    )
    cgroup_limit_bytes = _read_first_numeric_file(
        ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]
    )
    cgroup_usage_mb = (
        round(cgroup_usage_bytes / (1024**2), 2) if cgroup_usage_bytes is not None else None
    )
    cgroup_limit_mb = (
        round(cgroup_limit_bytes / (1024**2), 2) if cgroup_limit_bytes not in (None, 0) else None
    )
    cgroup_pct = (
        round(cgroup_usage_bytes / cgroup_limit_bytes * 100, 2)
        if cgroup_usage_bytes is not None and cgroup_limit_bytes not in (None, 0)
        else None
    )

    try:
        open_fds = len(os.listdir("/proc/self/fd"))
    except Exception:
        open_fds = None

    pending_tasks = None
    if loop:
        try:
            pending_tasks = len(asyncio.all_tasks(loop))
        except Exception:
            pending_tasks = None

    suspected_cause = "unknown"
    if cgroup_pct and cgroup_pct >= 90:
        suspected_cause = "memory_pressure"
    elif uptime_s < 180:
        suspected_cause = "pod_cold_start"

    diagnostics = {
        "uptime_s": uptime_s,
        "rss_mb": rss_mb,
        "cgroup_usage_mb": cgroup_usage_mb,
        "cgroup_limit_mb": cgroup_limit_mb,
        "cgroup_usage_pct": cgroup_pct,
        "open_fds": open_fds,
        "pending_tasks": pending_tasks,
        "suspected_cause": suspected_cause,
    }
    cpu_throttled = _read_cpu_throttling()
    if cpu_throttled is not None:
        diagnostics["cpu_nr_throttled"] = cpu_throttled

    if context_provider:
        try:
            ctx = context_provider() or {}
            if isinstance(ctx, dict):
                diagnostics.update({k: v for k, v in ctx.items() if v is not None})
        except Exception as exc:
            diagnostics["context_provider_error"] = str(exc)

    if extra_context:
        diagnostics.update({k: v for k, v in extra_context.items() if v is not None})

    return {k: v for k, v in diagnostics.items() if v is not None}


def _derive_connect_endpoint(base_url: str):
    if not base_url:
        return "api.deepgram.com", 443

    parsed = urlparse(base_url)
    host = parsed.hostname or "api.deepgram.com"
    if parsed.port:
        port = parsed.port
    elif parsed.scheme in ("https", "wss"):
        port = 443
    else:
        port = 80
    return host, port


try:
    from deepgram import (
        AsyncListenWebSocketClient,
        DeepgramClient,
        DeepgramClientOptions,
        ErrorResponse,
        LiveOptions,
        LiveResultResponse,
        LiveTranscriptionEvents,
    )
except ModuleNotFoundError as e:
    logger.error(f"Exception: {e}")
    logger.error("In order to use Deepgram, you need to `pip install pipecat-ai[deepgram]`.")
    raise Exception(f"Missing module: {e}")


class DeepgramSTTService(STTService):
    """Deepgram speech-to-text service.

    Provides real-time speech recognition using Deepgram's WebSocket API.
    Supports configurable models, languages, VAD events, and various audio
    processing options.
    """

    def __init__(
        self,
        *,
        api_key: str,
        url: str = "",
        base_url: str = "",
        sample_rate: Optional[int] = None,
        live_options: Optional[LiveOptions] = None,
        addons: Optional[Dict] = None,
        max_connect_retries: int = 3,
        connect_timeout_s: float = 2.5,
        diagnostics_context_provider: Optional[Callable[[], Dict]] = None,
        **kwargs,
    ):
        """Initialize the Deepgram STT service.

        Args:
            api_key: Deepgram API key for authentication.
            url: Custom Deepgram API base URL.

                .. deprecated:: 0.0.64
                    Parameter `url` is deprecated, use `base_url` instead.

            base_url: Custom Deepgram API base URL.
            sample_rate: Audio sample rate. If None, uses default or live_options value.
            live_options: Deepgram LiveOptions for detailed configuration.
            addons: Additional Deepgram features to enable.
            max_connect_retries: Maximum number of connection attempts before giving up.
            connect_timeout_s: Maximum time in seconds to wait for a connection attempt.
                Connection retries wait 100ms between attempts.
            diagnostics_context_provider: Optional callable returning a dict with
                additional runtime diagnostics (e.g., active call counts) to append
                to warning logs.
            **kwargs: Additional arguments passed to the parent STTService.
        """
        sample_rate = sample_rate or (live_options.sample_rate if live_options else None)
        super().__init__(sample_rate=sample_rate, **kwargs)

        if url:
            import warnings

            with warnings.catch_warnings():
                warnings.simplefilter("always")
                warnings.warn(
                    "Parameter 'url' is deprecated, use 'base_url' instead.",
                    DeprecationWarning,
                )
            base_url = url

        default_options = LiveOptions(
            encoding="linear16",
            language=Language.EN,
            model="nova-3-general",
            channels=1,
            interim_results=True,
            smart_format=True,
            punctuate=True,
            profanity_filter=True,
            vad_events=False,
        )

        merged_options = default_options.to_dict()
        if live_options:
            default_model = default_options.model
            merged_options.update(live_options.to_dict())
            # NOTE(aleix): Fixes an in deepgram-sdk where `model` is initialized
            # to the string "None" instead of the value `None`.
            if "model" in merged_options and merged_options["model"] == "None":
                merged_options["model"] = default_model

        if "language" in merged_options and isinstance(merged_options["language"], Language):
            merged_options["language"] = merged_options["language"].value

        self.set_model_name(merged_options["model"])
        self._settings = merged_options
        self._addons = addons
        self._diagnostics_context_provider = diagnostics_context_provider

        # Connection retry settings (100ms delay between retries)
        self._max_connect_retries = max_connect_retries
        self._connect_timeout_s = connect_timeout_s

        self._client = DeepgramClient(
            api_key,
            config=DeepgramClientOptions(
                url=base_url,
                options={
                    "keepalive": "true",
                    # Note: Connection timeout is enforced by asyncio.wait_for() in _connect()
                    # with the connect_timeout_s parameter (default 2.0s)
                },
                verbose=logging.ERROR,  # Enable error level and above logging
            ),
        )
        self._connect_host, self._connect_port = _derive_connect_endpoint(base_url)

        if self.vad_enabled:
            self._register_event_handler("on_speech_started")
            self._register_event_handler("on_utterance_end")

    @property
    def vad_enabled(self):
        """Check if Deepgram VAD events are enabled.

        Returns:
            True if VAD events are enabled in the current settings.
        """
        return self._settings["vad_events"]

    def can_generate_metrics(self) -> bool:
        """Check if this service can generate processing metrics.

        Returns:
            True, as Deepgram service supports metrics generation.
        """
        return True

    async def set_model(self, model: str):
        """Set the Deepgram model and reconnect.

        Args:
            model: The Deepgram model name to use.
        """
        await super().set_model(model)
        self.logger.info(f"Switching STT model to: [{model}]")
        self._settings["model"] = model
        await self._disconnect()
        await self._connect()

    async def set_language(self, language: Language):
        """Set the recognition language and reconnect.

        Args:
            language: The language to use for speech recognition.
        """
        self.logger.info(f"Switching STT language to: [{language}]")
        self._settings["language"] = language
        await self._disconnect()
        await self._connect()

    async def start(self, frame: StartFrame):
        """Start the Deepgram STT service.

        Args:
            frame: The start frame containing initialization parameters.
        """
        await super().start(frame)
        self._settings["sample_rate"] = self.sample_rate
        await self._connect()

    async def stop(self, frame: EndFrame):
        """Stop the Deepgram STT service.

        Args:
            frame: The end frame.
        """
        await super().stop(frame)
        await self._disconnect()

    async def cancel(self, frame: CancelFrame):
        """Cancel the Deepgram STT service.

        Args:
            frame: The cancel frame.
        """
        await super().cancel(frame)
        await self._disconnect()

    async def run_stt(self, audio: bytes) -> AsyncGenerator[Frame, None]:
        """Send audio data to Deepgram for transcription.

        Args:
            audio: Raw audio bytes to transcribe.

        Yields:
            Frame: None (transcription results come via WebSocket callbacks).
        """
        await self._connection.send(audio)
        yield None

    async def _connect(self):
        self.logger.debug("Attempting to connect to Deepgram...")
        await self.start_connection_metrics()

        loop = asyncio.get_running_loop()
        for attempt in range(self._max_connect_retries):
            attempt_started = time.perf_counter()
            dns_ms = await self._measure_dns_resolution(loop)
            try:
                # Clean up any previous connection attempt in background (non-blocking)
                if hasattr(self, "_connection") and self._connection is not None:
                    old_conn = self._connection
                    asyncio.create_task(self._cleanup_abandoned_connection(old_conn))

                # Create a new connection object for a clean attempt
                self._connection: AsyncListenWebSocketClient = self._client.listen.asyncwebsocket.v(
                    "1"
                )

                # Register event handlers
                self._connection.on(
                    LiveTranscriptionEvents(LiveTranscriptionEvents.Transcript), self._on_message
                )
                self._connection.on(
                    LiveTranscriptionEvents(LiveTranscriptionEvents.Error), self._on_error
                )

                if self.vad_enabled:
                    self._connection.on(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.SpeechStarted),
                        self._on_speech_started,
                    )
                    self._connection.on(
                        LiveTranscriptionEvents(LiveTranscriptionEvents.UtteranceEnd),
                        self._on_utterance_end,
                    )

                try:
                    start_result = await asyncio.wait_for(
                        self._connection.start(options=self._settings, addons=self._addons),
                        timeout=self._connect_timeout_s,
                    )
                except asyncio.TimeoutError:
                    elapsed_ms = round((time.perf_counter() - attempt_started) * 1000, 2)
                    diagnostics = _collect_runtime_diagnostics(
                        loop,
                        extra_context={
                            "dns_ms": dns_ms,
                            "connect_duration_ms": elapsed_ms,
                        },
                        context_provider=self._diagnostics_context_provider,
                    )
                    self.logger.warning(
                        (
                            "Deepgram connection attempt {}/{} timed out after {:.2f} second(s). "
                            "runtime_diagnostics={}"
                        ),
                        attempt + 1,
                        self._max_connect_retries,
                        self._connect_timeout_s,
                        diagnostics,
                    )
                    start_result = False
                except Exception as start_error:
                    elapsed_ms = round((time.perf_counter() - attempt_started) * 1000, 2)
                    diagnostics = _collect_runtime_diagnostics(
                        loop,
                        extra_context={
                            "dns_ms": dns_ms,
                            "connect_duration_ms": elapsed_ms,
                        },
                        context_provider=self._diagnostics_context_provider,
                    )
                    self.logger.warning(
                        (
                            "Deepgram connection attempt {}/{} failed with an exception: {}. "
                            "runtime_diagnostics={}"
                        ),
                        attempt + 1,
                        self._max_connect_retries,
                        start_error,
                        diagnostics,
                    )
                    start_result = False
                else:
                    if start_result:
                        elapsed_ms = round((time.perf_counter() - attempt_started) * 1000, 2)
                        diagnostics = _collect_runtime_diagnostics(
                            loop,
                            extra_context={
                                "dns_ms": dns_ms,
                                "connect_duration_ms": elapsed_ms,
                            },
                            context_provider=self._diagnostics_context_provider,
                        )
                        self.logger.info(
                            (
                                "Successfully connected to Deepgram on attempt {} in {:.2f} ms. "
                                "runtime_diagnostics={}"
                            ),
                            attempt + 1,
                            elapsed_ms,
                            diagnostics,
                        )
                        await self.stop_connection_metrics(success=True, connection_type="websocket")
                        await self.stop_reconnection_metrics(success=True, reason="successful_reconnection")
                        return  # Exit the method on success

                self.logger.warning(
                    f"Deepgram connection attempt {attempt + 1}/{self._max_connect_retries} failed."
                )

            except Exception as e:
                elapsed_ms = round((time.perf_counter() - attempt_started) * 1000, 2)
                diagnostics = _collect_runtime_diagnostics(
                    loop,
                    extra_context={
                        "dns_ms": dns_ms,
                        "connect_duration_ms": elapsed_ms,
                    },
                    context_provider=self._diagnostics_context_provider,
                )
                self.logger.warning(
                    (
                        "Deepgram connection attempt {}/{} failed with an exception: {}. "
                        "runtime_diagnostics={}"
                    ),
                    attempt + 1,
                    self._max_connect_retries,
                    e,
                    diagnostics,
                )

            # If this is not the last attempt, wait 100ms before retrying
            if attempt < self._max_connect_retries - 1:
                self.logger.info("Retrying in 0.1 second(s)...")
                await asyncio.sleep(0.1)

        error_msg = (
            f"{self}: unable to connect to Deepgram after {self._max_connect_retries} attempts."
        )
        await self.stop_connection_metrics(
            success=False, 
            error=f"Failed after {self._max_connect_retries} attempts", 
            connection_type="websocket"
        )
        await self.stop_reconnection_metrics(success=False, reason="max_retries_exceeded")
        self.logger.error(error_msg)
        await self.push_error(ErrorFrame(error_msg, fatal=True))

    async def _measure_dns_resolution(self, loop: Optional[asyncio.AbstractEventLoop]):
        if not loop or not self._connect_host:
            return None
        try:
            dns_task = loop.getaddrinfo(
                self._connect_host,
                self._connect_port,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP,
            )
            start = time.perf_counter()
            await asyncio.wait_for(dns_task, timeout=1.0)
            return round((time.perf_counter() - start) * 1000, 2)
        except Exception:
            return None

    async def _disconnect(self):
        # Guard against missing connection instance and ensure proper async check
        connection: AsyncListenWebSocketClient = getattr(self, "_connection", None)
        if connection and await connection.is_connected():
            self.logger.debug("Disconnecting from Deepgram")
            # Deepgram swallows asyncio.CancelledError internally which prevents
            # proper cancellation propagation. This issue was found with
            # parallel pipelines where `CancelFrame` was not awaited for to
            # finish in all branches and it was pushed downstream reaching the
            # end of the pipeline, which caused `cleanup()` to be called while
            # Deepgram disconnection was still finishing and therefore
            # preventing the task cancellation that occurs during `cleanup()`.
            # GH issue: https://github.com/deepgram/deepgram-python-sdk/issues/570
            await connection.finish()

    async def _cleanup_abandoned_connection(self, conn: AsyncListenWebSocketClient):
        """Clean up abandoned connection attempt in background (non-blocking).

        This prevents zombie connections from triggering spurious error events
        when they eventually timeout and call _on_error().

        Args:
            conn: The abandoned connection object to clean up.
        """
        try:
            # Try to finish with short timeout
            await asyncio.wait_for(conn.finish(), timeout=5)
            self.logger.debug("Successfully cleaned up abandoned connection")
        except Exception as e:
            # Ignore all cleanup errors - connection might not be fully started
            # This is expected and fine - we just want best-effort cleanup
            self.logger.debug(f"Abandoned connection cleanup failed: {e}")

    async def start_metrics(self):
        """Start TTFB and processing metrics collection."""
        await self.start_ttfb_metrics()
        await self.start_processing_metrics()

    async def _on_error(self, *args, **kwargs):
        error: ErrorResponse = kwargs["error"]
        self.logger.warning(f"{self} connection error, will retry: {error}")
        await self.push_error(ErrorFrame(f"{error}"))
        await self.stop_all_metrics()
        # NOTE(aleix): we don't disconnect (i.e. call finish on the connection)
        # because this triggers more errors internally in the Deepgram SDK. So,
        # we just forget about the previous connection and create a new one.
        await self.start_reconnection_metrics()
        await self._connect()

    async def _on_speech_started(self, *args, **kwargs):
        await self.start_metrics()
        await self._call_event_handler("on_speech_started", *args, **kwargs)

    async def _on_utterance_end(self, *args, **kwargs):
        await self._call_event_handler("on_utterance_end", *args, **kwargs)

    @traced_stt
    async def _handle_transcription(
        self, transcript: str, is_final: bool, language: Optional[Language] = None
    ):
        """Handle a transcription result with tracing."""
        pass

    async def _on_message(self, *args, **kwargs):
        result: LiveResultResponse = kwargs["result"]
        if len(result.channel.alternatives) == 0:
            return
        is_final = result.is_final
        transcript = result.channel.alternatives[0].transcript
        language = None
        if result.channel.alternatives[0].languages:
            language = result.channel.alternatives[0].languages[0]
            language = Language(language)
            self.logger.debug(f"Language:{language}")
        if len(transcript) > 0:
            await self.stop_ttfb_metrics()
            if is_final:
                await self.push_frame(
                    TranscriptionFrame(
                        transcript,
                        self._user_id,
                        time_now_iso8601(),
                        language,
                        result=result,
                    )
                )
                self.logger.debug(f"Final transcript: {transcript}")
                await self._handle_transcription(transcript, is_final, language)
                await self.stop_processing_metrics()
            else:
                # For interim transcriptions, just push the frame without tracing
                await self.push_frame(
                    InterimTranscriptionFrame(
                        transcript,
                        self._user_id,
                        time_now_iso8601(),
                        language,
                        result=result,
                    )
                )

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        """Process frames with Deepgram-specific handling.

        Args:
            frame: The frame to process.
            direction: The direction of frame processing.
        """
        await super().process_frame(frame, direction)

        if isinstance(frame, UserStartedSpeakingFrame) and not self.vad_enabled:
            # Start metrics if Deepgram VAD is disabled & pipeline VAD has detected speech
            await self.start_metrics()
        elif isinstance(frame, UserStoppedSpeakingFrame):
            # https://developers.deepgram.com/docs/finalize
            await self._connection.finalize()
            self.logger.trace(f"Triggered finalize event on: {frame.name=}, {direction=}")

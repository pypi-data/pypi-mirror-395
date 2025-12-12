#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

"""Vodafone Idea (VI) WebSocket frame serializer for audio streaming and call management."""

import base64
import json
from datetime import datetime, timezone
from typing import Optional

from loguru import logger
from pydantic import BaseModel

from pipecat.audio.utils import create_default_resampler
from pipecat.frames.frames import (
    AudioRawFrame,
    CancelFrame,
    EndFrame,
    Frame,
    InputAudioRawFrame,
    InputDTMFFrame,
    KeypadEntry,
    StartFrame,
    StartInterruptionFrame,
    TransportMessageFrame,
    TransportMessageUrgentFrame,
)
from pipecat.serializers.base_serializer import FrameSerializer, FrameSerializerType


class VIFrameSerializer(FrameSerializer):
    """Serializer for Vodafone Idea (VI) WebSocket protocol.

    This serializer handles converting between Pipecat frames and VI's WebSocket
    protocol for bidirectional audio streaming. It supports audio conversion, DTMF events,
    and real-time communication with VI telephony systems.

    VI WebSocket protocol requirements:
    - PCM audio format at 8kHz sample rate
    - 16-bit Linear PCM encoding
    - Base64 encoded audio payloads
    - JSON message format for control and media events
    - Bitrate: 128 Kbps

    Events (VI → Endpoint):
    - connected: WebSocket connection established
    - start: Stream session started with call/stream IDs
    - media: Audio data in Base64-encoded PCM
    - dtmf: Keypad digit pressed
    - stop: Stream ended
    - mark: Audio playback checkpoint confirmation

    Events (Endpoint → VI):
    - media: Send audio back to VI
    - mark: Request acknowledgment for audio playback
    - clear: Clear queued audio (interruption)
    - exit: Terminate session gracefully
    """

    class InputParams(BaseModel):
        """Configuration parameters for VIFrameSerializer.

        Attributes:
            vi_sample_rate: Sample rate used by VI, defaults to 8000 Hz (telephony standard).
            sample_rate: Optional override for pipeline input sample rate.
            auto_hang_up: Whether to automatically terminate call on EndFrame.
        """

        vi_sample_rate: int = 8000
        sample_rate: Optional[int] = None
        auto_hang_up: bool = False

    def __init__(
        self,
        stream_id: str,
        call_id: Optional[str] = None,
        params: Optional[InputParams] = None,
    ):
        """Initialize the VIFrameSerializer.

        Args:
            stream_id: The VI stream identifier.
            call_id: The associated VI call identifier.
            params: Configuration parameters.
        """
        self._stream_id = stream_id
        self._call_id = call_id
        self._params = params or VIFrameSerializer.InputParams()

        self._vi_sample_rate = self._params.vi_sample_rate
        self._sample_rate = 0  # Pipeline input rate
        self._call_ended = False

        self._resampler = create_default_resampler()

    @property
    def type(self) -> FrameSerializerType:
        """Gets the serializer type.

        Returns:
            The serializer type as TEXT for JSON WebSocket messages.
        """
        return FrameSerializerType.TEXT

    async def setup(self, frame: StartFrame):
        """Sets up the serializer with pipeline configuration.

        Args:
            frame: The StartFrame containing pipeline configuration.
        """
        self._sample_rate = self._params.sample_rate or frame.audio_in_sample_rate

    async def serialize(self, frame: Frame) -> str | bytes | None:
        """Serializes a Pipecat frame to VI WebSocket format.

        Handles conversion of various frame types to VI WebSocket messages.
        For EndFrames, initiates call termination if auto_hang_up is enabled.

        Args:
            frame: The Pipecat frame to serialize.

        Returns:
            Serialized data as JSON string, or None if the frame isn't handled.
        """
        if (
            self._params.auto_hang_up
            and not self._call_ended
            and isinstance(frame, (EndFrame, CancelFrame))
        ):
            self._call_ended = True
            # Return the exit event to terminate the VI session
            return await self._send_exit_event()

        elif isinstance(frame, StartInterruptionFrame):
            # Clear/interrupt command for VI - clears queued audio
            message = {
                "event": "clear",
                "stream_id": self._stream_id,
                "call_id": self._call_id,
            }
            logger.debug(f"VI: Sending clear event for stream_id: {self._stream_id}")
            return json.dumps(message)

        elif isinstance(frame, AudioRawFrame):
            if self._call_ended:
                logger.debug("VI SERIALIZE: Skipping audio - call has ended")
                return None

            # Convert PCM audio to VI format
            data = frame.audio

            # Resample to VI sample rate (8kHz)
            serialized_data = await self._resampler.resample(
                data, frame.sample_rate, self._vi_sample_rate
            )

            # Encode as base64 for transmission
            payload = base64.b64encode(serialized_data).decode("ascii")

            # VI expects media event format with Base64-encoded PCM audio
            timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

            message = {
                "event": "media",
                "stream_id": self._stream_id,
                "media": {
                    "timestamp": timestamp,
                    "chunk": len(serialized_data),  # Chunk size in bytes
                    "payload": payload,
                },
            }

            logger.debug(f"VI: Sending media event {message} for stream_id: {self._stream_id}")

            return json.dumps(message)

        elif isinstance(frame, (TransportMessageFrame, TransportMessageUrgentFrame)):
            # Pass through transport messages (for mark events, etc.)
            return json.dumps(frame.message)

        return None

    async def _send_exit_event(self):
        """Send an exit event to VI to terminate the session gracefully.

        This method is called when auto_hang_up is enabled and an EndFrame or
        CancelFrame is received. The exit event allows IVR logic to continue
        after the WebSocket session ends.
        """
        try:
            exit_event = {
                "event": "exit",
                "stream_id": self._stream_id,
                "call_id": self._call_id,
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            }

            logger.info(
                f"VI auto_hang_up: Sending exit event for stream_id: {self._stream_id}, call_id: {self._call_id}"
            )
            return json.dumps(exit_event)
        except Exception as e:
            logger.error(f"VI auto_hang_up: Failed to create exit event: {e}")
            return None

    async def deserialize(self, data: str | bytes) -> Frame | None:
        """Deserializes VI WebSocket data to Pipecat frames.

        Handles conversion of VI media events to appropriate Pipecat frames.

        Args:
            data: The raw WebSocket data from VI.

        Returns:
            A Pipecat frame corresponding to the VI event, or None if unhandled.
        """
        try:
            message = json.loads(data)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received from VI: {data}")
            return None

        # Log all incoming events for debugging and monitoring
        event = message.get("event")
        logger.debug(
            f"VI INCOMING EVENT: {event} - stream_id: {self._stream_id}, call_id: {self._call_id}"
        )

        if event == "media":
            # Handle incoming audio data from VI
            media = message.get("media", {})
            payload_base64 = media.get("payload")

            if not payload_base64:
                logger.warning("VI DESERIALIZE: No payload in VI media message")
                return None

            try:
                payload = base64.b64decode(payload_base64)
                chunk_size = len(payload)

                # Log chunk info (optional)
                logger.debug(
                    f"VI DESERIALIZE: Received audio from VI - {chunk_size} bytes at {self._vi_sample_rate}Hz"
                )

            except Exception as e:
                logger.error(f"VI DESERIALIZE: Error decoding VI audio payload: {e}")
                return None

            # Convert from VI sample rate (8kHz) to pipeline sample rate
            deserialized_data = await self._resampler.resample(
                payload,
                self._vi_sample_rate,
                self._sample_rate,
            )

            audio_frame = InputAudioRawFrame(
                audio=deserialized_data,
                num_channels=1,  # VI uses mono audio
                sample_rate=self._sample_rate,
            )
            return audio_frame

        elif event == "dtmf":
            # Handle DTMF events
            dtmf_data = message.get("dtmf", {})
            digit = dtmf_data.get("digit")

            if digit:
                try:
                    logger.info(f"VI: Received DTMF digit: {digit}")
                    return InputDTMFFrame(KeypadEntry(digit))
                except ValueError:
                    logger.warning(f"Invalid DTMF digit from VI: {digit}")
                    return None

        elif event == "connected":
            # Handle connection event
            logger.info(f"VI connection established: {message}")
            return None

        elif event == "start":
            # Handle stream start event
            logger.info(f"VI stream started: {message}")
            return None

        elif event == "stop":
            # Handle stream stop event
            logger.info(f"VI stream stopped: {message}")
            # Don't end the call here, wait for explicit exit or call end
            return None

        elif event == "mark":
            # Handle mark event - checkpoint confirming audio playback completion
            mark_data = message.get("mark", {})
            mark_name = mark_data.get("name", "unknown")
            logger.info(f"VI mark event received: {mark_name}")
            # Mark events are informational, no frame to return
            return None

        elif event == "error":
            # Handle error events
            error_msg = message.get("error", "Unknown error")
            logger.error(f"VI error: {error_msg}")
            return None

        elif event == "exit":
            # Handle exit event from VI
            logger.info("VI exit event received - terminating session")
            self._call_ended = True
            return CancelFrame()

        elif event == "call_end" or event == "callEnd":
            # Handle call end event (if VI sends this)
            logger.info("VI call end event received")
            self._call_ended = True
            return CancelFrame()

        else:
            logger.debug(f"VI UNHANDLED EVENT: {event}")

        return None

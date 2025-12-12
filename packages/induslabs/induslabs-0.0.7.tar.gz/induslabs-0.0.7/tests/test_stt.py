"""
Unit tests for STT functionality including WebSocket streaming
"""

import pytest
import asyncio
import json
from io import BytesIO
from unittest.mock import Mock, patch, MagicMock, mock_open, AsyncMock
from induslabs import Client, STTResponse, STTStreamResponse, STTSegment


@pytest.fixture
def client():
    """Create a test client"""
    return Client(api_key="test_key")


@pytest.fixture
def mock_stt_response():
    """Create a mock STT response"""
    return {
        "request_id": "stt-test-123",
        "text": "यह एक परीक्षण है",
        "language_detected": "hi",
        "audio_duration_seconds": 5.5,
        "processing_time_seconds": 1.2,
        "first_token_time_seconds": 0.05,
        "credits_used": 0.2,
    }


@pytest.fixture
def mock_audio_data():
    """Create mock audio data"""
    return b"fake_audio_data_pcm16"


class TestSTTBasic:
    """Test basic STT functionality (HTTP)"""

    @patch("requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_audio")
    def test_basic_stt_from_file(self, mock_file, mock_post, client, mock_stt_response):
        """Test basic STT from file path"""
        mock_response = Mock()
        mock_response.json.return_value = mock_stt_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = client.stt.transcribe(file="test.wav", language="hi")

        assert isinstance(result, STTResponse)
        assert result.text == "यह एक परीक्षण है"
        assert result.language_detected == "hi"
        assert result.request_id == "stt-test-123"
        assert result.audio_duration_seconds == 5.5
        assert result.processing_time_seconds == 1.2
        assert result.credits_used == 0.2

        # Verify API call
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args[1]
        assert "files" in call_kwargs
        assert "data" in call_kwargs
        assert call_kwargs["data"]["language"] == "hi"

    @patch("requests.post")
    def test_stt_from_file_object(self, mock_post, client, mock_stt_response):
        """Test STT from file-like object"""
        mock_response = Mock()
        mock_response.json.return_value = mock_stt_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        file_obj = BytesIO(b"fake_audio_data")
        result = client.stt.transcribe(file=file_obj, language="hi")

        assert isinstance(result, STTResponse)
        assert result.text == "यह एक परीक्षण है"

    @patch("requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_audio")
    def test_stt_default_parameters(self, mock_file, mock_post, client, mock_stt_response):
        """Test STT with default parameters"""
        mock_response = Mock()
        mock_response.json.return_value = mock_stt_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = client.stt.transcribe(file="test.wav")

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["data"]["chunk_length_s"] == 6
        assert call_kwargs["data"]["stride_s"] == 5.9
        assert call_kwargs["data"]["overlap_words"] == 7

    @patch("requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_audio")
    def test_stt_custom_parameters(self, mock_file, mock_post, client, mock_stt_response):
        """Test STT with custom parameters"""
        mock_response = Mock()
        mock_response.json.return_value = mock_stt_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = client.stt.transcribe(
            file="test.wav", language="en", chunk_length_s=10, stride_s=9.5, overlap_words=5
        )

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["data"]["language"] == "en"
        assert call_kwargs["data"]["chunk_length_s"] == 10
        assert call_kwargs["data"]["stride_s"] == 9.5
        assert call_kwargs["data"]["overlap_words"] == 5


class TestSTTStreaming:
    """Test WebSocket streaming STT functionality"""

    @patch("websocket.WebSocket")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_audio")
    def test_stream_basic(self, mock_file, mock_ws_class, client, mock_audio_data):
        """Test basic streaming STT"""
        mock_ws = MagicMock()
        mock_ws_class.return_value = mock_ws

        # Mock WebSocket messages
        messages = [
            json.dumps({"type": "chunk_final", "text": "यह", "start": 0.0, "end": 0.5}),
            json.dumps({"type": "chunk_final", "text": "एक", "start": 0.5, "end": 1.0}),
            json.dumps({"type": "final", "text": "यह एक परीक्षण", "request_id": "ws-123"}),
            json.dumps(
                {
                    "type": "metrics",
                    "buffer": 2.5,
                    "transcription": 0.8,
                    "total": 1.0,
                    "RTF": 0.4,
                    "request_id": "ws-123",
                }
            ),
        ]
        mock_ws.recv.side_effect = messages

        with patch.object(client.stt, "_convert_audio_to_pcm16", return_value=mock_audio_data):
            result = client.stt.transcribe_stream(file="test.wav")

        assert isinstance(result, STTStreamResponse)
        assert result.final_text == "यह एक परीक्षण"
        assert result.request_id == "ws-123"
        assert len(result.segments) == 2
        assert result.segments[0].text == "यह"
        assert result.segments[1].text == "एक"
        assert result.is_completed
        assert not result.has_error

        # Verify metrics
        assert result.metrics is not None
        assert result.metrics.buffer_duration == 2.5
        assert result.metrics.transcription_time == 0.8
        assert result.metrics.rtf == 0.4

    @patch("websocket.WebSocket")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_audio")
    def test_stream_with_callback(self, mock_file, mock_ws_class, client, mock_audio_data):
        """Test streaming STT with segment callback"""
        mock_ws = MagicMock()
        mock_ws_class.return_value = mock_ws

        messages = [
            json.dumps({"type": "chunk_final", "text": "hello", "start": 0.0, "end": 1.0}),
            json.dumps({"type": "chunk_final", "text": "world", "start": 1.0, "end": 2.0}),
            json.dumps({"type": "final", "text": "hello world", "request_id": "ws-456"}),
            json.dumps(
                {
                    "type": "metrics",
                    "buffer": 2.0,
                    "transcription": 0.5,
                    "total": 0.6,
                    "RTF": 0.3,
                    "request_id": "ws-456",
                }
            ),
        ]
        mock_ws.recv.side_effect = messages

        received_segments = []

        def on_segment(segment: STTSegment):
            received_segments.append(segment)

        with patch.object(client.stt, "_convert_audio_to_pcm16", return_value=mock_audio_data):
            result = client.stt.transcribe_stream(file="test.wav", on_segment=on_segment)

        assert len(received_segments) == 2
        assert received_segments[0].text == "hello"
        assert received_segments[1].text == "world"
        assert result.final_text == "hello world"

    @patch("websocket.WebSocket")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake_audio")
    def test_stream_error_handling(self, mock_file, mock_ws_class, client, mock_audio_data):
        """Test streaming STT error handling"""
        mock_ws = MagicMock()
        mock_ws_class.return_value = mock_ws

        messages = [
            json.dumps({"type": "error", "message": "Insufficient credits"}),
        ]
        mock_ws.recv.side_effect = messages

        with patch.object(client.stt, "_convert_audio_to_pcm16", return_value=mock_audio_data):
            result = client.stt.transcribe_stream(file="test.wav")

        assert result.has_error
        assert result.error == "Insufficient credits"
        assert result.is_completed

    @patch("websocket.WebSocket")
    def test_stream_from_file_object(self, mock_ws_class, client, mock_audio_data):
        """Test streaming STT from file-like object"""
        mock_ws = MagicMock()
        mock_ws_class.return_value = mock_ws

        messages = [
            json.dumps({"type": "final", "text": "test", "request_id": "ws-789"}),
            json.dumps(
                {
                    "type": "metrics",
                    "buffer": 1.0,
                    "transcription": 0.3,
                    "total": 0.4,
                    "RTF": 0.4,
                    "request_id": "ws-789",
                }
            ),
        ]
        mock_ws.recv.side_effect = messages

        file_obj = BytesIO(b"fake_audio_data")

        with patch.object(client.stt, "_convert_audio_to_pcm16", return_value=mock_audio_data):
            result = client.stt.transcribe_stream(file=file_obj)

        assert result.final_text == "test"


class TestSTTResponse:
    """Test STTResponse object"""

    def test_response_properties(self, mock_stt_response):
        """Test response properties"""
        result = STTResponse(mock_stt_response)

        assert result.request_id == "stt-test-123"
        assert result.text == "यह एक परीक्षण है"
        assert result.language_detected == "hi"
        assert result.audio_duration_seconds == 5.5
        assert result.processing_time_seconds == 1.2
        assert result.first_token_time_seconds == 0.05
        assert result.credits_used == 0.2

    def test_str_representation(self, mock_stt_response):
        """Test string representation"""
        result = STTResponse(mock_stt_response)
        assert str(result) == "यह एक परीक्षण है"

    def test_repr_representation(self, mock_stt_response):
        """Test repr representation"""
        result = STTResponse(mock_stt_response)
        repr_str = repr(result)
        assert "STTResponse" in repr_str
        assert "hi" in repr_str

    def test_to_dict(self, mock_stt_response):
        """Test converting to dictionary"""
        result = STTResponse(mock_stt_response)
        result_dict = result.to_dict()

        assert result_dict == mock_stt_response
        assert result_dict["text"] == "यह एक परीक्षण है"


class TestSTTStreamResponse:
    """Test STTStreamResponse object"""

    def test_empty_response(self):
        """Test empty response"""
        response = STTStreamResponse()

        assert len(response.segments) == 0
        assert response.final_text == ""
        assert response.metrics is None
        assert response.request_id is None
        assert not response.is_completed
        assert not response.has_error

    def test_add_segments(self):
        """Test adding segments"""
        response = STTStreamResponse()

        response.add_segment("hello", start=0.0, end=1.0)
        response.add_segment("world", start=1.0, end=2.0)

        assert len(response.segments) == 2
        assert response.segments[0].text == "hello"
        assert response.segments[0].start == 0.0
        assert response.segments[1].text == "world"

    def test_set_final(self):
        """Test setting final text"""
        response = STTStreamResponse()

        response.set_final("complete text", "req-123")

        assert response.final_text == "complete text"
        assert response.request_id == "req-123"

    def test_set_metrics(self):
        """Test setting metrics"""
        response = STTStreamResponse()

        response.set_metrics(
            buffer=2.5, transcription=0.8, total=1.0, rtf=0.4, request_id="req-456"
        )

        assert response.metrics is not None
        assert response.metrics.buffer_duration == 2.5
        assert response.metrics.transcription_time == 0.8
        assert response.metrics.total_time == 1.0
        assert response.metrics.rtf == 0.4

    def test_error_handling(self):
        """Test error handling"""
        response = STTStreamResponse()

        response.set_error("Something went wrong")

        assert response.has_error
        assert response.error == "Something went wrong"

    def test_completion(self):
        """Test response completion"""
        response = STTStreamResponse()

        assert not response.is_completed

        response.complete()

        assert response.is_completed

    def test_str_representation(self):
        """Test string representation"""
        response = STTStreamResponse()
        response.set_final("test text", "req-789")

        assert str(response) == "test text"

    def test_repr_representation(self):
        """Test repr representation"""
        response = STTStreamResponse()
        response.add_segment("test")
        response.complete()

        repr_str = repr(response)
        assert "STTStreamResponse" in repr_str
        assert "segments=1" in repr_str
        assert "completed" in repr_str


class TestSTTAsync:
    """Test async STT functionality"""

    @pytest.mark.asyncio
    async def test_async_stt(self, client, mock_stt_response):
        """Test async STT (HTTP)"""
        with patch("aiohttp.ClientSession.post") as mock_post:
            mock_response = MagicMock()

            async def mock_json():
                return mock_stt_response

            mock_response.json = mock_json
            mock_response.raise_for_status = Mock()

            mock_post.return_value.__aenter__.return_value = mock_response

            with patch("builtins.open", mock_open(read_data=b"fake_audio")):
                result = await client.stt.transcribe_async(file="test.wav", language="hi")

            assert isinstance(result, STTResponse)
            assert result.text == "यह एक परीक्षण है"

            await client.close()

    @pytest.mark.asyncio
    async def test_async_stream_stt(self, client, mock_audio_data):
        """Test async streaming STT (WebSocket)"""

        # Mock WebSocket connection
        mock_ws = AsyncMock()

        messages = [
            MagicMock(
                type=1,  # WSMsgType.TEXT
                data=json.dumps({"type": "chunk_final", "text": "hello", "start": 0.0, "end": 1.0}),
            ),
            MagicMock(
                type=1,
                data=json.dumps(
                    {"type": "final", "text": "hello world", "request_id": "ws-async-123"}
                ),
            ),
            MagicMock(
                type=1,
                data=json.dumps(
                    {
                        "type": "metrics",
                        "buffer": 1.5,
                        "transcription": 0.4,
                        "total": 0.5,
                        "RTF": 0.33,
                        "request_id": "ws-async-123",
                    }
                ),
            ),
        ]

        # Create an async iterator for messages
        async def message_iterator():
            for msg in messages:
                yield msg

        # Properly configure the mock to support async iteration
        mock_ws.__aiter__ = lambda self: message_iterator()

        # Create a mock context manager that returns the mock_ws
        mock_ws_context = AsyncMock()
        mock_ws_context.__aenter__.return_value = mock_ws
        mock_ws_context.__aexit__.return_value = None

        with patch("aiohttp.ClientSession.ws_connect", return_value=mock_ws_context):
            with patch("builtins.open", mock_open(read_data=b"fake_audio")):
                with patch.object(
                    client.stt, "_convert_audio_to_pcm16", return_value=mock_audio_data
                ):
                    result = await client.stt.transcribe_stream_async(file="test.wav")

        assert isinstance(result, STTStreamResponse)
        assert result.final_text == "hello world"
        assert result.request_id == "ws-async-123"
        assert len(result.segments) == 1

        await client.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Speech-to-Text Examples - WebSocket Streaming
"""
import os
import asyncio
from induslabs import Client, STTSegment


def main():
    client = Client()

    # Example 1: Basic transcription from file path
    print("Example 1: Basic Transcription")
    print("=" * 60)
    
    audio_file = "test_audio.wav"
    
    if os.path.exists(audio_file):
        result = client.stt.transcribe(file=audio_file)
        print(f"Transcription: {result.text}")
        print(f"\nDetailed Information:")
        print(f"  Request ID: {result.request_id}")
        if result.metrics:
            print(f"  Audio Duration: {result.metrics.buffer_duration:.2f}s")
            print(f"  Processing Time: {result.metrics.transcription_time:.2f}s")
            print(f"  Total Time: {result.metrics.total_time:.2f}s")
            print(f"  Real-time Factor (RTF): {result.metrics.rtf:.3f}")
    else:
        print(f"Audio file '{audio_file}' not found.")
        print("Creating a sample audio file using TTS...")
        
        # Create sample audio
        tts_response = client.tts.speak(
            text="यह एक टेस्ट है। भाषण से पाठ रूपांतरण का परीक्षण।",
            voice="Indus-hi-Urvashi",
        )
        tts_response.save(audio_file)
        print(f"Created {audio_file}")
        
        # Now transcribe
        result = client.stt.transcribe(file=audio_file)
        print(f"\nTranscription: {result.text}")

    # Example 2: Transcription with segment callback
    print("\n\nExample 2: Transcription with Real-time Segments")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        print("Transcribing with real-time segment callbacks...")
        print("Segments will appear as they're transcribed:\n")
        
        # Define callback to handle segments as they arrive
        def on_segment(segment: STTSegment):
            print(f"  📝 Segment: '{segment.text}' [{segment.start:.2f}s - {segment.end:.2f}s]")
        
        # Transcribe with segment callbacks
        result = client.stt.transcribe(
            file=audio_file,
            on_segment=on_segment
        )
        
        print(f"\n✅ Complete transcription: {result.text}")
        print(f"\nRequest ID: {result.request_id}")
        print(f"Total segments: {len(result.segments)}")
        
        if result.metrics:
            print(f"\nPerformance Metrics:")
            print(f"  Buffer Duration: {result.metrics.buffer_duration:.3f}s")
            print(f"  Transcription Time: {result.metrics.transcription_time:.3f}s")
            print(f"  Total Time: {result.metrics.total_time:.3f}s")
            print(f"  Real-time Factor (RTF): {result.metrics.rtf:.3f}")
        
        if result.has_error:
            print(f"\n❌ Error: {result.error}")

    # Example 3: Transcribe from file object
    print("\n\nExample 3: Transcription from file object")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        with open(audio_file, "rb") as f:
            result = client.stt.transcribe(file=f)
            print(f"Transcription: {result.text}")
            if result.metrics:
                print(f"Processing time: {result.metrics.transcription_time:.2f}s")

    # Example 4: Working with result objects
    print("\n\nExample 4: Working with result objects")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        result = client.stt.transcribe(audio_file)
        
        # String representation
        print(f"As string: {str(result)}")
        
        # Accessing segments
        print(f"\nSegments ({len(result.segments)}):")
        for i, segment in enumerate(result.segments, 1):
            print(f"  {i}. '{segment.text}' [{segment.start:.2f}s - {segment.end:.2f}s]")
        
        # Dict representation
        result_dict = result.to_dict()
        print(f"\nAs dictionary keys: {list(result_dict.keys())}")

    # Example 5: Custom chunk size
    print("\n\nExample 5: Custom chunk size")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        # Smaller chunks for more frequent updates
        result = client.stt.transcribe(
            file=audio_file,
            chunk_size=4096  # Smaller chunks
        )
        print(f"Transcription: {result.text}")
        print(f"Segments received: {len(result.segments)}")


async def async_examples():
    """Async examples for WebSocket streaming"""
    
    print("\n\n" + "=" * 60)
    print("ASYNC EXAMPLES")
    print("=" * 60)
    
    async with Client() as client:
        audio_file = "test_audio.wav"
        
        if not os.path.exists(audio_file):
            print(f"Audio file '{audio_file}' not found. Skipping async examples.")
            return
        
        # Example 6: Async transcription
        print("\nExample 6: Async Transcription")
        print("-" * 60)
        
        result = await client.stt.transcribe_async(audio_file)
        print(f"Transcription: {result.text}")
        if result.metrics:
            print(f"Processing time: {result.metrics.transcription_time:.2f}s")
        
        # Example 7: Async with segment callbacks
        print("\nExample 7: Async with Segment Callbacks")
        print("-" * 60)
        
        segments_received = []
        
        def on_segment(segment: STTSegment):
            segments_received.append(segment)
            print(f"  📝 Segment: '{segment.text}'")
        
        result = await client.stt.transcribe_async(
            audio_file,
            on_segment=on_segment
        )
        
        print(f"\n✅ Complete: {result.text}")
        print(f"Total segments: {len(segments_received)}")
        
        # Example 8: Parallel transcriptions
        print("\nExample 8: Parallel Async Transcriptions")
        print("-" * 60)
        
        # Transcribe the same file multiple times in parallel
        tasks = [
            client.stt.transcribe_async(audio_file)
            for _ in range(3)
        ]
        
        results = await asyncio.gather(*tasks)
        
        for i, result in enumerate(results, 1):
            print(f"  Result {i}: {result.text[:30]}...")
            if result.metrics:
                print(f"    RTF: {result.metrics.rtf:.3f}")


def streaming_with_progress():
    """Example showing progress indication with segment callbacks"""
    
    print("\n\n" + "=" * 60)
    print("STREAMING WITH PROGRESS INDICATION")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    segment_count = 0
    
    def progress_callback(segment: STTSegment):
        nonlocal segment_count
        segment_count += 1
        
        # Show progress
        print(f"\r  Progress: {segment_count} segments transcribed...", end="", flush=True)
    
    print("Starting transcription with progress updates...")
    
    result = client.stt.transcribe(
        audio_file,
        on_segment=progress_callback
    )
    
    print()  # New line after progress
    print(f"\n✅ Transcription complete!")
    print(f"   Total segments: {segment_count}")
    print(f"   Final text: {result.text}")
    
    if result.metrics:
        print(f"   RTF: {result.metrics.rtf:.3f} (lower is faster)")


def error_handling_example():
    """Example showing error handling"""
    
    print("\n\n" + "=" * 60)
    print("ERROR HANDLING")
    print("=" * 60)
    
    client = Client()
    
    # Example with non-existent file
    try:
        result = client.stt.transcribe("nonexistent.wav")
        if result.has_error:
            print(f"Transcription Error: {result.error}")
    except Exception as e:
        print(f"Error (expected): {e}")
    
    # Example with invalid audio data
    try:
        import io
        invalid_data = io.BytesIO(b"not valid audio data")
        result = client.stt.transcribe(invalid_data)
        if result.has_error:
            print(f"Invalid Audio Error: {result.error}")
    except Exception as e:
        print(f"Invalid Audio Error (expected): {e}")


def live_transcription_simulation():
    """Simulate live transcription with accumulated text"""
    
    print("\n\n" + "=" * 60)
    print("LIVE TRANSCRIPTION SIMULATION")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    accumulated_text = []
    
    def live_callback(segment: STTSegment):
        accumulated_text.append(segment.text)
        
        # Clear line and show accumulated transcription
        print(f"\r  Live: {' '.join(accumulated_text)}", end="", flush=True)
    
    print("Simulating live transcription (accumulated text)...\n")
    
    result = client.stt.transcribe(
        audio_file,
        on_segment=live_callback
    )
    
    print()  # New line
    print(f"\n✅ Final: {result.text}")


def performance_metrics_example():
    """Example focusing on performance metrics"""
    
    print("\n\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    import time
    
    start_time = time.time()
    result = client.stt.transcribe(audio_file)
    wall_time = time.time() - start_time
    
    print(f"Transcription: {result.text}")
    print(f"\nPerformance Analysis:")
    print(f"  Wall clock time: {wall_time:.3f}s")
    
    if result.metrics:
        print(f"  Audio duration: {result.metrics.buffer_duration:.3f}s")
        print(f"  Transcription time: {result.metrics.transcription_time:.3f}s")
        print(f"  Total time (server): {result.metrics.total_time:.3f}s")
        print(f"  Real-time Factor: {result.metrics.rtf:.3f}")
        
        # Calculate additional metrics
        speedup = result.metrics.buffer_duration / result.metrics.transcription_time
        print(f"  Speedup: {speedup:.2f}x (audio duration / processing time)")
        
        if result.metrics.rtf:
            print(f"\nInterpretation:")
            if result.metrics.rtf < 1.0:
                print(f"  ✅ Faster than real-time (RTF < 1.0)")
            else:
                print(f"  ⚠️  Slower than real-time (RTF > 1.0)")


if __name__ == "__main__":
    # Run synchronous examples
    main()
    
    # Run async examples
    asyncio.run(async_examples())
    
    # Additional examples
    streaming_with_progress()
    error_handling_example()
    live_transcription_simulation()
    performance_metrics_example()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
"""
Speech-to-Text Examples - WebSocket Streaming with Model and Streaming Parameters
"""
import os
import asyncio
from induslabs import Client, STTSegment


# --- NEW ERROR HANDLING FUNCTION ---
def handle_expected_error(func, *args, **kwargs):
    """Helper to catch expected ValueErrors due to validation."""
    try:
        func(*args, **kwargs)
        print("  ❌ Test Failed: Expected ValueError was not raised.")
    except ValueError as e:
        print(f"  ✅ Caught expected error: {e}")
    except Exception as e:
        print(f"  ❌ Caught unexpected exception: {e}")
# --- END NEW ERROR HANDLING FUNCTION ---


def main():
    # client needs to be created without 'async with' to run synchronous examples
    client = Client()

    # Example 1: Basic transcription with default model
    print("Example 1: Basic Transcription (Default Model)")
    print("=" * 60)
    
    audio_file = "test_audio.wav"
    
    if os.path.exists(audio_file):
        result = client.stt.transcribe(
            file=audio_file,
            model="default",
            streaming=False # UPDATED to bool
        )
        print(f"Transcription: {result.text}")
        print(f"\nDetailed Information:")
        print(f"  Request ID: {result.request_id}")
        print(f"  Model: default")
        print(f"  Streaming: False")
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
        result = client.stt.transcribe(
            file=audio_file,
            model="default",
            streaming=False # UPDATED to bool
        )
        print(f"\nTranscription: {result.text}")

    # Example 2: Transcription with hi-en model
    print("\n\nExample 2: Transcription with Hi-En Model")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        result = client.stt.transcribe(
            file=audio_file,
            model="hi-en",
            streaming=False, # UPDATED to bool
            language="hindi"
        )
        print(f"Transcription: {result.text}")
        print(f"Model: hi-en")
        print(f"Language: hindi")
        if result.metrics:
            print(f"Processing time: {result.metrics.transcription_time:.2f}s")

    # Example 3: Streaming mode with default model (NOW EXPECTED TO FAIL)
    print("\n\nExample 3: Streaming Mode with Default Model (Testing Validation)")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        print("Attempting to transcribe with streaming=True and model='default'...")
        
        def on_segment(segment: STTSegment):
            print(f"  📝 Segment: '{segment.text}'") # Should not print
        
        handle_expected_error(
            client.stt.transcribe,
            file=audio_file,
            model="default",
            streaming=True, # UPDATED to bool
            on_segment=on_segment
        )

    # Example 4: Streaming mode with hi-en model (VALID)
    print("\n\nExample 4: Streaming Mode with Hi-En Model (VALID)")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        print("Transcribing with hi-en model and streaming...\n")
        
        def on_segment(segment: STTSegment):
            print(f"  📝 [{segment.start:.2f}s] {segment.text}")
        
        result = client.stt.transcribe(
            file=audio_file,
            model="hi-en",
            streaming=True, # UPDATED to bool
            language="hindi",
            on_segment=on_segment
        )
        
        print(f"\n✅ Complete: {result.text}")
        print(f"Model: hi-en, Streaming: True")
        if result.metrics:
            print(f"RTF: {result.metrics.rtf:.3f}")

    # Example 5: Comparing models
    print("\n\nExample 5: Comparing Default vs Hi-En Model")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        print("Testing with default model (non-streaming)...")
        result_default = client.stt.transcribe(
            file=audio_file,
            model="default",
            streaming=False # UPDATED to bool
        )
        
        print("Testing with hi-en model (streaming)...")
        result_hien = client.stt.transcribe(
            file=audio_file,
            model="hi-en",
            streaming=True, # UPDATED to bool
            language="hindi"
        )
        
        print("\nComparison Results:")
        print(f"  Default Model: {result_default.text}")
        if result_default.metrics:
            print(f"    RTF: {result_default.metrics.rtf:.3f}")
        
        print(f"\n  Hi-En Model: {result_hien.text}")
        if result_hien.metrics:
            print(f"    RTF: {result_hien.metrics.rtf:.3f}")

    # Example 6: All parameter combinations (UPDATED TO REFLECT NEW VALIDATION)
    print("\n\nExample 6: Testing All Parameter Combinations (Valid/Invalid)")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        combinations = [
            ("default", False, "Valid - Non-Streaming"),
            ("default", True, "Invalid - Streaming=True requires hi-en"),
            ("hi-en", False, "Valid - Non-Streaming"),
            ("hi-en", True, "Valid - Streaming"),
        ]
        
        for model, streaming, status in combinations:
            print(f"\nTesting: model={model}, streaming={streaming} ({status})")
            
            if status.startswith("Invalid"):
                handle_expected_error(
                    client.stt.transcribe,
                    file=audio_file,
                    model=model,
                    streaming=streaming,
                    language="hindi" if model == "hi-en" else None
                )
            else:
                result = client.stt.transcribe(
                    file=audio_file,
                    model=model,
                    streaming=streaming,
                    language="hindi" if model == "hi-en" else None
                )
                print(f"  Result: {result.text[:50]}...")
                if result.metrics:
                    print(f"  RTF: {result.metrics.rtf:.3f}")

    # Example 7: Custom chunk size with streaming (Model changed to hi-en)
    print("\n\nExample 7: Custom Chunk Size with Streaming")
    print("=" * 60)
    
    if os.path.exists(audio_file):
        result = client.stt.transcribe(
            file=audio_file,
            model="hi-en", # CHANGED to hi-en to be valid for streaming=True
            streaming=True, # UPDATED to bool
            chunk_size=4096,
            language="hindi",
            on_segment=lambda s: print(f"  📝 {s.text}")
        )
        print(f"\n✅ Complete: {result.text}")
        print(f"Segments received: {len(result.segments)}")


async def async_examples():
    """Async examples with model and streaming parameters"""
    
    print("\n\n" + "=" * 60)
    print("ASYNC EXAMPLES WITH MODEL & STREAMING PARAMETERS")
    print("=" * 60)
    
    async with Client() as client:
        audio_file = "test_audio.wav"
        
        if not os.path.exists(audio_file):
            print(f"Audio file '{audio_file}' not found. Skipping async examples.")
            return
        
        # Example 8: Async with default model
        print("\nExample 8: Async with Default Model")
        print("-" * 60)
        
        result = await client.stt.transcribe_async(
            audio_file,
            model="default",
            streaming=False # UPDATED to bool
        )
        print(f"Transcription: {result.text}")
        print(f"Model: default, Streaming: False")
        if result.metrics:
            print(f"Processing time: {result.metrics.transcription_time:.2f}s")
        
        # Example 9: Async with hi-en model and streaming
        print("\nExample 9: Async with Hi-En Model and Streaming")
        print("-" * 60)
        
        segments_received = []
        
        def on_segment(segment: STTSegment):
            segments_received.append(segment)
            print(f"  📝 Segment: '{segment.text}'")
        
        result = await client.stt.transcribe_async(
            audio_file,
            model="hi-en",
            streaming=True, # UPDATED to bool
            language="hindi",
            on_segment=on_segment
        )
        
        print(f"\n✅ Complete: {result.text}")
        print(f"Model: hi-en, Streaming: True")
        print(f"Total segments: {len(segments_received)}")
        
        # Example 10: Parallel transcriptions with different models
        print("\nExample 10: Parallel Async Transcriptions (Different Models)")
        print("-" * 60)
        
        tasks = []
        
        # Valid: default (no stream)
        tasks.append(
            client.stt.transcribe_async(
                audio_file,
                model="default",
                streaming=False # UPDATED to bool
            )
        )
        # Valid: hi-en (no stream)
        tasks.append(
            client.stt.transcribe_async(
                audio_file,
                model="hi-en",
                streaming=False, # UPDATED to bool
                language="hindi"
            )
        )
        # Valid: hi-en (stream)
        tasks.append(
            client.stt.transcribe_async(
                audio_file,
                model="hi-en", # CHANGED to hi-en to be valid for streaming=True
                streaming=True, # UPDATED to bool
                language="hindi"
            )
        )
        
        results = await asyncio.gather(*tasks)
        
        models = ["default (no stream)", "hi-en (no stream)", "hi-en (stream)"]
        for i, (result, model_desc) in enumerate(zip(results, models), 1):
            print(f"  Result {i} ({model_desc}): {result.text[:40]}...")
            if result.metrics:
                print(f"    RTF: {result.metrics.rtf:.3f}")


def streaming_comparison():
    """Compare streaming vs non-streaming modes"""
    
    print("\n\n" + "=" * 60)
    print("STREAMING VS NON-STREAMING COMPARISON")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    # Non-Streaming (Valid with default)
    print("Testing Non-Streaming Mode (Model: default)...")
    segment_count_nonstream = 0
    
    def callback_nonstream(segment: STTSegment):
        nonlocal segment_count_nonstream
        segment_count_nonstream += 1
    
    result_nonstream = client.stt.transcribe(
        audio_file,
        model="default",
        streaming=False, # UPDATED to bool
        on_segment=callback_nonstream
    )
    
    print(f"  Segments: {segment_count_nonstream}")
    if result_nonstream.metrics:
        print(f"  RTF: {result_nonstream.metrics.rtf:.3f}")
    
    # Streaming (Valid with hi-en)
    print("\nTesting Streaming Mode (Model: hi-en)...")
    segment_count_stream = 0
    
    def callback_stream(segment: STTSegment):
        nonlocal segment_count_stream
        segment_count_stream += 1
        print(f"  📝 Segment {segment_count_stream}: {segment.text}")
    
    result_stream = client.stt.transcribe(
        audio_file,
        model="hi-en", # CHANGED to hi-en to be valid for streaming=True
        streaming=True, # UPDATED to bool
        language="hindi",
        on_segment=callback_stream
    )
    
    print(f"\n  Total segments: {segment_count_stream}")
    if result_stream.metrics:
        print(f"  RTF: {result_stream.metrics.rtf:.3f}")
    
    print("\nComparison:")
    print(f"  Non-Streaming segments (default): {segment_count_nonstream}")
    print(f"  Streaming segments (hi-en): {segment_count_stream}")
    print(f"  Non-streaming final text: {result_nonstream.text[:30]}...")
    print(f"  Streaming final text: {result_stream.text[:30]}...")


def model_comparison():
    """Compare default vs hi-en models"""
    
    print("\n\n" + "=" * 60)
    print("MODEL COMPARISON: DEFAULT vs HI-EN")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    import time
    
    print("Testing Default Model (Non-Streaming)...")
    start = time.time()
    result_default = client.stt.transcribe(
        audio_file,
        model="default",
        streaming=False # UPDATED to bool
    )
    time_default = time.time() - start
    
    print(f"  Text: {result_default.text}")
    print(f"  Wall time: {time_default:.3f}s")
    if result_default.metrics:
        print(f"  RTF: {result_default.metrics.rtf:.3f}")
    
    print("\nTesting Hi-En Model (Non-Streaming)...")
    start = time.time()
    result_hien = client.stt.transcribe(
        audio_file,
        model="hi-en",
        streaming=False, # UPDATED to bool
        language="hindi"
    )
    time_hien = time.time() - start
    
    print(f"  Text: {result_hien.text}")
    print(f"  Wall time: {time_hien:.3f}s")
    if result_hien.metrics:
        print(f"  RTF: {result_hien.metrics.rtf:.3f}")
    
    print("\nSummary (Non-Streaming):")
    print(f"  Default model wall time: {time_default:.3f}s")
    print(f"  Hi-En model wall time: {time_hien:.3f}s")
    if result_default.metrics and result_hien.metrics:
        print(f"  Default RTF: {result_default.metrics.rtf:.3f}")
        print(f"  Hi-En RTF: {result_hien.metrics.rtf:.3f}")


def error_handling_example():
    """Example showing error handling with new parameters"""
    
    print("\n\n" + "=" * 60)
    print("ERROR HANDLING WITH NEW PARAMETERS")
    print("=" * 60)
    
    client = Client()
    
    # Test for the new validation rule: streaming=True and model=default
    print("\nTest 1: Streaming=True with model='default'")
    handle_expected_error(
        client.stt.transcribe,
        "test_audio.wav",
        model="default",
        streaming=True # UPDATED to bool
    )

    # Example with invalid model (retained for completeness)
    print("\nTest 2: Invalid model parameter")
    handle_expected_error(
        client.stt.transcribe,
        "test_audio.wav",
        model="invalid-model",
        streaming=False
    )
    
    # Example with non-existent file
    print("\nTest 3: Non-existent file")
    try:
        result = client.stt.transcribe(
            "nonexistent.wav",
            model="default",
            streaming=False # UPDATED to bool
        )
        if result.has_error:
            print(f"  ℹ️  Transcription Error: {result.error}")
        else:
            print("  ❌ Test Failed: Expected error for non-existent file.")
    except Exception as e:
        print(f"  ✅ Error (expected from client/websocket): {e}")


def live_transcription_simulation():
    """Simulate live transcription with streaming enabled"""
    
    print("\n\n" + "=" * 60)
    print("LIVE TRANSCRIPTION SIMULATION (Streaming Mode)")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    accumulated_text = []
    
    def live_callback(segment: STTSegment):
        accumulated_text.append(segment.text)
        print(f"\r  Live: {' '.join(accumulated_text)}", end="", flush=True)
    
    print("Simulating live transcription with streaming=True (using hi-en model)...\n")
    
    result = client.stt.transcribe(
        audio_file,
        model="hi-en", # CHANGED to hi-en to be valid for streaming=True
        streaming=True, # UPDATED to bool
        language="hindi",
        on_segment=live_callback
    )
    
    print()  # New line
    print(f"\n✅ Final: {result.text}")
    print(f"Model: hi-en, Streaming: True")


def performance_metrics_with_params():
    """Example focusing on performance metrics with different parameters"""
    
    print("\n\n" + "=" * 60)
    print("PERFORMANCE METRICS WITH DIFFERENT PARAMETERS")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        return
    
    import time
    
    configs = [
        ("default", False, None),
        ("hi-en", False, "hindi"),
        ("hi-en", True, "hindi"), # default/True is now invalid, replaced with hi-en/True
    ]
    
    print(f"\n{'Model':<10} {'Streaming':<10} {'Wall Time':<12} {'RTF':<8} {'Result'}")
    print("-" * 60)
    
    for model, streaming, language in configs:
        start_time = time.time()
        result = client.stt.transcribe(
            audio_file,
            model=model,
            streaming=streaming,
            language=language
        )
        wall_time = time.time() - start_time
        
        rtf_str = f"{result.metrics.rtf:.3f}" if result.metrics else "N/A"
        text_preview = result.text[:30] + "..." if len(result.text) > 30 else result.text
        
        print(f"{model:<10} {str(streaming):<10} {wall_time:<12.3f} {rtf_str:<8} {text_preview}")
    
    print("\nInterpretation:")
    print("  - RTF < 1.0: Faster than real-time")
    print("  - RTF > 1.0: Slower than real-time")
    print("  - Streaming mode is typically for real-time applications.")


def comprehensive_test():
    """Comprehensive test of all scenarios"""
    
    print("\n\n" + "=" * 60)
    print("COMPREHENSIVE TEST: ALL SCENARIOS")
    print("=" * 60)
    
    client = Client()
    audio_file = "test_audio.wav"
    
    if not os.path.exists(audio_file):
        print(f"Audio file '{audio_file}' not found.")
        print("Please create test_audio.wav first.")
        return
    
    scenarios = [
        ("Default / Non-Streaming", "default", False, None, True),
        ("Default / Streaming", "default", True, None, False), # Invalid
        ("Hi-En / Non-Streaming", "hi-en", False, "hindi", True),
        ("Hi-En / Streaming", "hi-en", True, "hindi", True),
    ]
    
    results = {}
    
    for name, model, streaming, language, is_valid in scenarios:
        print(f"\n--- Testing: {name} ---")
        
        if not is_valid:
            handle_expected_error(
                client.stt.transcribe,
                audio_file,
                model=model,
                streaming=streaming,
                language=language
            )
            continue
            
        segment_count = 0
        def count_segments(s):
            nonlocal segment_count
            segment_count += 1
        
        result = client.stt.transcribe(
            audio_file,
            model=model,
            streaming=streaming,
            language=language,
            on_segment=count_segments
        )
        
        results[name] = {
            'text': result.text,
            'segments': segment_count,
            'rtf': result.metrics.rtf if result.metrics else None
        }
        
        print(f"  ✅ Segments: {segment_count}")
        print(f"  ✅ Text: {result.text[:50]}...")
        if result.metrics:
            print(f"  ✅ RTF: {result.metrics.rtf:.3f}")
    
    print("\n" + "=" * 60)
    print("SUMMARY OF VALID SCENARIOS")
    print("=" * 60)
    
    for name, data in results.items():
        if data['rtf'] is not None: # Only show valid scenarios that completed
            print(f"\n{name}:")
            print(f"  Segments: {data['segments']}")
            print(f"  RTF: {data['rtf']:.3f}")
            print(f"  Text length: {len(data['text'])} chars")


if __name__ == "__main__":
    # Run synchronous examples
    main()
    
    # Run async examples
    asyncio.run(async_examples())
    
    # Additional comparison examples
    streaming_comparison()
    model_comparison()
    error_handling_example()
    live_transcription_simulation()
    performance_metrics_with_params()
    comprehensive_test()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
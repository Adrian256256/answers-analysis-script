import json
import os
import requests
import tempfile
from pathlib import Path

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️  Whisper not installed. Run: pip install openai-whisper")

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    print("⚠️  SpeechRecognition not installed. Run: pip install SpeechRecognition")

# Load the JSON data
print("Loading data from final.json...")
with open('../data/final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Audio files directory already exists
audio_dir = Path('../data/audio_files')

def download_audio(url, output_path):
    """Download audio file from URL"""
    try:
        print(f"    Downloading audio...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"    ❌ Error downloading: {e}")
        return False

def transcribe_with_whisper(audio_path, model):
    """Transcribe audio using Whisper with optimized settings for accuracy"""
    try:
        print(f"    Transcribing with Whisper (high accuracy mode)...")
        result = model.transcribe(
            str(audio_path),
            language="en",  # Force English for better technical term recognition
            initial_prompt="Computer science exam. Technical terms: merge sort, heap sort, bubble sort, quick sort, insertion sort, binary search, linear search, polymorphism, inheritance, encapsulation, overloading, overriding, RAM, ROM, DRAM, SRAM, CPU, ALU, cache, control unit, LAN, WAN, network, router, switch, HTTP, HTTPS, port, binary, algorithm, data structure, queue, stack, tree, graph, complexity, Big O notation, SQL, WHERE, TRUNCATE, destructor, constructor, delete, new, kernel, driver, compiler, operating system, Dijkstra, greedy, round robin, scheduling, IPv4, IPv6, MAC address, Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday.",
            verbose=False,  # Don't print progress bar
            temperature=0.0,  # More deterministic (less creative guessing)
            beam_size=5,  # Better beam search for accuracy
            best_of=5,  # Consider multiple candidates
            fp16=False,  # Use FP32 for better accuracy on CPU
            compression_ratio_threshold=2.4,  # Detect and avoid repetitions
            logprob_threshold=-1.0,  # Filter out low confidence results
            no_speech_threshold=0.6,  # Better silence detection
            condition_on_previous_text=True,  # Use context from previous segments
            word_timestamps=False  # Focus on transcription accuracy, not timing
        )
        return result["text"].strip()
    except Exception as e:
        print(f"    ❌ Whisper transcription failed: {e}")
        return None

def transcribe_with_speech_recognition(audio_path):
    """Transcribe audio using SpeechRecognition (Google)"""
    try:
        print(f"    Transcribing with Google Speech Recognition...")
        recognizer = sr.Recognizer()
        with sr.AudioFile(str(audio_path)) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text.strip()
    except Exception as e:
        print(f"    ❌ Speech Recognition failed: {e}")
        return None

def count_audio_answers(data):
    """Count total audio answers in the dataset"""
    count = 0
    
    # Count in examProgress
    for user_id, user_data in data.get('examProgress', {}).items():
        if isinstance(user_data, dict) and 'answers' in user_data:
            for answer in user_data['answers'].values():
                if 'audioUrl' in answer:
                    count += 1
    
    # Count in examResults
    for user_id, results in data.get('examResults', {}).items():
        for result_id, result_data in results.items():
            if 'answers' in result_data:
                for answer in result_data['answers'].values():
                    if 'audioUrl' in answer:
                        count += 1
    
    return count

# Count audio answers
audio_count = count_audio_answers(data)
print(f"\n📊 Found {audio_count} audio answers to transcribe\n")

if audio_count == 0:
    print("✅ No audio files need transcription!")
    exit(0)

# Check if we have transcription tools available
if not WHISPER_AVAILABLE and not SR_AVAILABLE:
    print("❌ No transcription libraries available!")
    print("\nTo transcribe audio, install one of these:")
    print("  1. OpenAI Whisper (recommended): pip install openai-whisper")
    print("  2. SpeechRecognition: pip install SpeechRecognition")
    exit(1)

print(f"🎤 Using transcription method: {'Whisper (offline) - SMALL model (high accuracy)' if WHISPER_AVAILABLE else 'Google Speech Recognition (online)'}\n")

# Load Whisper model once if available
whisper_model = None
if WHISPER_AVAILABLE:
    print("📥 Loading Whisper model (this may take a moment)...")
    print("   Using 'small' model for high accuracy (slower but much better)")
    print("   Model sizes: tiny < base < small < medium < large")
    print("   'small' provides excellent accuracy for technical terms\n")
    try:
        whisper_model = whisper.load_model("small")  # small model - high accuracy
        print("✅ Whisper model loaded!\n")
    except Exception as e:
        print(f"❌ Failed to load Whisper model: {e}")
        print("   Falling back to 'base' model...")
        try:
            whisper_model = whisper.load_model("base")
            print("✅ Base model loaded!\n")
        except:
            WHISPER_AVAILABLE = False

transcribed_count = 0
failed_count = 0
skipped_count = 0

# Process examProgress users
print("=" * 60)
print("Processing users in examProgress...")
print("=" * 60)

for user_id, user_data in data.get('examProgress', {}).items():
    if not isinstance(user_data, dict) or 'answers' not in user_data:
        continue
    
    print(f"\n👤 User: {user_id[:20]}...")
    
    for question_id, answer in user_data['answers'].items():
        if 'audioUrl' not in answer:
            continue
        
        # Check if already transcribed
        if 'transcription' in answer and answer['transcription']:
            print(f"  ⏭️  {question_id}: Already transcribed, skipping")
            skipped_count += 1
            continue
        
        audio_url = answer['audioUrl']
        print(f"  🎵 {question_id}:")
        
        # Use filename from audio_files directory if exists
        audio_filename = f"{user_id}_{question_id}.webm"
        audio_path = audio_dir / audio_filename
        
        # Download if not exists
        if not audio_path.exists():
            if not download_audio(audio_url, audio_path):
                failed_count += 1
                continue
        else:
            print(f"    Using existing audio file")
        
        # Transcribe
        transcription = None
        if WHISPER_AVAILABLE and whisper_model:
            transcription = transcribe_with_whisper(audio_path, whisper_model)
        elif SR_AVAILABLE:
            transcription = transcribe_with_speech_recognition(audio_path)
        
        if transcription:
            answer['transcription'] = transcription
            transcribed_count += 1
            print(f"    ✅ Transcribed: '{transcription[:60]}{'...' if len(transcription) > 60 else ''}'")
        else:
            answer['transcription'] = "TRANSCRIPTION_FAILED"
            failed_count += 1
            print(f"    ❌ Failed to transcribe")

# Process examResults users
print("\n" + "=" * 60)
print("Processing users in examResults...")
print("=" * 60)

for user_id, results in data.get('examResults', {}).items():
    for result_id, result_data in results.items():
        if 'answers' not in result_data:
            continue
        
        print(f"\n👤 User: {user_id[:20]}...")
        
        for question_id, answer in result_data['answers'].items():
            if 'audioUrl' not in answer:
                continue
            
            # Check if already transcribed
            if 'transcription' in answer and answer['transcription']:
                print(f"  ⏭️  {question_id}: Already transcribed, skipping")
                skipped_count += 1
                continue
            
            audio_url = answer['audioUrl']
            print(f"  🎵 {question_id}:")
            
            # Use filename from audio_files directory if exists
            audio_filename = f"{user_id}_{question_id}.webm"
            audio_path = audio_dir / audio_filename
            
            # Download if not exists
            if not audio_path.exists():
                if not download_audio(audio_url, audio_path):
                    failed_count += 1
                    continue
            else:
                print(f"    Using existing audio file")
            
            # Transcribe
            transcription = None
            if WHISPER_AVAILABLE and whisper_model:
                transcription = transcribe_with_whisper(audio_path, whisper_model)
            elif SR_AVAILABLE:
                transcription = transcribe_with_speech_recognition(audio_path)
            
            if transcription:
                answer['transcription'] = transcription
                transcribed_count += 1
                print(f"    ✅ Transcribed: '{transcription[:60]}{'...' if len(transcription) > 60 else ''}'")
            else:
                answer['transcription'] = "TRANSCRIPTION_FAILED"
                failed_count += 1
                print(f"    ❌ Failed to transcribe")

# Save updated data
output_file = '../data/final_with_transcriptions.json'
print("\n" + "=" * 60)
print("Saving transcriptions...")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Summary
print("\n" + "=" * 60)
print("🎉 TRANSCRIPTION COMPLETE!")
print("=" * 60)
print(f"📊 Statistics:")
print(f"  - Total audio files: {audio_count}")
print(f"  - Successfully transcribed: {transcribed_count}")
print(f"  - Failed: {failed_count}")
print(f"  - Skipped (already done): {skipped_count}")
print(f"\n💾 Updated data saved to: {output_file}")
print(f"📁 Audio files in: {audio_dir}/")
print("\n💡 Tip: Run generate_csv.py again to include transcriptions in CSVs")

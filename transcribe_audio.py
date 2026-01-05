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
    print("⚠️  Whisper not installed. Installing now...")

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

# Load the simplified JSON
with open('simplified_exam_data.json', 'r') as f:
    data = json.load(f)

# Create a directory for downloaded audio files
audio_dir = Path('audio_files')
audio_dir.mkdir(exist_ok=True)

def download_audio(url, output_path):
    """Download audio file from URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"  ❌ Error downloading: {e}")
        return False

def transcribe_with_whisper(audio_path):
    """Transcribe audio using Whisper"""
    try:
        # Using 'medium' model for best accuracy
        model = whisper.load_model("medium")  # Options: tiny, base, small, medium, large
        result = model.transcribe(
            str(audio_path),
            language="en",  # Force English for better technical term recognition
            initial_prompt="Computer science technical exam answer. Common terms: merge sort, heap sort, bubble sort, quick sort, polymorphism, inheritance, encapsulation, network, algorithm"
        )
        return result["text"].strip()
    except Exception as e:
        print(f"  ❌ Whisper transcription failed: {e}")
        return None

def transcribe_with_speech_recognition(audio_path):
    """Transcribe audio using SpeechRecognition (Google)"""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(str(audio_path)) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text.strip()
    except Exception as e:
        print(f"  ❌ Speech Recognition failed: {e}")
        return None

# Count audio answers
audio_count = 0
transcribed_count = 0

for user in data['users']:
    for answer in user['answers']:
        if answer.get('answer_type') == 'audio' and answer.get('audio_url'):
            if answer.get('transcription') == "NOT_AVAILABLE_IN_SOURCE_DATA":
                audio_count += 1

print(f"🎤 Found {audio_count} audio answers to transcribe\n")

if audio_count == 0:
    print("✅ No audio files need transcription!")
    exit(0)

# Check if we have transcription tools available
if not WHISPER_AVAILABLE and not SR_AVAILABLE:
    print("❌ No transcription libraries available!")
    print("\nTo transcribe audio, install one of these:")
    print("  1. OpenAI Whisper (recommended): pip install openai-whisper")
    print("  2. SpeechRecognition: pip install SpeechRecognition pydub")
    exit(1)

print(f"Using transcription method: {'Whisper (offline) - MEDIUM model' if WHISPER_AVAILABLE else 'Google Speech Recognition (online)'}\n")

# Process each user's answers
for user_idx, user in enumerate(data['users']):
    print(f"Processing user {user_idx + 1}/{len(data['users'])}: {user['user_id'][:10]}...")
    
    for answer_idx, answer in enumerate(user['answers']):
        if answer.get('answer_type') == 'audio' and answer.get('audio_url'):
            if answer.get('transcription') == "NOT_AVAILABLE_IN_SOURCE_DATA":
                audio_url = answer['audio_url']
                question_id = answer['question_id']
                
                print(f"  Transcribing {question_id}...")
                
                # Download audio file
                audio_filename = f"{user['user_id']}_{question_id}.webm"
                audio_path = audio_dir / audio_filename
                
                if not audio_path.exists():
                    if not download_audio(audio_url, audio_path):
                        continue
                
                # Transcribe
                transcription = None
                if WHISPER_AVAILABLE:
                    transcription = transcribe_with_whisper(audio_path)
                elif SR_AVAILABLE:
                    transcription = transcribe_with_speech_recognition(audio_path)
                
                if transcription:
                    answer['transcription'] = transcription
                    if 'user_answer' not in answer or not answer['user_answer']:
                        answer['user_answer'] = transcription
                    transcribed_count += 1
                    print(f"  ✅ Transcribed: '{transcription[:50]}...'")
                else:
                    answer['transcription'] = "TRANSCRIPTION_FAILED"
                    print(f"  ⚠️  Failed to transcribe")

# Save updated data
output_file = 'simplified_exam_data_with_transcriptions.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Transcription complete!")
print(f"  • Total audio files: {audio_count}")
print(f"  • Successfully transcribed: {transcribed_count}")
print(f"  • Failed: {audio_count - transcribed_count}")
print(f"\n📄 Updated data saved to: {output_file}")
print(f"🎵 Audio files saved in: {audio_dir}/")

import json
import whisper
from pathlib import Path
import requests

# Test pe un singur fișier audio
print("Loading Whisper model...")
model = whisper.load_model("tiny")
print("✅ Model loaded!\n")

# Load JSON
with open('final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

audio_dir = Path('audio_files')

# Găsește primul răspuns audio
for user_id, results in data.get('examResults', {}).items():
    for result_id, result_data in results.items():
        if 'answers' in result_data:
            for question_id, answer in result_data['answers'].items():
                if 'audioUrl' in answer:
                    audio_url = answer['audioUrl']
                    
                    print(f"Testing transcription for:")
                    print(f"  User: {user_id}")
                    print(f"  Question: {question_id}")
                    print(f"  URL: {audio_url[:80]}...")
                    
                    # Download
                    audio_filename = f"{user_id}_{question_id}.webm"
                    audio_path = audio_dir / audio_filename
                    
                    print(f"\nDownloading to: {audio_path}")
                    try:
                        response = requests.get(audio_url, timeout=30)
                        response.raise_for_status()
                        with open(audio_path, 'wb') as f:
                            f.write(response.content)
                        print(f"✅ Downloaded ({len(response.content)} bytes)")
                    except Exception as e:
                        print(f"❌ Download failed: {e}")
                        exit(1)
                    
                    # Transcribe
                    print(f"\nTranscribing...")
                    try:
                        result = model.transcribe(str(audio_path), language="en", verbose=False)
                        transcription = result["text"].strip()
                        print(f"\n✅ Transcription successful!")
                        print(f"📝 Result: '{transcription}'")
                    except Exception as e:
                        print(f"❌ Transcription failed: {e}")
                        exit(1)
                    
                    print("\n🎉 Test complete! The script should work for all files.")
                    exit(0)

print("No audio answers found!")

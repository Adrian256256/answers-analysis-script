import json
import whisper
from pathlib import Path

print("=" * 70)
print("RE-TRANSCRIBING AUDIO FILES WITH MAXIMUM ACCURACY")
print("=" * 70)

# Load the existing transcriptions
print("\n📂 Loading existing data...")
with open('../data/final_with_transcriptions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load Whisper model
print("\n📥 Loading Whisper 'small' model (high accuracy)...")
print("   This will take longer but provide much better results")
print("   Model: 'small' (244M parameters - excellent for technical terms)\n")
try:
    model = whisper.load_model("small")
    print("✅ Small model loaded!\n")
except Exception as e:
    print(f"⚠️  Failed to load 'small' model: {e}")
    print("   Falling back to 'base' model...")
    model = whisper.load_model("base")
    print("✅ Base model loaded!\n")

audio_dir = Path('../data/audio_files')
total_audio = 0
retranscribed = 0
failed = 0

def transcribe_audio(audio_path, model):
    """Transcribe with maximum accuracy settings"""
    try:
        result = model.transcribe(
            str(audio_path),
            language="en",
            initial_prompt="Computer science exam. Technical terms: merge sort, heap sort, bubble sort, quick sort, insertion sort, binary search, linear search, polymorphism, inheritance, encapsulation, overloading, overriding, abstraction, polymorphism, interface, abstract, RAM, ROM, DRAM, SRAM, CPU, ALU, cache, control unit, LAN, WAN, MAN, VPN, network, router, switch, HTTP, HTTPS, FTP, TCP, UDP, IP, port, MAC, binary, algorithm, data structure, queue, stack, tree, graph, linked list, array, complexity, Big O notation, SQL, WHERE, SELECT, INSERT, DELETE, UPDATE, TRUNCATE, kernel, driver, compiler, interpreter, operating system, Dijkstra, Prim, Kruskal, greedy, dynamic programming, divide and conquer, recursion, iteration, round robin, FCFS, SJF, priority scheduling, IPv4, IPv6, MAC address, destructor, constructor, delete, new, malloc, free, Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, January, February, March, April, May, June, July, August, September, October, November, December.",
            verbose=False,
            temperature=0.0,  # Deterministic
            beam_size=5,  # Better beam search
            best_of=5,  # Consider multiple candidates
            fp16=False,  # Use FP32 for better accuracy
            condition_on_previous_text=True,  # Use context
            compression_ratio_threshold=2.4,  # Detect and skip repetitive transcriptions
            logprob_threshold=-1.0,  # More conservative confidence threshold
            no_speech_threshold=0.6,  # Better silence detection
            word_timestamps=False  # Focus on accuracy, not timing
        )
        return result["text"].strip()
    except Exception as e:
        print(f"      ❌ Failed: {e}")
        return None

print("=" * 70)
print("Re-transcribing audio files from examProgress...")
print("=" * 70)

for user_id, user_data in data.get('examProgress', {}).items():
    if not isinstance(user_data, dict) or 'answers' not in user_data:
        continue
    
    for question_id, answer in user_data['answers'].items():
        if 'audioUrl' not in answer:
            continue
        
        total_audio += 1
        audio_filename = f"{user_id}_{question_id}.webm"
        audio_path = audio_dir / audio_filename
        
        if not audio_path.exists():
            print(f"  ⚠️  {user_id[:15]}... / {question_id}: Audio file not found")
            failed += 1
            continue
        
        old_transcription = answer.get('transcription', '')
        print(f"\n  🎵 {user_id[:15]}... / {question_id}")
        print(f"     Old: '{old_transcription}'")
        
        new_transcription = transcribe_audio(audio_path, model)
        
        if new_transcription:
            answer['transcription'] = new_transcription
            print(f"     New: '{new_transcription}'")
            retranscribed += 1
            
            if old_transcription != new_transcription:
                print(f"     ✅ IMPROVED!")
            else:
                print(f"     ✓ Same")
        else:
            failed += 1

print("\n" + "=" * 70)
print("Re-transcribing audio files from examResults...")
print("=" * 70)

for user_id, results in data.get('examResults', {}).items():
    for result_id, result_data in results.items():
        if 'answers' not in result_data:
            continue
        
        for question_id, answer in result_data['answers'].items():
            if 'audioUrl' not in answer:
                continue
            
            total_audio += 1
            audio_filename = f"{user_id}_{question_id}.webm"
            audio_path = audio_dir / audio_filename
            
            if not audio_path.exists():
                print(f"  ⚠️  {user_id[:15]}... / {question_id}: Audio file not found")
                failed += 1
                continue
            
            old_transcription = answer.get('transcription', '')
            print(f"\n  🎵 {user_id[:15]}... / {question_id}")
            print(f"     Old: '{old_transcription}'")
            
            new_transcription = transcribe_audio(audio_path, model)
            
            if new_transcription:
                answer['transcription'] = new_transcription
                print(f"     New: '{new_transcription}'")
                retranscribed += 1
                
                if old_transcription != new_transcription:
                    print(f"     ✅ IMPROVED!")
                else:
                    print(f"     ✓ Same")
            else:
                failed += 1

# Save updated data
print("\n" + "=" * 70)
print("Saving improved transcriptions...")
with open('../data/final_with_transcriptions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 70)
print("🎉 RE-TRANSCRIPTION COMPLETE!")
print("=" * 70)
print(f"📊 Statistics:")
print(f"  - Total audio files: {total_audio}")
print(f"  - Successfully re-transcribed: {retranscribed}")
print(f"  - Failed: {failed}")
print(f"\n💾 Updated data saved to: ../data/final_with_transcriptions.json")
print(f"📝 Run 'cd scripts && python3 generate_csv.py' to update CSVs with new transcriptions")

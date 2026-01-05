# Exam Answers Analysis Script

This project analyzes user responses collected from the [Exametric app](https://exametric-clwq.vercel.app), processes audio transcriptions, and generates comprehensive statistics and visualizations.

## Overview

The Exametric app is a computer science knowledge assessment tool that collects both written and audio responses. This project processes the exported Firebase data, transcribes audio answers using AI, and creates a simplified, analysis-ready dataset.

## Project Structure

### Source Files

- **`exametric-439ba-default-rtdb-export _new.json`** - Raw Firebase Realtime Database export containing all user exam data
- **`examQuestions.ts`** - TypeScript file with exam questions, types, and correct answers

### Processing Scripts

- **`script.py`** - Initial data processing script that extracts and simplifies the raw JSON data into a structured format
- **`transcribe_audio.py`** - Audio transcription script using OpenAI's Whisper model (medium) to convert audio responses to text
- **`add_questions.py`** - Adds question texts and metadata from `examQuestions.ts` to the simplified dataset

### Output Files

- **`simplified_exam_data.json`** - Cleaned and structured exam data without transcriptions
- **`simplified_exam_data_with_transcriptions.json`** - Dataset with AI-transcribed audio answers
- **`simplified_exam_data_with_questions.json`** - **Final comprehensive dataset** with all data including question texts, transcriptions, and metadata
- **`graphs/`** - Directory containing generated visualizations and statistics

### Other Files

- **`.gitignore`** - Excludes source data, generated files, and audio downloads from version control
- **`audio_files/`** - Downloaded audio responses (created during transcription)

## Step-by-Step Process

### 1. Data Export
Export exam data from Firebase Realtime Database to JSON format.

### 2. Data Simplification
```bash
python script.py
```
Extracts and restructures the raw Firebase data into a clean format containing:
- User information (ID, email, submission status)
- Individual answers with timestamps
- Performance metrics (scores, time spent, tab changes)

### 3. Audio Transcription
```bash
python transcribe_audio.py
```
Downloads audio files and transcribes them using Whisper AI (medium model):
- Processes 57 audio responses
- Uses English language model with technical terms prompt
- Accurately transcribes computer science terminology
- Saves transcriptions directly in the dataset

### 4. Question Text Integration
```bash
python add_questions.py
```
Parses `examQuestions.ts` and adds to each answer:
- Full question text
- Question type (blank, audio, multiple)
- Audio question TTS text
- Expected correct answers

## Final Dataset Structure

The final JSON (`simplified_exam_data_with_questions.json`) contains:

```json
{
  "users": [
    {
      "user_id": "string",
      "email": "string",
      "submitted": boolean,
      "tab_changes": number,
      "total_score": number,
      "correct_answers_count": number,
      "time_spent_seconds": number,
      "answers": [
        {
          "question_id": "string",
          "question_text": "string",
          "question_type": "blank|audio|multiple",
          "question_tts_text": "string (for audio)",
          "user_answer": "string",
          "transcription": "string (for audio)",
          "expected_answers": ["string"],
          "correct": boolean,
          "time_to_answer_ms": number,
          "time_to_answer_seconds": number,
          "answered_at": "ISO timestamp",
          "audio_url": "string (for audio)"
        }
      ]
    }
  ],
  "summary": {
    "total_users": number,
    "submitted_users": number,
    "total_answers": number
  }
}
```

## Requirements

```bash
pip install openai-whisper matplotlib requests
```

- Python 3.x
- openai-whisper (for audio transcription)
- matplotlib (for visualizations)
- requests (for downloading audio files)

## Setup and Usage

### 1. Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install openai-whisper matplotlib requests
```

### 2. Prepare Data

Place your Firebase export file named `exametric-439ba-default-rtdb-export _new.json` in the project root.

### 3. Generate Datasets

Run the scripts in order:

```bash
# Step 1: Simplify the raw data
python script.py

# Step 2: Transcribe audio answers (takes ~10-15 minutes)
python transcribe_audio.py

# Step 3: Add question texts
python add_questions.py
```

**Note:** The generated JSON files (`simplified_*.json`) are excluded from Git via `.gitignore`. You need to generate them locally using the steps above.

### 4. Analyze Data

The final dataset `simplified_exam_data_with_questions.json` is now ready for analysis!

## Key Features

- Clean, structured data format
- AI-powered audio transcription with high accuracy
- Complete question texts and metadata
- Performance metrics (time, accuracy, engagement)
- Cheating detection indicators (tab changes)
- Ready for statistical analysis and visualization

## Data Source

Firebase Realtime Database export from the [Exametric application](https://exametric-clwq.vercel.app), a computer science assessment platform with written and audio-based questions.

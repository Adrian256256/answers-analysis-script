# Exam Answers Analysis Script

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
   - [Transcribing Audio Answers](#transcribing-audio-answers)
   - [Generating CSV Reports](#generating-csv-reports)
   - [Re-transcribing with Better Accuracy](#re-transcribing-with-better-accuracy)
6. [Output Files](#output-files)
   - [Individual User CSVs](#individual-user-csvs)
   - [Statistics CSV](#statistics-csv)
7. [CSV Column Descriptions](#csv-column-descriptions)
   - [Individual User CSV Columns](#individual-user-csv-columns)
   - [Statistics CSV - General Statistics](#statistics-csv---general-statistics)
   - [Statistics CSV - Individual User Data](#statistics-csv---individual-user-data)
8. [Time Format](#time-format)
9. [Data Source](#data-source)
10. [Viewing CSV Files on GitHub](#viewing-csv-files-on-github)
11. [Notes](#notes)

---

## Overview

This project analyzes exam response data exported from Firebase. It processes JSON data containing user answers (both text and audio), generates comprehensive CSV reports, and transcribes audio responses using OpenAI's Whisper model.

The analysis focuses on:
- Individual user performance and behavior
- Answer patterns (text vs audio responses)
- Time spent on questions and overall exam
- Tab change tracking (potential indicators of multitasking or cheating)
- Audio transcription for qualitative analysis

---

## Project Structure

```
answers-analysis-script/
├── final.json                          # Source data (Firebase export)
├── final_with_transcriptions.json      # Data with audio transcriptions
├── examQuestions.ts                    # Question definitions and text
├── questions_map.json                  # Parsed question text mapping
├── generate_csv.py                     # Main script: generates CSV reports
├── transcribe_audio.py                 # Script: transcribes audio answers
├── retranscribe_audio.py              # Script: re-transcribe with better accuracy
├── parse_questions.py                  # Script: extracts questions from TypeScript
├── audio_files/                        # Directory: downloaded audio files (74 files)
├── user_csvs/                          # Directory: individual user folders
│   ├── <user_id_1>/
│   │   ├── summary.csv                 # User statistics and metadata
│   │   └── answers.csv                 # Detailed answer information
│   ├── <user_id_2>/
│   │   ├── summary.csv
│   │   └── answers.csv
│   └── ...                             # 16 user folders total
└── statistics_all_users.csv            # Aggregated statistics for all users
```

---

## Requirements

- Python 3.8+
- OpenAI Whisper (for audio transcription)
- Python packages:
  - `json` (built-in)
  - `csv` (built-in)
  - `datetime` (built-in)
  - `collections` (built-in)
  - `requests`
  - `whisper` (openai-whisper)

---

## Setup and Installation

1. **Install Python dependencies:**
   ```bash
   pip install openai-whisper requests
   ```

2. **Place your data file:**
   - Ensure `final.json` (Firebase export) is in the project root

3. **Parse question definitions:**
   ```bash
   python3 parse_questions.py
   ```
   This creates `questions_map.json` with question text extracted from `examQuestions.ts`.

---

## Usage

### Transcribing Audio Answers

First-time transcription of all audio responses:

```bash
python3 transcribe_audio.py
```

This will:
- Download audio files from Firebase Storage to `audio_files/`
- Transcribe each audio response using Whisper
- Save results to `final_with_transcriptions.json`

**Note:** Initial transcription uses the "base" Whisper model and takes approximately 2-3 minutes for 74 audio files.

### Generating CSV Reports

Generate all CSV reports from the transcribed data:

```bash
python3 generate_csv.py
```

This creates:
- 16 individual user CSV files in `user_csvs/`
- 1 comprehensive statistics file: `statistics_all_users.csv`

### Re-transcribing with Better Accuracy

If transcription accuracy is insufficient, re-transcribe with improved settings:

```bash
python3 retranscribe_audio.py
```

This uses optimized Whisper parameters:
- Better model selection (base vs tiny)
- Enhanced prompt with technical terms
- Anti-repetition settings
- Improved silence detection

After re-transcription, regenerate CSVs:
```bash
python3 generate_csv.py
```

---

## Output Files

### Individual User CSVs

**Location:** `user_csvs/<user_id>/`

Each user has a dedicated folder containing two CSV files:

#### 1. `summary.csv` - User Metadata

Contains key statistics and metadata in a key-value format:
- Email address
- Submission timestamp
- Answer counts
- Time spent
- Tab change count
- Current section (for in-progress users)

**This file is optimized for GitHub viewing** - displays as a clean table when viewed on GitHub.

#### 2. `answers.csv` - Detailed Answer Breakdown

Contains a table with all questions answered by the user:
- Question ID and text
- User responses (text or audio transcription)
- Timing information
- Audio URLs (for audio responses)

**This file is also optimized for GitHub viewing** - GitHub automatically renders CSV files as tables.

**Example:** 
- `user_csvs/hXKCWwzPgWQ17gIEU9nKwtLaZx73/summary.csv`
- `user_csvs/hXKCWwzPgWQ17gIEU9nKwtLaZx73/answers.csv`

### Statistics CSV

**Location:** `statistics_all_users.csv`

Contains two sections:

1. **General Statistics**: Aggregated metrics across all users
2. **Individual User Data**: One row per user with key metrics

---

## CSV Column Descriptions

### Individual User CSV Columns

#### Summary CSV (Key-Value Format)

| Metric | Description | Example |
|--------|-------------|---------|
| `Email` | User's email address | user205520@exam.org |
| `Submission Time (Date/Time)` | Timestamp of exam submission | 2025-12-18 15:36:43 |
| `Answered Count (Total)` | Total number of questions answered | 25 |
| `Total Questions (Count)` | Total questions in exam | 25 |
| `Time Spent (mm:ss)` | Total time spent on exam | 9:21 |
| `Start Time (Date/Time)` | Timestamp when exam started | 2025-12-18 15:27:22 |
| `Current Section` | Current section (for incomplete exams) | section3_standard |
| `Current Question Index` | Index of current question | 15 |
| `Tab Change Count (Total)` | Number of times user switched tabs | 4 |

#### Answers CSV (Table Format)

| Column | Description | Example |
|--------|-------------|---------|
| `Question ID` | Unique identifier for the question | section1_accomodation_Q3 |
| `Question Text` | Full text of the question | "What day is it today?" |
| `Answer Type` | Type of response | Text or Audio |
| `User Answer (Text)` | Text response (for text questions) | "22" |
| `Audio URL` | Firebase Storage URL (for audio responses) | https://firebasestorage.googleapis.com/... |
| `Transcription (Audio Answers)` | Whisper transcription of audio response | "Today is Thursday." |
| `Time to Answer (mm:ss)` | Time taken to answer this question | 0:42 |
| `Answered At (Timestamp)` | ISO timestamp when answered | 2025-12-18T15:28:11.971Z |
| `Question Displayed At (Timestamp)` | ISO timestamp when question was shown | 2025-12-18T15:27:29.647Z |
| `Audio Question Duration (mm:ss)` | Duration of audio question playback | 0:01 |

---

### Statistics CSV - General Statistics

Aggregated metrics across all 16 users:

| Metric | Description | Example Value |
|--------|-------------|---------------|
| `Total Users (Count)` | Total number of users in dataset | 16 |
| `Total Answers (Count)` | Total answers across all users | 242 |
| `Total Text Answers (Count)` | Number of text-based answers | 168 |
| `Total Audio Answers (Count)` | Number of audio-based answers | 74 |
| `Text vs Audio Ratio` | Ratio of text to audio answers | 2.27:1 |
| `Average Time to Answer - Overall (mm:ss)` | Mean time across all answers | 0:24 |
| `Average Time to Answer - Text (mm:ss)` | Mean time for text answers | 0:17 |
| `Average Time to Answer - Audio (mm:ss)` | Mean time for audio answers | 0:39 |
| `Audio takes longer than Text by (mm:ss)` | Time difference between audio and text | 0:22 |
| `Audio/Text Time Ratio` | Ratio of audio to text answer times | 2.29 |
| `Average Tab Changes per User (Count)` | Mean tab changes per user | 3.0 |
| `Max Tab Changes (Count)` | Maximum tab changes by any user | 14 |
| `Min Tab Changes (Count)` | Minimum tab changes | 0 |
| `Users with 0 Tab Changes (Count)` | Users who never switched tabs | 9 |
| `Users with Tab Changes (Count)` | Users who switched tabs at least once | 6 |
| `Total Answered Questions (Count)` | Total questions answered across all users | 228 |
| `Total Time Spent by All Users (mm:ss)` | Cumulative time spent | 122:43 |
| `Average Time Spent per User (mm:ss)` | Mean time spent per user | 10:13 |

---

### Statistics CSV - Individual User Data

One row per user with key performance metrics:

| Column | Description | Example |
|--------|-------------|---------|
| `User ID` | Unique Firebase user identifier | 1KznrIROVcQisRpGQw0kRF79lEW2 |
| `Email` | User's email address | user228962@exam.org |
| `Total Answers (Count)` | Number of questions answered by user | 18 |
| `Text Answers (Count)` | Number of text responses | 11 |
| `Audio Answers (Count)` | Number of audio responses | 7 |
| `Average Time to Answer (mm:ss)` | Mean time per question for this user | 0:24 |
| `Tab Changes (Count)` | Number of tab switches | 0 |
| `Time Spent (mm:ss)` | Total time spent on exam | 8:46 |
| `Current Section` | Last active section (N/A if completed) | N/A |
| `Submission Time (Date/Time)` | Completion timestamp (N/A if incomplete) | 2026-01-04 15:03:20 |

---

## Time Format

All time values are formatted as **mm:ss** (minutes:seconds):
- `0:03` = 3 seconds
- `0:42` = 42 seconds
- `8:46` = 8 minutes 46 seconds
- `122:43` = 122 minutes 43 seconds (2 hours 2 minutes 43 seconds)

**Source conversions:**
- Milliseconds converted to mm:ss for `timeToAnswerMs`, `audioQuestionDurationMs`
- Seconds converted to mm:ss for `timeSpent`
- ISO timestamps preserved for `answeredAt`, `questionDisplayedAt`, `timestamp`

---

## Data Source

### Firebase Export Structure

The project uses two JSON files:

**1. `final.json`** - Original Firebase export without transcriptions
- Contains raw exam data with audio URLs
- Audio responses have `audioUrl` field but no `transcription` field
- This is your initial data source

**2. `final_with_transcriptions.json`** - Enhanced version with audio transcriptions
- Same structure as `final.json` but with added transcriptions
- Created by running `transcribe_audio.py` or `retranscribe_audio.py`
- Each audio answer includes a `transcription` field with the Whisper-generated text
- File size is slightly larger (~134KB vs 130KB) due to transcription text

**Key Difference:**
```json
// final.json (before transcription)
"answer": {
  "audioUrl": "https://firebasestorage.googleapis.com/...",
  "timeToAnswerMs": 42000
}

// final_with_transcriptions.json (after transcription)
"answer": {
  "audioUrl": "https://firebasestorage.googleapis.com/...",
  "timeToAnswerMs": 42000,
  "transcription": "Today is Thursday."
}
```

**Script Behavior:**
- `generate_csv.py` automatically uses `final_with_transcriptions.json` if it exists
- If `final_with_transcriptions.json` is not found, it falls back to `final.json`
- Transcriptions appear as "Not transcribed yet" in CSVs when using `final.json`

---

### JSON Structure

The project processes JSON files with the following structure:

```json
{
  "examProgress": {
    "userId": {
      "answers": { "questionId": {...} },
      "currentSection": "section3_standard",
      "startTimestamp": 1234567890000,
      "tabChangeCount": 4,
      ...
    }
  },
  "examResults": {
    "userId": {
      "resultId": {
        "answers": { "questionId": {...} },
        "answeredCount": 25,
        "timestamp": "2025-12-18T15:36:43.123Z",
        "timeSpent": 561,
        ...
      }
    }
  },
  "users": {
    "userId": {
      "email": "user@example.com",
      "name": "User Name",
      "role": "student"
    }
  }
}
```

### Question Types

1. **Text Questions**: Short answer, multiple choice
2. **Audio Questions**: Voice-recorded responses transcribed via Whisper

### Sections

- `section1_accomodation`: Accommodation questions (demographics, preferences)
- `section2_standard`: Written technical questions (standard version)
- `section2_control`: Written technical questions (control version)
- `section3_standard`: Audio technical questions (standard version)
- `section3_control`: Audio technical questions (control version)

---

## Viewing CSV Files on GitHub

All CSV files are optimized for viewing directly on GitHub:

### Individual User Data

1. Navigate to `user_csvs/` directory
2. Click on any user ID folder (e.g., `hXKCWwzPgWQ17gIEU9nKwtLaZx73`)
3. Click on either file:
   - `summary.csv` - Clean key-value table with user statistics
   - `answers.csv` - Detailed answer breakdown in table format

**GitHub automatically renders CSV files as formatted tables** - no need to download!

### Statistics Data

Click on `statistics_all_users.csv` in the root directory to view:
- Aggregated metrics across all users
- Individual user comparison table

### Benefits of this Structure

✅ **Easy navigation** - Each user has a dedicated folder  
✅ **GitHub-friendly** - CSV files render as tables automatically  
✅ **Organized** - Separate files for summary vs detailed data  
✅ **Shareable** - Direct links to specific user data  
✅ **Clean commits** - Changes to one user don't affect others

---

## Notes

1. **Transcription Quality**: 
   - Initial transcriptions use Whisper "base" model
   - Re-transcription available with optimized parameters for technical terms
   - Some audio responses may contain background noise or unclear speech

2. **Tab Changes**: 
   - Tracked as potential indicator of multitasking or academic integrity issues
   - 56% of users (9/16) never switched tabs
   - Maximum observed: 14 tab changes

3. **Time Calculations**:
   - `Time to Answer` = `Answered At` - `Question Displayed At`
   - Negative times possible if system clock adjustments occurred

4. **Missing Data**:
   - Some users have incomplete exams (4/16 in progress)
   - N/A values indicate missing or inapplicable data

5. **Audio Files**:
   - Downloaded to `audio_files/` directory
   - Format: WebM (VP8/Opus)
   - Naming convention: `{userId}_{questionId}.webm`

6. **Privacy**: 
   - User IDs are Firebase-generated unique identifiers
   - Emails included for identification purposes
   - Consider anonymization for sharing data

---

## License

This project is for internal analysis purposes. Ensure compliance with data protection regulations (GDPR, etc.) when handling user data.

# Exam Answers Analysis Script

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
   - [Quick Start (Using Helper Script)](#quick-start-using-helper-script)
   - [Manual Usage](#manual-usage)
   - [Transcribing Audio Answers](#transcribing-audio-answers)
   - [Generating CSV Reports](#generating-csv-reports)
   - [Re-transcribing with Better Accuracy](#re-transcribing-with-better-accuracy)
6. [Manual Verification and Correction](#manual-verification-and-correction)
   - [Workflow for Manual Grading](#workflow-for-manual-grading)
7. [Output Files](#output-files)
   - [Individual User CSVs](#individual-user-csvs)
   - [General Statistics CSVs](#general-statistics-csvs)
8. [CSV Column Descriptions](#csv-column-descriptions)
   - [Individual User CSV Columns](#individual-user-csv-columns)
   - [General Statistics CSVs](#general-statistics-csvs-1)
9. [Time Format](#time-format)
10. [Data Source](#data-source)
11. [Viewing CSV Files on GitHub](#viewing-csv-files-on-github)
12. [Notes](#notes)

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
├── scripts/                            # All Python scripts
│   ├── generate_csv.py                 # Main script: generates CSV reports
│   ├── transcribe_audio.py             # Script: transcribes audio answers
│   ├── retranscribe_audio.py          # Script: re-transcribe with better accuracy
│   └── parse_questions.py              # Script: extracts questions from TypeScript
├── data/                               # All data files and audio
│   ├── final.json                      # Source data (Firebase export)
│   ├── final_with_transcriptions.json  # Data with audio transcriptions
│   ├── examQuestions.ts                # Question definitions and text
│   ├── questions_map.json              # Parsed question text mapping
│   ├── audio_files/                    # Downloaded audio files (103 files)
│   ├── retranscribe.log                # Logs from re-transcription
│   └── retranscribe_final.log          # Final re-transcription logs
├── output/                             # All generated CSV files (auto-generated)
│   ├── user_csvs/                      # Individual user folders (20 users)
│   │   ├── <user_id_1>/
│   │   │   ├── summary.csv             # User statistics and metadata
│   │   │   └── answers.csv             # Detailed answer information
│   │   ├── <user_id_2>/
│   │   │   ├── summary.csv
│   │   │   └── answers.csv
│   │   └── ...
│   └── general_statistics/             # Aggregated statistics
│       ├── summary.csv                 # Overall metrics and averages
│       └── users.csv                   # Comparison table of all users
├── manual_corrected_csvs/              # Manual corrections folder (user-created)
│   ├── user_csvs/                      # Copy of user CSVs for manual grading
│   │   └── ...                         # Corrected transcriptions & grading
│   └── general_statistics/             # Copy of statistics with manual counts
│       ├── summary.csv                 # Updated with manual grading
│       └── users.csv                   # Updated with correct/wrong counts
├── .venv/                              # Python virtual environment
├── .gitignore
├── run.sh                              # Helper script for easy execution
└── README.md
```

**Note:** The `manual_corrected_csvs/` folder should be created manually by copying the `output/` folder after generation. This folder is where you perform manual verification and corrections.

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
   - Ensure `final.json` (Firebase export) is in the `data/` folder
   - Ensure `examQuestions.ts` is in the `data/` folder

3. **Parse question definitions:**
   ```bash
   cd scripts
   python3 parse_questions.py
   ```
   This creates `questions_map.json` with question text extracted from `examQuestions.ts`.

---

## Usage

### Quick Start (Using Helper Script)

For convenience, you can use the interactive helper script:

```bash
./run.sh
```

This will present a menu with options to:
1. Parse questions from examQuestions.ts
2. Transcribe audio files
3. Generate CSV reports
4. Re-transcribe audio with better accuracy
5. Run full pipeline (transcribe + generate CSVs)

### Manual Usage

#### Transcribing Audio Answers

First-time transcription of all audio responses:

```bash
cd scripts
python3 transcribe_audio.py
```

This will:
- Download audio files from Firebase Storage to `data/audio_files/`
- Transcribe each audio response using Whisper
- Save results to `data/final_with_transcriptions.json`

**Note:** Initial transcription uses the "base" Whisper model and takes approximately 2-3 minutes for all audio files.

### Generating CSV Reports

Generate all CSV reports from the transcribed data:

```bash
cd scripts
python3 generate_csv.py
```

This creates:
- Individual user CSV files in `output/user_csvs/<user_id>/`
- General statistics in `output/general_statistics/`

### Re-transcribing with Better Accuracy

If transcription accuracy is insufficient, re-transcribe with improved settings:

```bash
cd scripts
python3 retranscribe_audio.py
```

This uses optimized Whisper parameters:
- Better model selection (base vs tiny)
- Enhanced prompt with technical terms
- Anti-repetition settings
- Improved silence detection

After re-transcription, regenerate CSVs:
```bash
cd scripts
python3 generate_csv.py
```

---

## Manual Verification and Correction

### Workflow for Manual Grading

After generating the CSV files, you should perform manual verification:

1. **Create a copy for manual corrections:**
   - Copy the entire `output/` folder to `manual_corrected_csvs/`
   - This preserves the original generated files

2. **Review and correct transcriptions:**
   - Open each user's `answers.csv` in the `manual_corrected_csvs/` folder
   - Check the **Transcription (Audio Answers)** column
   - Correct any incorrect transcriptions directly in the CSV
   - Common issues to look for:
     - Technical terms misheard by Whisper
     - Similar-sounding words (e.g., "Queue" vs "Cue")
     - Repetitive transcriptions that indicate audio quality issues

3. **Mark correct/wrong answers:**
   - For each answer, fill in either the **Correct** or **Wrong** column
   - Use consistent markers (e.g., "✓", "1", "Yes" for correct; "✗", "1", "Yes" for wrong)
   - Leave both empty if you cannot determine correctness

4. **Update summary statistics:**
   - In each user's `summary.csv`, fill in:
     - **Correct Answers (Count)** - total number of correct answers
     - **Wrong Answers (Count)** - total number of wrong answers
   - Update the `general_statistics/users.csv` with the same counts

**Important:** Always work in the `manual_corrected_csvs/` folder to keep the original generated files intact. This allows you to regenerate if needed without losing manual corrections.

---

## Output Files

### Individual User CSVs

**Location:** `output/user_csvs/<user_id>/`

Each user has a dedicated folder containing two CSV files:

#### 1. `summary.csv` - User Metadata

Contains key statistics and metadata in a key-value format:
- Email address
- Submission timestamp
- Answer counts (Total, Unanswered)
- Correct/Wrong answers (empty for manual verification)
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
- Correct/Wrong columns (empty for manual verification)

**This file is also optimized for GitHub viewing** - GitHub automatically renders CSV files as tables.

**Example:** 
- `output/user_csvs/hXKCWwzPgWQ17gIEU9nKwtLaZx73/summary.csv`
- `output/user_csvs/hXKCWwzPgWQ17gIEU9nKwtLaZx73/answers.csv`

### General Statistics CSVs

**Location:** `output/general_statistics/`

Contains two CSV files with aggregated statistics:

#### 1. `summary.csv` - Overall Metrics

Contains aggregated metrics across all users in a key-value format:
- Total users (submitted vs in-progress)
- Answer statistics (total, text, audio, ratios)
- Average time to answer (overall, text, audio)
- Tab change statistics
- Time spent statistics

**Optimized for GitHub viewing** - displays as a clean summary table.

#### 2. `users.csv` - User Comparison Table

Contains a table comparing all users side-by-side:
- User ID and email
- Status (Submitted/In Progress)
- Total questions and answered count
- Unanswered count (calculated automatically)
- Correct/Wrong counts (empty for manual verification)
- Answer counts by type (text/audio)
- Average response times
- Tab changes
- Time spent
- Current section
- Submission timestamp

**Perfect for GitHub viewing** - compare all users in one table.

**Example:** 
- `general_statistics/summary.csv`
- `general_statistics/users.csv`

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
| `Unanswered Questions (Count)` | Questions not answered (auto-calculated) | 0 |
| `Correct Answers (Count)` | Correct answers (empty for manual entry) | *[to be filled]* |
| `Wrong Answers (Count)` | Wrong answers (empty for manual entry) | *[to be filled]* |
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
| `Correct` | Manual verification field for correct answers | *[to be filled]* |
| `Wrong` | Manual verification field for wrong answers | *[to be filled]* |

---

### General Statistics CSVs

#### Summary CSV (Key-Value Format)

Aggregated metrics across all 19 users:

| Metric | Description | Example Value |
|--------|-------------|---------------|
| `Total Users (Count)` | Total number of users in dataset | 19 |
| `Submitted Users (Count)` | Users who completed the exam | 15 |
| `In Progress Users (Count)` | Users still taking the exam | 4 |
| `Total Answers (Count)` | Total answers across all users | 304 |
| `Total Text Answers (Count)` | Number of text-based answers | 208 |
| `Total Audio Answers (Count)` | Number of audio-based answers | 96 |
| `Text vs Audio Ratio` | Ratio of text to audio answers | 2.17:1 |
| `Average Time to Answer - Overall (mm:ss)` | Mean time across all answers | 0:22 |
| `Average Time to Answer - Text (mm:ss)` | Mean time for text answers | 0:15 |
| `Average Time to Answer - Audio (mm:ss)` | Mean time for audio answers | 0:35 |
| `Audio takes longer than Text by (mm:ss)` | Time difference between audio and text | 0:19 |
| `Audio/Text Time Ratio` | Ratio of audio to text answer times | 2.24 |
| `Average Tab Changes per User (Count)` | Mean tab changes per user | 3.17 |
| `Max Tab Changes (Count)` | Maximum tab changes by any user | 14 |
| `Min Tab Changes (Count)` | Minimum tab changes | 0 |
| `Users with 0 Tab Changes (Count)` | Users who never switched tabs | 10 |
| `Users with Tab Changes (Count)` | Users who switched tabs at least once | 8 |
| `Total Answered Questions (Count)` | Total questions answered across all users | 290 |
| `Total Time Spent by All Users (mm:ss)` | Cumulative time spent | 143:22 |
| `Average Time Spent per User (mm:ss)` | Mean time spent per user | 9:33 |

#### Users CSV (Table Format)

| Column | Description | Example |
|--------|-------------|---------|
| `User ID` | Firebase user identifier | hXKCWwzPgWQ17gIEU9nKwtLaZx73 |
| `Email` | User's email address | user205520@exam.org |
| `Status` | Exam completion status | Submitted or In Progress |
| `Total Answers (Count)` | Total questions answered | 25 |
| `Text Answers (Count)` | Number of text answers | 14 |
| `Audio Answers (Count)` | Number of audio answers | 11 |
| `Average Time to Answer (mm:ss)` | Mean time per answer | 0:22 |
| `Tab Changes (Count)` | Times user switched tabs | 4 |
| `Time Spent (mm:ss)` | Total time spent on exam | 9:21 |
| `Current Section` | Current section (if in progress) | section3_standard |
| `Submission Time (Date/Time)` | Timestamp of submission | 2025-12-18 15:36:43 |

---

## Time Format

All time values are formatted as **mm:ss** (minutes:seconds):
- `0:03` = 3 seconds
- `0:42` = 42 seconds
- `8:46` = 8 minutes 46 seconds
- `143:22` = 143 minutes 22 seconds (2 hours 23 minutes 22 seconds)

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

### General Statistics Data

1. Navigate to `general_statistics/` directory
2. Click on either file:
   - `summary.csv` - Aggregated metrics across all users
   - `users.csv` - Comparison table of all users side-by-side

---

## Notes

1. **Transcription Quality**: 
   - Initial transcriptions use Whisper "base" model
   - Re-transcription available with optimized parameters for technical terms
   - Some audio responses may contain background noise or unclear speech

2. **Tab Changes**: 
   - Tracked as potential indicator of multitasking or academic integrity issues
   - 53% of users (10/19) never switched tabs
   - Maximum observed: 14 tab changes

3. **Time Calculations**:
   - `Time to Answer` = `Answered At` - `Question Displayed At`
   - Negative times possible if system clock adjustments occurred

4. **Missing Data**:
   - Some users have incomplete exams (4/19 in progress)
   - N/A values indicate missing or inapplicable data

5. **Audio Files**:
   - Downloaded to `audio_files/` directory (96 files)
   - Format: WebM (VP8/Opus)
   - Naming convention: `{userId}_{questionId}.webm`

6. **Privacy**: 
   - User IDs are Firebase-generated unique identifiers
   - Emails included for identification purposes
   - Consider anonymization for sharing data

---

## License

This project is for internal analysis purposes. Ensure compliance with data protection regulations (GDPR, etc.) when handling user data.

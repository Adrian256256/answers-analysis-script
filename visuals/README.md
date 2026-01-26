# Statistics Visualizations - Exam Analysis

This folder contains graphic visualizations automatically generated from exam data.

## Generated Charts

### 1. `1_overall_accuracy.png`
**Answer Distribution - Overall Total**
- Bar chart showing the total number of correct vs incorrect answers
- Displays percentages for each category
- Colors: Green (correct), Red (incorrect)

### 2. `2_text_vs_audio.png`
**Comparison: Text vs Audio Answers**
- Two side-by-side charts:
  - Left: Comparison of answer counts (correct/incorrect) for Text vs Audio
  - Right: Accuracy percentage comparison between Text and Audio
- Highlights the performance difference between the two answer types

### 3. `3_user_performance.png`
**Top 15 Users - Individual Performance**
- Horizontal bar chart showing each user's accuracy
- Sorted in descending order by accuracy
- Color coding:
  - Green: ≥80% (Pass)
  - Orange: 60-79% (Satisfactory)
  - Red: <60% (Unsatisfactory)
- Displays score (correct/total) for each user

### 4. `4_accuracy_distribution.png`
**User Accuracy Distribution**
- Histogram showing how many users fall within each accuracy range
- Ranges: 0-40%, 40-50%, 50-60%, 60-70%, 70-80%, 80-90%, 90-100%
- Displays mean and median accuracy
- Color gradient from red (low) to dark green (high)

### 5. `5_pie_charts.png`
**Pie Charts - Distributions**
- Two pie charts:
  - Left: Correct vs Incorrect distribution (overall total)
  - Right: Text vs Audio distribution (answer types)
- Each segment displays count and percentage

### 6. `6_summary_table.png`
**Summary Table - General Statistics**
- Table with detailed statistics:
  - OVERALL row: general totals
  - Text row: statistics for text answers
  - Audio row: statistics for audio answers
- Columns: Correct, Incorrect, Total, Accuracy (%)

## Detailed Text vs Audio Analysis

### 7. `7_total_correct_comparison.png`
**How Many Answers Were Correct? Text vs Audio**
- Simple side-by-side bar comparison
- Green bars: Correct answers
- Red bars: Incorrect answers
- Large numbers show the actual count
- Clear labels showing totals for each type
- Easy to understand which question type had more correct answers

### 8. `8_accuracy_percentage_comparison.png`
**Which Type of Questions Was Easier? Accuracy Comparison**
- Large percentage display for each question type
- Shows accuracy rate as a percentage (0-100%)
- Reference lines at 60% (Satisfactory) and 80% (Pass)
- Yellow box highlights the performance difference
- Bottom summary shows the raw numbers (correct out of total)
- Clear answer to: "Were text or audio questions easier?"

### 9. `9_user_preference_analysis.png`
**Do Students Perform Better on Text or Audio Questions?**
- Counts how many users did better on each type
- Three categories:
  - Better at Text Questions
  - Better at Audio Questions
  - Equal Performance (difference < 2%)
- Shows both user count and percentage
- Helps understand student preferences
- Simple bar chart with clear labels

### 10. `10_numbers_breakdown.png`
**The Numbers Behind Performance: Complete Breakdown**
- Clear table showing all the numbers
- Rows: Total questions, Correct answers, Incorrect answers, Accuracy rate
- Columns: Text questions, Audio questions, Difference
- Large, readable fonts
- Highlighted accuracy row (most important metric)
- Interpretation box at bottom explaining what the numbers mean
- Perfect for understanding the complete picture

## Regeneration

To regenerate all visualizations with updated data:

```bash
cd /Users/adrian/Documents/Facultate/MPS/answers-analysis-script
.venv/bin/python scripts/generate_visuals.py
```

## Notes

- All charts are saved in PNG format with high resolution (300 DPI)
- Visualizations are automatically generated from CSV files in `manual_corrected_csvs/user_csvs/`
- The script that generates these visualizations is located at `scripts/generate_visuals.py`
- **Total visualizations: 10** (6 general + 4 detailed text vs audio analysis)

## Current Statistics

**Last generated:** January 26, 2026

- **Total users evaluated:** 17
- **Total answers evaluated:** 246
- **Overall accuracy:** 78.86%
- **Text accuracy:** 80.52%
- **Audio accuracy:** 76.09%
- **Text vs Audio performance difference:** +4.43%

## Chart Categories

### General Statistics (Charts 1-6)
Charts 1-6 provide overall exam statistics including:
- **Chart 1**: Total correct vs incorrect answers
- **Chart 2**: Basic text vs audio comparison
- **Chart 3**: Top performing users
- **Chart 4**: How accuracy is distributed among users
- **Chart 5**: Pie charts showing distributions
- **Chart 6**: Summary table with key numbers

### Detailed Text vs Audio Analysis (Charts 7-10)
Charts 7-10 focus specifically on comparing text questions versus audio questions:
- **Chart 7**: Raw numbers - how many correct answers for each type
- **Chart 8**: Accuracy percentages - which type was easier
- **Chart 9**: User preferences - who prefers which type
- **Chart 10**: Complete breakdown - all the numbers in one table

**Key Questions Answered:**
1. Are text questions easier than audio questions?
2. How many more/fewer correct answers were there?
3. Do most students prefer one type over another?
4. What's the exact performance difference?

All charts use:
- **Large, clear fonts** for easy reading
- **Simple layouts** - one main idea per chart
- **Explanatory text** built into the visualization
- **Color coding**: Green = correct/good, Red = incorrect/poor, Blue = text, Orange = audio

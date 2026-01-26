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

## Current Statistics

**Last generated:** January 26, 2026

- **Total users evaluated:** 17
- **Total answers evaluated:** 246
- **Overall accuracy:** 78.86%
- **Text accuracy:** 80.52%
- **Audio accuracy:** 76.09%
- **Text vs Audio performance difference:** +4.43%

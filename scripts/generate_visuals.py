#!/usr/bin/env python3
"""
Generate visual statistics from general_statistics/summary.csv
Creates clear and simple visualizations for exam analysis.
"""

import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Paths
BASE_DIR = Path(__file__).parent.parent
SUMMARY_FILE = BASE_DIR / 'manual_corrected_csvs' / 'general_statistics' / 'summary.csv'
USERS_FILE = BASE_DIR / 'manual_corrected_csvs' / 'general_statistics' / 'users.csv'
USER_CSVS_DIR = BASE_DIR / 'manual_corrected_csvs' / 'user_csvs'
VISUALS_DIR = BASE_DIR / 'visuals'
VISUALS_DIR.mkdir(exist_ok=True)

# Colors
COLOR_CORRECT = '#4CAF50'  # Green
COLOR_WRONG = '#F44336'    # Red
COLOR_TEXT = '#2196F3'     # Blue
COLOR_AUDIO = '#FF9800'    # Orange
COLOR_PARTIAL = '#FFC107'  # Yellow


def load_summary_data():
    """Load data from summary.csv into a dictionary."""
    data = {}
    
    with open(SUMMARY_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            metric = row['Metric']
            value = row['Value']
            data[metric] = value
    
    return data


def parse_number(value):
    """Parse a number from a string, handling percentages and counts."""
    if isinstance(value, (int, float)):
        return value
    
    value = str(value).strip()
    
    # Remove percentage sign
    if '%' in value:
        value = value.replace('%', '')
    
    # Remove commas
    value = value.replace(',', '')
    
    # Try to convert to float
    try:
        return float(value)
    except:
        return 0


def load_user_pair_data():
    """Load pair statistics from each user's summary.csv."""
    users_pairs = []
    
    for user_dir in sorted(USER_CSVS_DIR.glob('*')):
        if not user_dir.is_dir():
            continue
        
        summary_file = user_dir / 'summary.csv'
        if not summary_file.exists():
            continue
        
        user_id = user_dir.name
        correct_pairs = 0
        wrong_pairs = 0
        partial_pairs = 0
        
        with open(summary_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                metric = row.get('Metric', '')
                value = row.get('Value', '0')
                
                if metric == 'Correct Pairs (Both Correct)':
                    correct_pairs = int(value) if value.isdigit() else 0
                elif metric == 'Wrong Pairs (Both Wrong)':
                    wrong_pairs = int(value) if value.isdigit() else 0
                elif metric == 'Partial Pairs (One Correct)':
                    partial_pairs = int(value) if value.isdigit() else 0
        
        # Only include users with at least some graded pairs
        if correct_pairs + wrong_pairs + partial_pairs > 0:
            users_pairs.append({
                'user_id': user_id,
                'correct_pairs': correct_pairs,
                'wrong_pairs': wrong_pairs,
                'partial_pairs': partial_pairs,
                'total_pairs': correct_pairs + wrong_pairs + partial_pairs
            })
    
    return users_pairs


def calculate_standard_vs_control_accuracy():
    """Calculate separate accuracy metrics for standard and control questions."""
    total_correct = 0
    total_wrong = 0
    standard_correct = 0
    standard_wrong = 0
    control_correct = 0
    control_wrong = 0
    
    for user_dir in sorted(USER_CSVS_DIR.glob('*')):
        if not user_dir.is_dir():
            continue
        
        answers_file = user_dir / 'answers.csv'
        if not answers_file.exists():
            continue
        
        with open(answers_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                question_id = row.get('Question ID', '')
                
                # Skip accommodation questions
                if 'accomodation' in question_id:
                    continue
                
                is_correct = 'x' in row.get('Correct', '').lower()
                is_wrong = 'x' in row.get('Wrong', '').lower()
                
                # Count totals
                if is_correct:
                    total_correct += 1
                if is_wrong:
                    total_wrong += 1
                
                # Separate standard and control
                if '_standard_' in question_id:
                    if is_correct:
                        standard_correct += 1
                    if is_wrong:
                        standard_wrong += 1
                elif '_control_' in question_id:
                    if is_correct:
                        control_correct += 1
                    if is_wrong:
                        control_wrong += 1
    
    # Calculate accuracies
    overall_accuracy = (total_correct / (total_correct + total_wrong) * 100) if (total_correct + total_wrong) > 0 else 0
    core_accuracy = (standard_correct / (standard_correct + standard_wrong) * 100) if (standard_correct + standard_wrong) > 0 else 0
    control_accuracy = (control_correct / (control_correct + control_wrong) * 100) if (control_correct + control_wrong) > 0 else 0
    
    return {
        'overall_accuracy': overall_accuracy,
        'overall_correct': total_correct,
        'overall_wrong': total_wrong,
        'core_accuracy': core_accuracy,
        'core_correct': standard_correct,
        'core_wrong': standard_wrong,
        'control_accuracy': control_accuracy,
        'control_correct': control_correct,
        'control_wrong': control_wrong
    }


def generate_overall_accuracy_chart(data):
    """Chart 1: Overall Correct vs Wrong Answers."""
    correct = parse_number(data.get('Total Correct Answers (Count)', 0))
    wrong = parse_number(data.get('Total Wrong Answers (Count)', 0))
    accuracy = parse_number(data.get('Overall Accuracy (%)', 0))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Correct', 'Wrong']
    values = [correct, wrong]
    colors = [COLOR_CORRECT, COLOR_WRONG]
    
    bars = ax.bar(categories, values, color=colors, width=0.6, edgecolor='black', linewidth=2)
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(val)}',
                ha='center', va='bottom', fontsize=16, fontweight='bold')
    
    ax.set_ylabel('Number of Answers', fontsize=14, fontweight='bold')
    ax.set_title(f'Overall Accuracy: {accuracy:.1f}%\n(Correct vs Wrong Answers)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, max(values) * 1.15)
    
    # Add grid
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '1_overall_accuracy.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 1_overall_accuracy.png")


def generate_text_vs_audio_chart(data):
    """Chart 2: Text vs Audio Comparison."""
    text_correct = parse_number(data.get('Text Answers - Correct (Count)', 0))
    text_wrong = parse_number(data.get('Text Answers - Wrong (Count)', 0))
    audio_correct = parse_number(data.get('Audio Answers - Correct (Count)', 0))
    audio_wrong = parse_number(data.get('Audio Answers - Wrong (Count)', 0))
    
    text_accuracy = parse_number(data.get('Text Accuracy (%)', 0))
    audio_accuracy = parse_number(data.get('Audio Accuracy (%)', 0))
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    categories = ['Text Questions', 'Audio Questions']
    correct_vals = [text_correct, audio_correct]
    wrong_vals = [text_wrong, audio_wrong]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, correct_vals, width, label='Correct', 
                   color=COLOR_CORRECT, edgecolor='black', linewidth=2)
    bars2 = ax.bar(x + width/2, wrong_vals, width, label='Wrong', 
                   color=COLOR_WRONG, edgecolor='black', linewidth=2)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('Number of Answers', fontsize=14, fontweight='bold')
    ax.set_title('Text vs Audio Performance Comparison', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=13, fontweight='bold')
    ax.legend(fontsize=12, loc='upper right')
    
    # Set ylim to make room for accuracy text at bottom
    max_val = max(correct_vals + wrong_vals)
    ax.set_ylim(-max_val * 0.12, max_val * 1.15)
    
    # Add accuracy percentages below x-axis (using axis coordinates for better positioning)
    y_pos = -max_val * 0.08
    ax.text(0, y_pos, f'{text_accuracy:.1f}% accuracy', 
            ha='center', va='top', 
            fontsize=13, fontweight='bold', color=COLOR_TEXT)
    ax.text(1, y_pos, f'{audio_accuracy:.1f}% accuracy', 
            ha='center', va='top', 
            fontsize=13, fontweight='bold', color=COLOR_AUDIO)
    
    # Add grid
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '2_text_vs_audio.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 2_text_vs_audio.png")


def generate_accuracy_comparison_chart(data):
    """Chart 3: Accuracy Percentage Comparison."""
    overall_acc = parse_number(data.get('Overall Accuracy (%)', 0))
    text_acc = parse_number(data.get('Text Accuracy (%)', 0))
    audio_acc = parse_number(data.get('Audio Accuracy (%)', 0))
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    categories = ['Overall', 'Text', 'Audio']
    accuracies = [overall_acc, text_acc, audio_acc]
    colors = ['#9C27B0', COLOR_TEXT, COLOR_AUDIO]
    
    bars = ax.bar(categories, accuracies, color=colors, width=0.6, 
                  edgecolor='black', linewidth=2)
    
    # Add percentage labels
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc:.1f}%',
                ha='center', va='bottom', fontsize=18, fontweight='bold')
    
    ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
    ax.set_title('Accuracy Comparison Across Question Types', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    
    # Add horizontal line at 75%
    ax.axhline(y=75, color='red', linestyle='--', linewidth=2, alpha=0.5, label='75% threshold')
    ax.legend(fontsize=11)
    
    # Add grid
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '3_accuracy_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 3_accuracy_comparison.png")


def generate_time_analysis_chart(data):
    """Chart 4: Time Analysis."""
    def parse_time(time_str):
        """Convert mm:ss to seconds."""
        try:
            parts = time_str.split(':')
            return int(parts[0]) * 60 + int(parts[1])
        except:
            return 0
    
    avg_overall = parse_time(data.get('Average Time to Answer - Overall (mm:ss)', '0:00'))
    avg_text = parse_time(data.get('Average Time to Answer - Text (mm:ss)', '0:00'))
    avg_audio = parse_time(data.get('Average Time to Answer - Audio (mm:ss)', '0:00'))
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    categories = ['Overall', 'Text', 'Audio']
    times = [avg_overall, avg_text, avg_audio]
    colors = ['#9C27B0', COLOR_TEXT, COLOR_AUDIO]
    
    bars = ax.bar(categories, times, color=colors, width=0.6, 
                  edgecolor='black', linewidth=2)
    
    # Add time labels
    for bar, time_sec in zip(bars, times):
        height = bar.get_height()
        minutes = time_sec // 60
        seconds = time_sec % 60
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{minutes}:{seconds:02d}',
                ha='center', va='bottom', fontsize=16, fontweight='bold')
    
    ax.set_ylabel('Average Time (seconds)', fontsize=14, fontweight='bold')
    ax.set_title('Average Time to Answer Questions', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, max(times) * 1.15)
    
    # Add grid
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add explanation
    ratio = data.get('Audio/Text Time Ratio', 'N/A')
    ax.text(0.5, 0.95, f'Audio questions take {ratio}x longer than Text questions',
            transform=ax.transAxes, ha='center', va='top', fontsize=12,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '4_time_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 4_time_analysis.png")


def generate_pairs_overview_chart(users_pairs):
    """Chart 5: Pairs Analysis Overview."""
    total_correct = sum(u['correct_pairs'] for u in users_pairs)
    total_wrong = sum(u['wrong_pairs'] for u in users_pairs)
    total_partial = sum(u['partial_pairs'] for u in users_pairs)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    categories = ['Both Correct', 'Both Wrong', 'One Correct']
    values = [total_correct, total_wrong, total_partial]
    colors = [COLOR_CORRECT, COLOR_WRONG, COLOR_PARTIAL]
    
    bars = ax.bar(categories, values, color=colors, width=0.6, 
                  edgecolor='black', linewidth=2)
    
    # Add value labels
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(val)}',
                ha='center', va='bottom', fontsize=18, fontweight='bold')
    
    ax.set_ylabel('Number of Question Pairs', fontsize=14, fontweight='bold')
    ax.set_title('Question Pairs Analysis\n(Standard vs Control)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, max(values) * 1.15)
    
    # Add grid
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add explanation
    total_pairs = sum(values)
    consistency = (total_correct + total_wrong) / total_pairs * 100 if total_pairs > 0 else 0
    ax.text(0.5, 0.05, 
            f'Consistency Rate: {consistency:.1f}% (students answered both questions in pair the same way)',
            transform=ax.transAxes, ha='center', va='bottom', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '5_pairs_overview.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 5_pairs_overview.png")


def generate_pairs_pie_chart(users_pairs):
    """Chart 6: Pairs Distribution Pie Chart."""
    total_correct = sum(u['correct_pairs'] for u in users_pairs)
    total_wrong = sum(u['wrong_pairs'] for u in users_pairs)
    total_partial = sum(u['partial_pairs'] for u in users_pairs)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    labels = ['Both Correct', 'Both Wrong', 'One Correct\n(Inconsistent)']
    sizes = [total_correct, total_wrong, total_partial]
    colors = [COLOR_CORRECT, COLOR_WRONG, COLOR_PARTIAL]
    explode = (0.05, 0.05, 0.1)
    
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                        autopct='%1.1f%%', startangle=90, textprops={'fontsize': 13},
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 2})
    
    # Make percentage text bold and larger
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(16)
        autotext.set_fontweight('bold')
    
    # Make labels bold
    for text in texts:
        text.set_fontweight('bold')
        text.set_fontsize(12)
    
    ax.set_title('Distribution of Question Pair Results', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Add total count
    total = sum(sizes)
    ax.text(0.5, -0.1, f'Total Pairs Analyzed: {total}',
            transform=ax.transAxes, ha='center', va='top', fontsize=13, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '6_pairs_pie_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 6_pairs_pie_chart.png")


def generate_user_pairs_performance(users_pairs):
    """Chart 7: Top Users by Correct Pairs."""
    # Sort by correct pairs
    sorted_users = sorted(users_pairs, key=lambda x: x['correct_pairs'], reverse=True)[:10]
    
    if not sorted_users:
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    user_labels = [u['user_id'][:15] + '...' for u in sorted_users]
    correct = [u['correct_pairs'] for u in sorted_users]
    partial = [u['partial_pairs'] for u in sorted_users]
    wrong = [u['wrong_pairs'] for u in sorted_users]
    
    x = np.arange(len(user_labels))
    width = 0.25
    
    bars1 = ax.bar(x - width, correct, width, label='Both Correct', 
                   color=COLOR_CORRECT, edgecolor='black', linewidth=1)
    bars2 = ax.bar(x, partial, width, label='One Correct', 
                   color=COLOR_PARTIAL, edgecolor='black', linewidth=1)
    bars3 = ax.bar(x + width, wrong, width, label='Both Wrong', 
                   color=COLOR_WRONG, edgecolor='black', linewidth=1)
    
    # Add value labels
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=9)
    
    ax.set_ylabel('Number of Pairs', fontsize=13, fontweight='bold')
    ax.set_title('Top 10 Users - Question Pairs Performance', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(user_labels, rotation=45, ha='right', fontsize=9)
    ax.legend(fontsize=11, loc='upper right')
    
    # Add grid
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '7_user_pairs_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 7_user_pairs_performance.png")


def generate_three_accuracy_metrics_chart(accuracy_data):
    """Chart 8: Three Accuracy Metrics Comparison (Overall, Control, Core)."""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Extract data
    overall_acc = accuracy_data['overall_accuracy']
    control_acc = accuracy_data['control_accuracy']
    core_acc = accuracy_data['core_accuracy']
    
    categories = ['Overall Accuracy\n(All Questions)', 
                  'Control Accuracy\n(Consistency Check)', 
                  'Core Accuracy\n(Actual Knowledge)']
    accuracies = [overall_acc, control_acc, core_acc]
    colors = ['#9C27B0', '#FF5722', '#4CAF50']  # Purple, Orange-Red, Green
    
    bars = ax.bar(categories, accuracies, color=colors, width=0.6, 
                  edgecolor='black', linewidth=2)
    
    # Add percentage labels on bars
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc:.2f}%',
                ha='center', va='bottom', fontsize=20, fontweight='bold')
    
    # Add counts below each bar
    counts_text = [
        f'{accuracy_data["overall_correct"]}C / {accuracy_data["overall_wrong"]}W',
        f'{accuracy_data["control_correct"]}C / {accuracy_data["control_wrong"]}W',
        f'{accuracy_data["core_correct"]}C / {accuracy_data["core_wrong"]}W'
    ]
    
    for i, (bar, count_text) in enumerate(zip(bars, counts_text)):
        ax.text(bar.get_x() + bar.get_width()/2., -3,
                count_text,
                ha='center', va='top', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgray', alpha=0.7))
    
    ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
    ax.set_title('Three Accuracy Metrics Comparison\n(Based on Question Type)', 
                 fontsize=17, fontweight='bold', pad=20)
    ax.set_ylim(-8, 105)
    
    # Add grid
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add explanatory text boxes at the bottom with proper formulas
    explanation_overall = "Formula (1):\nAccuracy = (Correct / (Correct + Wrong)) × 100\n\nAll questions (standard + control)"
    explanation_control = "Formula (2):\nAccuracy_control = (C_dup / (C_dup + W_dup)) × 100\n\nOnly control questions (duplicates)"
    explanation_core = "Formula (3):\nAccuracy_core = (C_core / (C_core + W_core)) × 100\n\nOnly standard questions (exclude control)"
    
    fig.text(0.15, 0.02, explanation_overall, ha='center', va='bottom', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#E1BEE7', alpha=0.8, linewidth=1.5))
    fig.text(0.5, 0.02, explanation_control, ha='center', va='bottom', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#FFCCBC', alpha=0.8, linewidth=1.5))
    fig.text(0.85, 0.02, explanation_core, ha='center', va='bottom', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#C8E6C9', alpha=0.8, linewidth=1.5))
    
    plt.tight_layout(rect=[0, 0.14, 1, 1])
    plt.savefig(VISUALS_DIR / '8_three_accuracy_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 8_three_accuracy_metrics.png")


def main():
    """Main function to generate all visualizations."""
    print("\n" + "="*60)
    print("  GENERATING STATISTICS VISUALIZATIONS")
    print("="*60 + "\n")
    
    print("Loading data from summary.csv...")
    data = load_summary_data()
    print(f"✓ Loaded {len(data)} metrics\n")
    
    print("Loading user pair statistics...")
    users_pairs = load_user_pair_data()
    print(f"✓ Loaded pair data for {len(users_pairs)} users\n")
    
    print("Calculating standard vs control accuracy...")
    accuracy_metrics = calculate_standard_vs_control_accuracy()
    print(f"✓ Overall: {accuracy_metrics['overall_accuracy']:.2f}%, Control: {accuracy_metrics['control_accuracy']:.2f}%, Core: {accuracy_metrics['core_accuracy']:.2f}%\n")
    
    print("Generating charts...\n")
    
    # Generate all charts
    generate_overall_accuracy_chart(data)
    generate_text_vs_audio_chart(data)
    generate_accuracy_comparison_chart(data)
    generate_time_analysis_chart(data)
    generate_pairs_overview_chart(users_pairs)
    generate_pairs_pie_chart(users_pairs)
    generate_user_pairs_performance(users_pairs)
    generate_three_accuracy_metrics_chart(accuracy_metrics)
    
    print("\n" + "="*60)
    print(f"✅ All visualizations saved to: {VISUALS_DIR}")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()

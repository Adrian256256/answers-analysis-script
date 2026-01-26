#!/usr/bin/env python3
"""
Generate visual statistics and charts for exam analysis.
Creates various diagrams, tables, and visualizations saved to the 'visuals' folder.
"""

import csv
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Paths
BASE_DIR = Path(__file__).parent.parent
USER_CSVS_DIR = BASE_DIR / 'manual_corrected_csvs' / 'user_csvs'
VISUALS_DIR = BASE_DIR / 'visuals'
VISUALS_DIR.mkdir(exist_ok=True)

# Colors
COLOR_CORRECT = '#4CAF50'  # Green
COLOR_WRONG = '#F44336'    # Red
COLOR_TEXT = '#2196F3'     # Blue
COLOR_AUDIO = '#FF9800'    # Orange


def collect_user_data():
    """Collect all user statistics from CSV files."""
    users_data = []
    
    for user_dir in sorted(USER_CSVS_DIR.glob('*')):
        if not user_dir.is_dir():
            continue
        
        user_id = user_dir.name
        answers_file = user_dir / 'answers.csv'
        
        if not answers_file.exists():
            continue
        
        with open(answers_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            correct = 0
            wrong = 0
            text_correct = 0
            text_wrong = 0
            audio_correct = 0
            audio_wrong = 0
            
            for row in reader:
                if len(row) >= 12:
                    answer_type = row[2]
                    is_correct = 'x' in row[10]
                    is_wrong = 'x' in row[11]
                    
                    if is_correct:
                        correct += 1
                        if answer_type == 'Text':
                            text_correct += 1
                        elif answer_type == 'Audio':
                            audio_correct += 1
                    
                    if is_wrong:
                        wrong += 1
                        if answer_type == 'Text':
                            text_wrong += 1
                        elif answer_type == 'Audio':
                            audio_wrong += 1
        
        total = correct + wrong
        if total > 0:
            users_data.append({
                'user_id': user_id,
                'correct': correct,
                'wrong': wrong,
                'total': total,
                'accuracy': correct / total * 100,
                'text_correct': text_correct,
                'text_wrong': text_wrong,
                'audio_correct': audio_correct,
                'audio_wrong': audio_wrong
            })
    
    return users_data


def generate_overall_accuracy_chart(users_data):
    """Generate bar chart showing overall correct vs wrong answers."""
    total_correct = sum(u['correct'] for u in users_data)
    total_wrong = sum(u['wrong'] for u in users_data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Correct', 'Incorrect']
    values = [total_correct, total_wrong]
    colors = [COLOR_CORRECT, COLOR_WRONG]
    
    bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value}\n({value/(total_correct+total_wrong)*100:.1f}%)',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Number of Answers', fontsize=12, fontweight='bold')
    ax.set_title('Answer Distribution - Overall Total', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, max(values) * 1.15)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '1_overall_accuracy.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 1_overall_accuracy.png")


def generate_text_vs_audio_chart(users_data):
    """Generate comparison chart for Text vs Audio answers."""
    text_correct = sum(u['text_correct'] for u in users_data)
    text_wrong = sum(u['text_wrong'] for u in users_data)
    audio_correct = sum(u['audio_correct'] for u in users_data)
    audio_wrong = sum(u['audio_wrong'] for u in users_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart
    categories = ['Text', 'Audio']
    correct_values = [text_correct, audio_correct]
    wrong_values = [text_wrong, audio_wrong]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, correct_values, width, label='Correct', 
                    color=COLOR_CORRECT, alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax1.bar(x + width/2, wrong_values, width, label='Incorrect',
                    color=COLOR_WRONG, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('Number of Answers', fontsize=12, fontweight='bold')
    ax1.set_title('Comparison: Text vs Audio Answers', fontsize=13, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    
    # Accuracy comparison
    text_total = text_correct + text_wrong
    audio_total = audio_correct + audio_wrong
    text_accuracy = text_correct / text_total * 100 if text_total > 0 else 0
    audio_accuracy = audio_correct / audio_total * 100 if audio_total > 0 else 0
    
    accuracies = [text_accuracy, audio_accuracy]
    colors_acc = [COLOR_TEXT, COLOR_AUDIO]
    
    bars = ax2.bar(categories, accuracies, color=colors_acc, alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc:.2f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Accuracy: Text vs Audio', fontsize=13, fontweight='bold', pad=15)
    ax2.set_ylim(0, 100)
    ax2.axhline(y=50, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '2_text_vs_audio.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 2_text_vs_audio.png")


def generate_user_performance_chart(users_data):
    """Generate chart showing individual user performance."""
    # Sort by accuracy
    sorted_users = sorted(users_data, key=lambda x: x['accuracy'], reverse=True)
    
    # Take top 15 users
    top_users = sorted_users[:15]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    user_labels = [f"User {i+1}" for i in range(len(top_users))]
    accuracies = [u['accuracy'] for u in top_users]
    colors = [COLOR_CORRECT if acc >= 80 else COLOR_AUDIO if acc >= 60 else COLOR_WRONG 
              for acc in accuracies]
    
    bars = ax.barh(user_labels, accuracies, color=colors, alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i, (bar, acc, user) in enumerate(zip(bars, accuracies, top_users)):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2.,
                f'{acc:.1f}% ({user["correct"]}/{user["total"]})',
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Users - Individual Performance', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 105)
    ax.axvline(x=80, color='green', linestyle='--', alpha=0.5, linewidth=1, label='Pass (80%)')
    ax.axvline(x=60, color='orange', linestyle='--', alpha=0.5, linewidth=1, label='Satisfactory (60%)')
    ax.grid(axis='x', alpha=0.3)
    ax.legend(loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '3_user_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 3_user_performance.png")


def generate_accuracy_distribution_chart(users_data):
    """Generate histogram showing distribution of user accuracies."""
    accuracies = [u['accuracy'] for u in users_data]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bins = [0, 40, 50, 60, 70, 80, 90, 100]
    n, bins, patches = ax.hist(accuracies, bins=bins, edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Color bins
    colors = ['#d32f2f', '#f57c00', '#fbc02d', '#afb42b', '#689f38', '#388e3c', '#1b5e20']
    for i, patch in enumerate(patches):
        patch.set_facecolor(colors[i])
    
    # Add value labels
    for i, (count, bin_edge) in enumerate(zip(n, bins[:-1])):
        if count > 0:
            bin_center = (bins[i] + bins[i+1]) / 2
            ax.text(bin_center, count, f'{int(count)}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Accuracy Range (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Users', fontsize=12, fontweight='bold')
    ax.set_title('User Accuracy Distribution', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    # Add statistics text
    mean_acc = np.mean(accuracies)
    median_acc = np.median(accuracies)
    stats_text = f'Mean: {mean_acc:.1f}%\nMedian: {median_acc:.1f}%'
    ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
           verticalalignment='top', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
           fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '4_accuracy_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 4_accuracy_distribution.png")


def generate_pie_charts(users_data):
    """Generate pie charts for overall statistics."""
    total_correct = sum(u['correct'] for u in users_data)
    total_wrong = sum(u['wrong'] for u in users_data)
    text_total = sum(u['text_correct'] + u['text_wrong'] for u in users_data)
    audio_total = sum(u['audio_correct'] + u['audio_wrong'] for u in users_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie 1: Correct vs Wrong
    sizes1 = [total_correct, total_wrong]
    labels1 = [f'Correct\n{total_correct} ({total_correct/(total_correct+total_wrong)*100:.1f}%)',
               f'Incorrect\n{total_wrong} ({total_wrong/(total_correct+total_wrong)*100:.1f}%)']
    colors1 = [COLOR_CORRECT, COLOR_WRONG]
    explode1 = (0.05, 0)
    
    ax1.pie(sizes1, explode=explode1, labels=labels1, colors=colors1,
           autopct='', startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'},
           wedgeprops={'edgecolor': 'black', 'linewidth': 2})
    ax1.set_title('Answer Distribution\nCorrect vs Incorrect', 
                 fontsize=13, fontweight='bold', pad=20)
    
    # Pie 2: Text vs Audio
    sizes2 = [text_total, audio_total]
    labels2 = [f'Text\n{text_total} ({text_total/(text_total+audio_total)*100:.1f}%)',
               f'Audio\n{audio_total} ({audio_total/(text_total+audio_total)*100:.1f}%)']
    colors2 = [COLOR_TEXT, COLOR_AUDIO]
    explode2 = (0.05, 0)
    
    ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2,
           autopct='', startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'},
           wedgeprops={'edgecolor': 'black', 'linewidth': 2})
    ax2.set_title('Answer Type Distribution\nText vs Audio', 
                 fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '5_pie_charts.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 5_pie_charts.png")


def generate_summary_table(users_data):
    """Generate a summary table image."""
    total_correct = sum(u['correct'] for u in users_data)
    total_wrong = sum(u['wrong'] for u in users_data)
    total_graded = total_correct + total_wrong
    
    text_correct = sum(u['text_correct'] for u in users_data)
    text_wrong = sum(u['text_wrong'] for u in users_data)
    text_total = text_correct + text_wrong
    
    audio_correct = sum(u['audio_correct'] for u in users_data)
    audio_wrong = sum(u['audio_wrong'] for u in users_data)
    audio_total = audio_correct + audio_wrong
    
    # Create table data
    table_data = [
        ['Category', 'Correct', 'Incorrect', 'Total', 'Accuracy'],
        ['OVERALL', f'{total_correct}', f'{total_wrong}', f'{total_graded}', 
         f'{total_correct/total_graded*100:.2f}%'],
        ['Text', f'{text_correct}', f'{text_wrong}', f'{text_total}', 
         f'{text_correct/text_total*100:.2f}%' if text_total > 0 else 'N/A'],
        ['Audio', f'{audio_correct}', f'{audio_wrong}', f'{audio_total}', 
         f'{audio_correct/audio_total*100:.2f}%' if audio_total > 0 else 'N/A'],
    ]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.25, 0.15, 0.15, 0.15, 0.2])
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.5)
    
    # Style header row
    for i in range(5):
        cell = table[(0, i)]
        cell.set_facecolor('#2196F3')
        cell.set_text_props(weight='bold', color='white', fontsize=13)
    
    # Style data rows
    colors_alt = ['#E3F2FD', '#FFFFFF']
    for i in range(1, 4):
        for j in range(5):
            cell = table[(i, j)]
            cell.set_facecolor(colors_alt[i % 2])
            cell.set_text_props(fontsize=12, weight='bold')
            if i == 1:  # OVERALL row
                cell.set_facecolor('#FFF9C4')
    
    ax.set_title('Summary Table - General Statistics', 
                fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '6_summary_table.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 6_summary_table.png")


def main():
    """Main function to generate all visualizations."""
    print("\n" + "="*60)
    print("  GENERATING STATISTICS VISUALIZATIONS")
    print("="*60 + "\n")
    
    print("Collecting data from CSV files...")
    users_data = collect_user_data()
    print(f"Loaded data for {len(users_data)} users\n")
    
    print("Generating charts and diagrams...\n")
    
    generate_overall_accuracy_chart(users_data)
    generate_text_vs_audio_chart(users_data)
    generate_user_performance_chart(users_data)
    generate_accuracy_distribution_chart(users_data)
    generate_pie_charts(users_data)
    generate_summary_table(users_data)
    
    print("\n" + "="*60)
    print(f"All visualizations have been generated in: {VISUALS_DIR}")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()

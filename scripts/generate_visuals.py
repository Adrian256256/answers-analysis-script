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


def generate_text_vs_audio_detailed_comparison(users_data):
    """Generate simple, clear comparison of total correct answers."""
    text_correct = sum(u['text_correct'] for u in users_data)
    text_wrong = sum(u['text_wrong'] for u in users_data)
    audio_correct = sum(u['audio_correct'] for u in users_data)
    audio_wrong = sum(u['audio_wrong'] for u in users_data)
    
    text_total = text_correct + text_wrong
    audio_total = audio_correct + audio_wrong
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Simple side-by-side comparison
    categories = ['Text Questions', 'Audio Questions']
    correct_vals = [text_correct, audio_correct]
    wrong_vals = [text_wrong, audio_wrong]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, correct_vals, width, label='Correct Answers', 
                   color=COLOR_CORRECT, alpha=0.85, edgecolor='black', linewidth=2)
    bars2 = ax.bar(x + width/2, wrong_vals, width, label='Incorrect Answers',
                   color=COLOR_WRONG, alpha=0.85, edgecolor='black', linewidth=2)
    
    # Add large value labels on bars
    for bar, val in zip(bars1, correct_vals):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                f'{val}',
                ha='center', va='center', fontsize=20, fontweight='bold', color='white')
    
    for bar, val in zip(bars2, wrong_vals):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                f'{val}',
                ha='center', va='center', fontsize=20, fontweight='bold', color='white')
    
    # Add total annotations above bars
    for i, (correct, wrong) in enumerate(zip(correct_vals, wrong_vals)):
        total = correct + wrong
        ax.text(x[i], max(correct, wrong) + 10,
               f'Total: {total} answers',
               ha='center', va='bottom', fontsize=12, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.7))
    
    ax.set_ylabel('Number of Answers', fontsize=14, fontweight='bold')
    ax.set_title('How Many Answers Were Correct?\nText Questions vs Audio Questions', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=13, fontweight='bold')
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(max(correct_vals), max(wrong_vals)) * 1.25)
    
    # Add explanation box
    explanation = f'Text Questions: {text_correct}/{text_total} correct\nAudio Questions: {audio_correct}/{audio_total} correct'
    ax.text(0.02, 0.98, explanation, transform=ax.transAxes,
           fontsize=11, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '7_total_correct_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 7_total_correct_comparison.png")


def generate_user_text_vs_audio_performance(users_data):
    """Generate simple chart showing accuracy percentages for text vs audio."""
    text_correct = sum(u['text_correct'] for u in users_data)
    text_wrong = sum(u['text_wrong'] for u in users_data)
    audio_correct = sum(u['audio_correct'] for u in users_data)
    audio_wrong = sum(u['audio_wrong'] for u in users_data)
    
    text_total = text_correct + text_wrong
    audio_total = audio_correct + audio_wrong
    
    text_accuracy = text_correct / text_total * 100 if text_total > 0 else 0
    audio_accuracy = audio_correct / audio_total * 100 if audio_total > 0 else 0
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    categories = ['Text Questions', 'Audio Questions']
    accuracies = [text_accuracy, audio_accuracy]
    colors = [COLOR_TEXT, COLOR_AUDIO]
    
    bars = ax.bar(categories, accuracies, color=colors, alpha=0.85, 
                  edgecolor='black', linewidth=3, width=0.6)
    
    # Add large percentage labels
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
               f'{acc:.1f}%',
               ha='center', va='center', fontsize=28, fontweight='bold', color='white')
    
    # Add reference lines with labels
    ax.axhline(y=80, color='green', linestyle='--', linewidth=2, alpha=0.5)
    ax.text(0.02, 81, 'Pass threshold (80%)', fontsize=10, color='green', 
           fontweight='bold', transform=ax.get_yaxis_transform())
    
    ax.axhline(y=60, color='orange', linestyle='--', linewidth=2, alpha=0.5)
    ax.text(0.02, 61, 'Satisfactory (60%)', fontsize=10, color='orange',
           fontweight='bold', transform=ax.get_yaxis_transform())
    
    ax.set_ylabel('Accuracy Percentage (%)', fontsize=14, fontweight='bold')
    ax.set_title('Which Type of Questions Was Easier?\nAccuracy Comparison', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.set_xticklabels(categories, fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add performance difference annotation
    diff = text_accuracy - audio_accuracy
    diff_text = f'Text questions were {abs(diff):.1f}% {"easier" if diff > 0 else "harder"} than Audio'
    ax.text(0.5, 0.95, diff_text, transform=ax.transAxes,
           ha='center', va='top', fontsize=13, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.8))
    
    # Add summary box
    summary = f'Text: {text_correct} correct out of {text_total}\nAudio: {audio_correct} correct out of {audio_total}'
    ax.text(0.98, 0.02, summary, transform=ax.transAxes,
           fontsize=11, verticalalignment='bottom', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '8_accuracy_percentage_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 8_accuracy_percentage_comparison.png")


def generate_text_audio_consistency_analysis(users_data):
    """Show how many users prefer text vs audio based on their scores."""
    # Filter users with both types
    users_with_both = [u for u in users_data 
                       if (u['text_correct'] + u['text_wrong']) > 0 
                       and (u['audio_correct'] + u['audio_wrong']) > 0]
    
    if len(users_with_both) == 0:
        print("⚠ Skipped: 9_user_preference_analysis.png (no users with both answer types)")
        return
    
    # Count preferences
    text_better = 0
    audio_better = 0
    equal = 0
    
    for user in users_with_both:
        text_total = user['text_correct'] + user['text_wrong']
        audio_total = user['audio_correct'] + user['audio_wrong']
        
        text_acc = user['text_correct'] / text_total * 100 if text_total > 0 else 0
        audio_acc = user['audio_correct'] / audio_total * 100 if audio_total > 0 else 0
        
        diff = abs(text_acc - audio_acc)
        
        if diff < 2:  # Consider equal if difference is less than 2%
            equal += 1
        elif text_acc > audio_acc:
            text_better += 1
        else:
            audio_better += 1
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    categories = ['Better at\nText Questions', 'Better at\nAudio Questions', 'Equal\nPerformance']
    values = [text_better, audio_better, equal]
    colors_bar = [COLOR_TEXT, COLOR_AUDIO, '#9E9E9E']
    
    bars = ax.bar(categories, values, color=colors_bar, alpha=0.85,
                  edgecolor='black', linewidth=3, width=0.6)
    
    # Add large value labels
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
               f'{val}\nusers',
               ha='center', va='center', fontsize=18, fontweight='bold', color='white')
        
        # Add percentage above bar
        pct = val / len(users_with_both) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
               f'{pct:.1f}%',
               ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('Number of Users', fontsize=14, fontweight='bold')
    ax.set_title('Do Students Perform Better on Text or Audio Questions?\nUser Preference Analysis', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(values) * 1.3)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add explanation
    total_users = len(users_with_both)
    explanation = f'Analysis based on {total_users} users who answered both types of questions\n'
    explanation += f'"Equal" means the difference in accuracy is less than 2%'
    ax.text(0.5, 0.95, explanation, transform=ax.transAxes,
           ha='center', va='top', fontsize=11,
           bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '9_user_preference_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 9_user_preference_analysis.png")


def generate_text_audio_statistical_summary(users_data):
    """Simple breakdown showing the numbers behind text vs audio performance."""
    text_correct = sum(u['text_correct'] for u in users_data)
    text_wrong = sum(u['text_wrong'] for u in users_data)
    audio_correct = sum(u['audio_correct'] for u in users_data)
    audio_wrong = sum(u['audio_wrong'] for u in users_data)
    
    text_total = text_correct + text_wrong
    audio_total = audio_correct + audio_wrong
    
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.axis('tight')
    ax.axis('off')
    
    # Create simple, clear table
    table_data = [
        ['', 'Text Questions', 'Audio Questions', 'Difference'],
        ['Total Questions', f'{text_total}', f'{audio_total}', f'{text_total - audio_total:+d}'],
        ['Correct Answers', f'{text_correct}', f'{audio_correct}', f'{text_correct - audio_correct:+d}'],
        ['Incorrect Answers', f'{text_wrong}', f'{audio_wrong}', f'{text_wrong - audio_wrong:+d}'],
        ['Accuracy Rate', 
         f'{text_correct/text_total*100:.1f}%', 
         f'{audio_correct/audio_total*100:.1f}%', 
         f'{(text_correct/text_total - audio_correct/audio_total)*100:+.1f}%'],
    ]
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.25, 0.25, 0.25])
    
    table.auto_set_font_size(False)
    table.set_fontsize(16)
    table.scale(1, 3.5)
    
    # Style header row (row 0)
    for i in range(4):
        cell = table[(0, i)]
        cell.set_facecolor('#2196F3')
        cell.set_text_props(weight='bold', color='white', fontsize=18)
        cell.set_height(0.15)
    
    # Style data rows with alternating colors
    colors_alt = ['#E3F2FD', '#FFFFFF', '#E3F2FD', '#FFFFFF']
    for i in range(1, 5):
        for j in range(4):
            cell = table[(i, j)]
            cell.set_facecolor(colors_alt[i-1])
            
            # Make first column (labels) bold
            if j == 0:
                cell.set_text_props(fontsize=16, weight='bold', ha='left')
            else:
                cell.set_text_props(fontsize=18, weight='bold')
            
            # Highlight accuracy row
            if i == 4:
                cell.set_facecolor('#FFF9C4')
                cell.set_text_props(fontsize=20, weight='bold')
    
    # Add title with explanation
    title_text = 'The Numbers Behind Performance:\nText Questions vs Audio Questions'
    ax.text(0.5, 0.95, title_text, transform=ax.transAxes,
           ha='center', va='top', fontsize=20, fontweight='bold')
    
    # Add interpretation box
    text_acc = text_correct/text_total*100
    audio_acc = audio_correct/audio_total*100
    diff = text_acc - audio_acc
    
    if abs(diff) < 2:
        interpretation = 'Performance is nearly EQUAL on both question types'
        box_color = 'lightgreen'
    elif diff > 0:
        interpretation = f'Students perform BETTER on Text questions by {abs(diff):.1f}%'
        box_color = 'lightblue'
    else:
        interpretation = f'Students perform BETTER on Audio questions by {abs(diff):.1f}%'
        box_color = 'lightyellow'
    
    ax.text(0.5, 0.08, interpretation, transform=ax.transAxes,
           ha='center', va='top', fontsize=16, fontweight='bold',
           bbox=dict(boxstyle='round,pad=1', facecolor=box_color, alpha=0.9, linewidth=3))
    
    plt.tight_layout()
    plt.savefig(VISUALS_DIR / '10_numbers_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: 10_numbers_breakdown.png")


def main():
    """Main function to generate all visualizations."""
    print("\n" + "="*60)
    print("  GENERATING STATISTICS VISUALIZATIONS")
    print("="*60 + "\n")
    
    print("Collecting data from CSV files...")
    users_data = collect_user_data()
    print(f"Loaded data for {len(users_data)} users\n")
    
    print("Generating charts and diagrams...\n")
    
    # Original charts
    generate_overall_accuracy_chart(users_data)
    generate_text_vs_audio_chart(users_data)
    generate_user_performance_chart(users_data)
    generate_accuracy_distribution_chart(users_data)
    generate_pie_charts(users_data)
    generate_summary_table(users_data)
    
    # New detailed text vs audio analysis charts
    print("\nGenerating detailed Text vs Audio analysis...\n")
    generate_text_vs_audio_detailed_comparison(users_data)
    generate_user_text_vs_audio_performance(users_data)
    generate_text_audio_consistency_analysis(users_data)
    generate_text_audio_statistical_summary(users_data)
    
    print("\n" + "="*60)
    print(f"All visualizations have been generated in: {VISUALS_DIR}")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()

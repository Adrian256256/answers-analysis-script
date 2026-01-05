import json
from datetime import datetime

# Load the original JSON data
with open('exametric-439ba-default-rtdb-export _new.json', 'r') as f:
    data = json.load(f)

exam_progress = data.get('examProgress', {})
exam_results = data.get('examResults', {})

# Create simplified structure
simplified_data = {
    "users": []
}

# Process each user
for user_id in exam_progress.keys():
    user_data = {
        "user_id": user_id,
        "submitted": exam_progress[user_id].get('submitted', False),
        "tab_changes": exam_progress[user_id].get('tabChangeCount', 0),
        "start_timestamp": exam_progress[user_id].get('startTimestamp'),
        "answers": []
    }
    
    # Get user's exam results if available
    user_results = None
    if user_id in exam_results:
        # Get the first (and usually only) exam result for this user
        exam_ids = list(exam_results[user_id].keys())
        if exam_ids:
            user_results = exam_results[user_id][exam_ids[0]]
            user_data['email'] = user_results.get('email')
            user_data['total_score'] = user_results.get('score')
            user_data['correct_answers_count'] = user_results.get('correctAnswers')
            user_data['total_questions'] = user_results.get('totalQuestions')
            user_data['time_spent_seconds'] = user_results.get('timeSpent')
            user_data['submission_timestamp'] = user_results.get('timestamp')
    
    # Get answers from both exam progress and exam results
    progress_answers = exam_progress[user_id].get('answers', {})
    result_answers = {}
    
    if user_results and 'answers' in user_results:
        result_answers = user_results['answers']
    
    # Combine both sources (prefer results if available)
    all_answers = {**progress_answers, **result_answers}
    
    for question_id, answer_data in all_answers.items():
        answer_obj = {
            "question_id": question_id,
            "answered_at": answer_data.get('answeredAt'),
            "question_displayed_at": answer_data.get('questionDisplayedAt'),
            "time_to_answer_ms": answer_data.get('timeToAnswerMs'),
            "time_to_answer_seconds": round(answer_data.get('timeToAnswerMs', 0) / 1000, 2)
        }
        
        # Check if it's a text answer
        if 'text' in answer_data:
            answer_obj['answer_type'] = 'text'
            answer_obj['user_answer'] = answer_data['text']
        
        # Check if it's an audio answer
        if 'audioUrl' in answer_data:
            answer_obj['answer_type'] = 'audio'
            answer_obj['audio_url'] = answer_data['audioUrl']
            answer_obj['audio_duration_ms'] = answer_data.get('audioQuestionDurationMs')
            answer_obj['audio_duration_seconds'] = round(answer_data.get('audioQuestionDurationMs', 0) / 1000, 2)
            # Note: Transcription not available in the original data
            answer_obj['transcription'] = "NOT_AVAILABLE_IN_SOURCE_DATA"
        
        # Get expected answer and correctness from results
        if user_results and 'analysis' in user_results:
            analysis = user_results['analysis'].get(question_id)
            if analysis:
                answer_obj['correct'] = analysis.get('correct')
                answer_obj['expected_answers'] = analysis.get('expectedAnswers', [])
                # For audio answers, the transcribed text might be in userAnswer
                if answer_obj.get('answer_type') == 'audio' and 'userAnswer' in analysis:
                    answer_obj['user_answer'] = analysis['userAnswer']
                    answer_obj['transcription'] = analysis['userAnswer']
        
        user_data['answers'].append(answer_obj)
    
    # Only add users who have some data
    if user_data['answers'] or user_data.get('email'):
        simplified_data['users'].append(user_data)

# Add summary statistics
simplified_data['summary'] = {
    "total_users": len(simplified_data['users']),
    "submitted_users": sum(1 for u in simplified_data['users'] if u['submitted']),
    "in_progress_users": sum(1 for u in simplified_data['users'] if not u['submitted']),
    "total_answers": sum(len(u['answers']) for u in simplified_data['users']),
    "generated_at": datetime.now().isoformat()
}

# Save to new file
output_file = 'simplified_exam_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(simplified_data, f, indent=2, ensure_ascii=False)

print(f"✅ Simplified data saved to: {output_file}")
print(f"\n📊 Summary:")
print(f"  • Total users: {simplified_data['summary']['total_users']}")
print(f"  • Submitted: {simplified_data['summary']['submitted_users']}")
print(f"  • In progress: {simplified_data['summary']['in_progress_users']}")
print(f"  • Total answers: {simplified_data['summary']['total_answers']}")
print(f"\n💡 The simplified JSON contains:")
print(f"  • User ID")
print(f"  • Email (if submitted)")
print(f"  • Submission status")
print(f"  • Tab changes count")
print(f"  • Score and statistics")
print(f"  • All answers with:")
print(f"    - Question ID")
print(f"    - User answer (text or audio)")
print(f"    - Expected answers")
print(f"    - Correctness")
print(f"    - Time to answer")
print(f"    - Transcription (when available)")

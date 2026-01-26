import json
import csv
import os
from datetime import datetime
from collections import defaultdict

def load_data():
    """Încarcă datele din final_with_transcriptions.json (sau final.json dacă nu există)"""
    # Încearcă să încarce fișierul cu transcripții
    import os
    if os.path.exists('../data/final_with_transcriptions.json'):
        print('📝 Using final_with_transcriptions.json (with audio transcriptions)')
        with open('../data/final_with_transcriptions.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print('📝 Using final.json (no transcriptions yet)')
        with open('../data/final.json', 'r', encoding='utf-8') as f:
            return json.load(f)

def load_questions():
    """Încarcă maparea întrebărilor din questions_map.json"""
    import os
    if os.path.exists('../data/questions_map.json'):
        with open('../data/questions_map.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def ms_to_time_format(ms):
    """Convertește milisecunde în format mm:ss"""
    if not ms or ms == 0:
        return "0:00"
    total_seconds = ms / 1000
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return f"{minutes}:{seconds:02d}"

def seconds_to_time_format(seconds):
    """Convertește secunde în format mm:ss"""
    if not seconds or seconds == 0:
        return "0:00"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

def get_user_complete_data(user_id, data):
    """Obține datele complete pentru un user, fie din examProgress, fie din examResults"""
    exam_progress = data.get('examProgress', {}).get(user_id, {})
    
    # Dacă userul are submitted: true în examProgress, caută datele în examResults
    if exam_progress.get('submitted') == True:
        exam_results = data.get('examResults', {}).get(user_id, {})
        if exam_results:
            # Ia primul result (există un ID sub user_id)
            for result_id, result_data in exam_results.items():
                return result_data, True  # True înseamnă că e submitted
        return None, True
    
    return exam_progress, False

def get_user_email(user_id, data):
    """Obține emailul unui user din secțiunea users"""
    users = data.get('users', {})
    user_info = users.get(user_id, {})
    return user_info.get('email', 'N/A')

def create_user_csv(user_id, data, questions_map, output_dir='../output/user_csvs'):
    """Creează două CSV-uri pentru un user specific: summary.csv și answers.csv"""
    # Creează un folder pentru acest user
    user_folder = os.path.join(output_dir, user_id)
    os.makedirs(user_folder, exist_ok=True)
    
    summary_path = os.path.join(user_folder, 'summary.csv')
    answers_path = os.path.join(user_folder, 'answers.csv')
    
    # Obține datele complete pentru user
    user_data, is_submitted = get_user_complete_data(user_id, data)
    
    if not user_data:
        # Nu există date pentru acest user
        with open(summary_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['No data available for this user'])
        return
    
    # Creează summary.csv
    with open(summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['Metric', 'Value'])
        
        # Email (din secțiunea users)
        email = get_user_email(user_id, data)
        writer.writerow(['Email', email])
        
        # Timestamp final (dacă există)
        if 'timestamp' in user_data:
            submit_time = datetime.fromisoformat(user_data['timestamp'].replace('Z', '+00:00'))
            writer.writerow(['Submission Time (Date/Time)', submit_time.strftime('%Y-%m-%d %H:%M:%S')])
        
        # Rezultate
        if 'answeredCount' in user_data:
            writer.writerow(['Answered Count (Total)', user_data['answeredCount']])
        if 'totalQuestions' in user_data:
            total_questions = user_data['totalQuestions']
            answered_count = user_data.get('answeredCount', 0)
            unanswered = total_questions - answered_count
            
            writer.writerow(['Total Questions (Count)', total_questions])
            writer.writerow(['Unanswered Questions (Count)', unanswered])
        
        # Correct/Wrong answers - pentru completare manuală
        writer.writerow(['Correct Answers (Count)', ''])  # Gol pentru completare manuală
        writer.writerow(['Wrong Answers (Count)', ''])    # Gol pentru completare manuală
        
        if 'timeSpent' in user_data:
            time_spent_formatted = seconds_to_time_format(user_data['timeSpent'])
            writer.writerow(['Time Spent (mm:ss)', time_spent_formatted])
        
        # Informații generale (pentru userii in progress)
        if 'startTimestamp' in user_data:
            start_time = datetime.fromtimestamp(user_data['startTimestamp'] / 1000)
            writer.writerow(['Start Time (Date/Time)', start_time.strftime('%Y-%m-%d %H:%M:%S')])
        
        if 'currentSection' in user_data:
            writer.writerow(['Current Section', user_data['currentSection']])
        
        if 'currentQuestionIndex' in user_data:
            writer.writerow(['Current Question Index', user_data['currentQuestionIndex']])
        
        if 'tabChangeCount' in user_data:
            writer.writerow(['Tab Change Count (Total)', user_data['tabChangeCount']])
        
        # Întrebări audio și written
        if 'audioQuestionIds' in user_data:
            writer.writerow(['Audio Question IDs', ', '.join(user_data['audioQuestionIds'])])
        
        if 'writtenQuestionIds' in user_data:
            writer.writerow(['Written Question IDs', ', '.join(user_data['writtenQuestionIds'])])
    
    # Creează answers.csv
    if 'answers' in user_data and user_data['answers']:
        with open(answers_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Question ID', 'Question Text', 'Answer Type', 'User Answer (Text)', 'Audio URL', 
                           'Transcription (Audio Answers)', 'Time to Answer (mm:ss)', 'Answered At (Timestamp)', 
                           'Question Displayed At (Timestamp)', 'Audio Question Duration (mm:ss)', 'Correct', 'Wrong'])
            
            for question_id, answer in sorted(user_data['answers'].items()):
                answer_type = 'Audio' if 'audioUrl' in answer else 'Text'
                
                # Obține textul întrebării
                question_text = questions_map.get(question_id, 'N/A')
                
                # Pentru text - pune în coloana "User Answer (Text)"
                # Pentru audio - pune URL și transcripție separate
                user_text = answer.get('text', '') if 'text' in answer else ''
                audio_url = answer.get('audioUrl', '')
                transcription = answer.get('transcription', 'Not transcribed yet') if 'audioUrl' in answer else ''
                
                time_to_answer_ms = answer.get('timeToAnswerMs', 0)
                time_to_answer = ms_to_time_format(time_to_answer_ms) if time_to_answer_ms else ''
                answered_at = answer.get('answeredAt', '')
                displayed_at = answer.get('questionDisplayedAt', '')
                audio_duration_ms = answer.get('audioQuestionDurationMs', 0)
                audio_duration = ms_to_time_format(audio_duration_ms) if audio_duration_ms else ''
                
                writer.writerow([
                    question_id,
                    question_text,
                    answer_type,
                    user_text,
                    audio_url,
                    transcription,
                    time_to_answer,
                    answered_at,
                    displayed_at,
                    audio_duration,
                    '',  # Correct - empty for manual verification
                    ''   # Wrong - empty for manual verification
                ])
    
    print(f'Created CSVs for user: {user_id}')

def create_statistics_csv(data, output_dir='../output/general_statistics'):
    """Creează două CSV-uri separate cu statistici: summary.csv și users.csv"""
    
    # Creează folderul pentru statistici
    os.makedirs(output_dir, exist_ok=True)
    
    exam_progress = data.get('examProgress', {})
    
    # Calculează mai întâi toate statisticile generale
    total_users = len(exam_progress)
    submitted_count = 0
    in_progress_count = 0
    
    all_text_times = []
    all_audio_times = []
    all_times = []
    all_tab_changes = []
    total_text_answers = 0
    total_audio_answers = 0
    total_answered = 0
    total_time_spent = 0
    
    # Colectează date pentru statistici
    for user_id in exam_progress.keys():
        user_data, is_submitted = get_user_complete_data(user_id, data)
        
        if not user_data:
            submitted_count += 1
            continue
        
        if is_submitted:
            submitted_count += 1
        else:
            in_progress_count += 1
        
        answers = user_data.get('answers', {})
        
        # Tipuri de răspunsuri și timpi
        for ans in answers.values():
            if 'timeToAnswerMs' in ans:
                time = ans['timeToAnswerMs']
                all_times.append(time)
                
                if 'text' in ans:
                    total_text_answers += 1
                    all_text_times.append(time)
                elif 'audioUrl' in ans:
                    total_audio_answers += 1
                    all_audio_times.append(time)
        
        # Tab changes
        if 'tabChangeCount' in user_data:
            all_tab_changes.append(user_data['tabChangeCount'])
        
        # Răspunsuri
        if 'answeredCount' in user_data:
            total_answered += user_data['answeredCount']
        if 'timeSpent' in user_data:
            total_time_spent += user_data['timeSpent']
    
    # 1. Creează summary.csv cu statistici generale
    summary_path = os.path.join(output_dir, 'summary.csv')
    with open(summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Users (Count)', total_users])
        writer.writerow(['Submitted Users (Count)', submitted_count])
        writer.writerow(['In Progress Users (Count)', in_progress_count])
        writer.writerow([])
        
        writer.writerow(['Total Answers (Count)', total_text_answers + total_audio_answers])
        writer.writerow(['Total Text Answers (Count)', total_text_answers])
        writer.writerow(['Total Audio Answers (Count)', total_audio_answers])
        writer.writerow(['Text vs Audio Ratio', f'{round(total_text_answers / total_audio_answers, 2)}:1' if total_audio_answers > 0 else 'N/A'])
        writer.writerow([])
        
        # Statistici timp de răspuns
        if all_times:
            avg_overall_ms = sum(all_times) / len(all_times)
            writer.writerow(['Average Time to Answer - Overall (mm:ss)', ms_to_time_format(avg_overall_ms)])
        if all_text_times:
            avg_text_ms = sum(all_text_times) / len(all_text_times)
            writer.writerow(['Average Time to Answer - Text (mm:ss)', ms_to_time_format(avg_text_ms)])
        if all_audio_times:
            avg_audio_ms = sum(all_audio_times) / len(all_audio_times)
            writer.writerow(['Average Time to Answer - Audio (mm:ss)', ms_to_time_format(avg_audio_ms)])
        if all_text_times and all_audio_times:
            avg_text = sum(all_text_times) / len(all_text_times)
            avg_audio = sum(all_audio_times) / len(all_audio_times)
            diff_ms = avg_audio - avg_text
            writer.writerow(['Audio takes longer than Text by (mm:ss)', ms_to_time_format(diff_ms)])
            writer.writerow(['Audio/Text Time Ratio', round(avg_audio / avg_text, 2)])
        writer.writerow([])
        
        # Statistici tab changes
        if all_tab_changes:
            writer.writerow(['Average Tab Changes per User (Count)', round(sum(all_tab_changes) / len(all_tab_changes), 2)])
            writer.writerow(['Max Tab Changes (Count)', max(all_tab_changes)])
            writer.writerow(['Min Tab Changes (Count)', min(all_tab_changes)])
            writer.writerow(['Users with 0 Tab Changes (Count)', sum(1 for tc in all_tab_changes if tc == 0)])
            writer.writerow(['Users with Tab Changes (Count)', sum(1 for tc in all_tab_changes if tc > 0)])
        writer.writerow([])
        
        # Statistici răspunsuri
        if total_answered > 0:
            writer.writerow(['Total Answered Questions (Count)', total_answered])
        writer.writerow([])
        
        # Statistici timp petrecut
        if total_time_spent > 0:
            writer.writerow(['Total Time Spent by All Users (mm:ss)', seconds_to_time_format(total_time_spent)])
            avg_time = total_time_spent / submitted_count if submitted_count > 0 else 0
            writer.writerow(['Average Time Spent per User (mm:ss)', seconds_to_time_format(avg_time)])
    
    print(f'✅ Created {summary_path}')
    
    # 2. Creează users.csv cu date individuale pentru fiecare user
    users_path = os.path.join(output_dir, 'users.csv')
    with open(users_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'User ID', 
            'Email',
            'Status',
            'Total Questions (Count)',
            'Answered (Count)',
            'Unanswered (Count)',
            'Correct (Count)',
            'Wrong (Count)',
            'Text Answers (Count)', 
            'Audio Answers (Count)',
            'Average Time to Answer (mm:ss)',
            'Tab Changes (Count)',
            'Time Spent (mm:ss)',
            'Current Section',
            'Submission Time (Date/Time)'
        ])
        
        # Procesează fiecare user
        for user_id in sorted(exam_progress.keys()):
            user_data, is_submitted = get_user_complete_data(user_id, data)
            
            if not user_data:
                email = get_user_email(user_id, data)
                writer.writerow([
                    user_id,
                    email,
                    'No Data',
                    'N/A', 'N/A', 'N/A', '', '', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
                ])
                continue
            
            email = get_user_email(user_id, data)
            status = 'Submitted' if is_submitted else 'In Progress'
            
            # Calculează Total Questions și Unanswered
            total_questions = user_data.get('totalQuestions', 'N/A')
            answered_count = user_data.get('answeredCount', 0)
            unanswered = total_questions - answered_count if isinstance(total_questions, int) else 'N/A'
            
            # Contorizare răspunsuri
            answers = user_data.get('answers', {})
            
            text_answers = sum(1 for ans in answers.values() if 'text' in ans)
            audio_answers = sum(1 for ans in answers.values() if 'audioUrl' in ans)
            
            # Timp mediu de răspuns
            times = [ans.get('timeToAnswerMs', 0) for ans in answers.values() if 'timeToAnswerMs' in ans]
            avg_time_ms = sum(times) / len(times) if times else 0
            avg_time_formatted = ms_to_time_format(avg_time_ms) if times else 'N/A'
            
            # Tab changes
            tab_changes = user_data.get('tabChangeCount', 0)
            
            # Time spent
            time_spent = user_data.get('timeSpent', 0)
            time_spent_formatted = seconds_to_time_format(time_spent) if time_spent > 0 else 'N/A'
            
            # Secțiune curentă
            current_section = user_data.get('currentSection', 'N/A')
            
            # Submission time
            if 'timestamp' in user_data:
                submission_time = datetime.fromisoformat(user_data['timestamp'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
            else:
                submission_time = 'N/A'
            
            writer.writerow([
                user_id,
                email,
                status,
                total_questions,
                answered_count,
                unanswered,
                '',  # Correct - gol pentru completare manuală
                '',  # Wrong - gol pentru completare manuală
                text_answers,
                audio_answers,
                avg_time_formatted,
                tab_changes,
                time_spent_formatted,
                current_section,
                submission_time
            ])
    
    print(f'✅ Created {users_path}')


def main():
    """Funcție principală"""
    print('Loading data from final.json...')
    data = load_data()
    
    print('Loading questions map...')
    questions_map = load_questions()
    print(f'✅ Loaded {len(questions_map)} questions\n')
    
    print('\nGenerating individual user CSVs...')
    exam_progress = data.get('examProgress', {})
    
    for user_id in exam_progress.keys():
        create_user_csv(user_id, data, questions_map)
    
    print(f'\nTotal users processed: {len(exam_progress)}')
    
    print('\nGenerating statistics CSVs...')
    create_statistics_csv(data)
    
    print('\n✅ All CSVs generated successfully!')
    print(f'- Individual user CSVs: user_csvs/<user_id>/summary.csv and answers.csv')
    print(f'- General statistics: general_statistics/summary.csv and users.csv')

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()

# Script pentru calculul accuracy-ului pe user, doar pentru întrebări STANDARD
import csv
import os

def is_standard(qid):
    return 'standard' in qid

def process_user_answers(user_id, answers_path):
    text_right = text_wrong = audio_right = audio_wrong = 0
    with open(answers_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row['Question ID']
            if not is_standard(qid):
                continue
            answer_type = row['Answer Type'].strip()
            correct = row['Correct'].strip()
            wrong = row['Wrong'].strip()
            if answer_type == 'Text':
                if correct:
                    text_right += 1
                elif wrong:
                    text_wrong += 1
            elif answer_type == 'Audio':
                if correct:
                    audio_right += 1
                elif wrong:
                    audio_wrong += 1
    text_total = text_right + text_wrong
    audio_total = audio_right + audio_wrong
    text_acc = round(text_right / text_total, 3) if text_total else ''
    audio_acc = round(audio_right / audio_total, 3) if audio_total else ''
    return [user_id, text_right, text_wrong, text_acc, audio_right, audio_wrong, audio_acc]

def main():
    base = 'manual_corrected_csvs/user_csvs'
    out_csv = 'output/general_statistics/standard_accuracy_per_user.csv'
    user_dirs = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
    results = []
    for user_id in sorted(user_dirs):
        answers_path = os.path.join(base, user_id, 'answers.csv')
        if os.path.exists(answers_path):
            results.append(process_user_answers(user_id, answers_path))
    with open(out_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in results:
            writer.writerow(row)

if __name__ == '__main__':
    main()

import json
import re

def parse_exam_questions():
    """Parse examQuestions.ts și extrage textul întrebărilor"""
    
    with open('examQuestions.ts', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    questions = {}
    current_section = None
    current_question = None
    current_question_text = None
    current_tts_text = None
    
    for line in lines:
        # Detectează începutul unei secțiuni
        section_match = re.match(r'\s*(section\d+_\w+):\s*\{', line)
        if section_match:
            # Salvează întrebarea anterioară înainte de a schimba secțiunea
            if current_section and current_question and current_question_text:
                full_id = f"{current_section}_{current_question}"
                questions[full_id] = current_tts_text if current_tts_text else current_question_text
            
            current_section = section_match.group(1)
            current_question = None
            current_question_text = None
            current_tts_text = None
            continue
        
        # Detectează întrebare + question pe aceeași linie (format compact)
        inline_q_match = re.match(r'\s*(Q\d+):\s*\{.*question:\s*"([^"]+)".*(?:tts_text:\s*"([^"]+)")?', line)
        if inline_q_match and current_section:
            # Salvează întrebarea anterioară
            if current_question and current_question_text:
                full_id = f"{current_section}_{current_question}"
                questions[full_id] = current_tts_text if current_tts_text else current_question_text
            
            current_question = inline_q_match.group(1)
            current_question_text = inline_q_match.group(2)
            current_tts_text = inline_q_match.group(3) if inline_q_match.group(3) else None
            
            # Salvează imediat pentru format inline
            full_id = f"{current_section}_{current_question}"
            questions[full_id] = current_tts_text if current_tts_text else current_question_text
            current_question = None  # Reset pentru că am salvat deja
            continue
        
        # Detectează începutul unei întrebări (format multi-line)
        question_match = re.match(r'\s*(Q\d+):\s*\{', line)
        if question_match and current_section:
            # Salvează întrebarea anterioară dacă există
            if current_question and current_question_text:
                full_id = f"{current_section}_{current_question}"
                # Folosește tts_text dacă există, altfel question_text
                questions[full_id] = current_tts_text if current_tts_text else current_question_text
            
            # Resetează pentru noua întrebare
            current_question = question_match.group(1)
            current_question_text = None
            current_tts_text = None
            continue
        
        # Extrage textul întrebării
        if current_question:
            q_text_match = re.search(r'question:\s*"([^"]+)"', line)
            if q_text_match:
                current_question_text = q_text_match.group(1)
            
            tts_match = re.search(r'tts_text:\s*"([^"]+)"', line)
            if tts_match:
                current_tts_text = tts_match.group(1)
    
    # Nu uita să salvezi ultima întrebare
    if current_section and current_question and current_question_text:
        full_id = f"{current_section}_{current_question}"
        questions[full_id] = current_tts_text if current_tts_text else current_question_text
    
    return questions

if __name__ == '__main__':
    questions = parse_exam_questions()
    
    # Salvează într-un JSON pentru a fi folosit de generate_csv.py
    with open('questions_map.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Parsed {len(questions)} questions")
    print("\nSample questions:")
    for i, (qid, text) in enumerate(list(questions.items())[:5]):
        print(f"  {qid}: {text[:60]}...")

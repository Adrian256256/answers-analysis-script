import json
import re

# Parse the TypeScript file to extract questions
questions_map = {}

# Section 1 - Accommodation
questions_map['section1_accomodation_Q1'] = {
    'question': 'What is your age?',
    'type': 'blank'
}
questions_map['section1_accomodation_Q2'] = {
    'question': 'Choose what best describes you:',
    'type': 'multiple',
    'options': ['student', 'employee', 'working student', 'freelancer', 'entrepreneur', 'other']
}
questions_map['section1_accomodation_Q3'] = {
    'question': 'Record yourself answering the next audio question: What day is it today?',
    'type': 'audio',
    'tts_text': 'What day is it today?'
}
questions_map['section1_accomodation_Q4'] = {
    'question': 'Would you say you remember information better when you hear it or when you see it (for example, by reading or looking at images)?',
    'type': 'multiple',
    'options': ['I remember better when I read.', 'I remember better when I hear.']
}
questions_map['section1_accomodation_Q5'] = {
    'question': 'Can you remember what the first question was? Write it down.',
    'type': 'blank'
}

# Section 2 - Standard
section2_standard = {
    'Q1': {'question': 'How many bits are there in one byte?', 'answers': ['8', 'eight']},
    'Q2': {'question': 'Which type of memory is volatile and temporarily stores data during execution?', 'answers': ['RAM', 'Random Access Memory']},
    'Q3': {'question': 'Which component performs arithmetic and logical operations?', 'answers': ['ALU', 'Arithmetic Logic Unit']},
    'Q4': {'question': 'Which device forwards packets based on IP addresses?', 'answers': ['Router']},
    'Q5': {'question': 'Which logic gate outputs true only when all inputs are true?', 'answers': ['AND', 'AND gate']},
    'Q6': {'question': 'Which layer of the OSI model handles routing and IP addressing?', 'answers': ['Network layer']},
    'Q7': {'question': 'Which protocol is used for secure file transfer over SSH?', 'answers': ['SFTP', 'Secure File Transfer Protocol']},
    'Q8': {'question': 'Which port number is used by HTTP?', 'answers': ['80']},
    'Q9': {'question': 'Which data structure uses hierarchical parent-child relationships?', 'answers': ['Tree']},
    'Q10': {'question': 'Which SQL clause filters query results?', 'answers': ['WHERE']},
    'Q11': {'question': 'Which component controls data flow within the CPU?', 'answers': ['Control Unit']},
    'Q12': {'question': 'What is the Big O time complexity of linear search?', 'answers': ['O(n)']}
}

for q_id, q_data in section2_standard.items():
    questions_map[f'section2_standard_{q_id}'] = {
        'question': q_data['question'],
        'type': 'blank',
        'correct_answers': q_data['answers']
    }

# Section 2 - Control
section2_control = {
    'Q1': {'question': 'Which number system uses base 2?', 'answers': ['Binary']},
    'Q2': {'question': 'Which type of memory retains data even when power is off?', 'answers': ['ROM', 'Read Only Memory']},
    'Q3': {'question': 'What does the acronym ISA stand for?', 'answers': ['Instruction Set Architecture']},
    'Q4': {'question': 'Which device connects computers within the same network using MAC addresses?', 'answers': ['Switch']},
    'Q5': {'question': 'Which logic gate outputs the opposite of its input?', 'answers': ['NOT', 'NOT gate']},
    'Q6': {'question': 'Which OSI layer ensures reliable data delivery?', 'answers': ['Transport layer']},
    'Q7': {'question': 'Which protocol secures web communication?', 'answers': ['HTTPS']},
    'Q8': {'question': 'Which port number is used by HTTPS?', 'answers': ['443']},
    'Q9': {'question': 'Which data structure uses nodes connected by edges?', 'answers': ['Graph']},
    'Q10': {'question': 'Which command in SQL removes all table data but keeps the structure?', 'answers': ['TRUNCATE']},
    'Q11': {'question': 'Which CPU part temporarily stores instructions and data?', 'answers': ['Cache']},
    'Q12': {'question': 'What is the Big O time complexity of binary search?', 'answers': ['O(log n)', 'O(logn)']}
}

for q_id, q_data in section2_control.items():
    questions_map[f'section2_control_{q_id}'] = {
        'question': q_data['question'],
        'type': 'blank',
        'correct_answers': q_data['answers']
    }

# Section 3 - Standard (Audio)
section3_standard = {
    'Q1': {'tts': 'What does the acronym D R A M stand for?', 'answers': ['Dynamic Random Access Memory']},
    'Q2': {'tts': 'What does the acronym M A C stand for?', 'answers': ['Media Access Control']},
    'Q3': {'tts': 'Which software manages computer hardware?', 'answers': ['Operating system', 'OS']},
    'Q4': {'tts': 'What does the acronym W A N stand for?', 'answers': ['Wide Area Network']},
    'Q5': {'tts': 'Which programming language keyword is used to create an object in C++?', 'answers': ['new']},
    'Q6': {'tts': 'Which OOP concept allows the same method name with different parameters?', 'answers': ['Overloading', 'Function overloading']},
    'Q7': {'tts': 'Which OOP concept hides implementation details from users?', 'answers': ['Encapsulation']},
    'Q8': {'tts': 'Which Linux command changes the current directory?', 'answers': ['cd']},
    'Q9': {'tts': 'Which data structure operates on a First In First Out basis?', 'answers': ['Queue']},
    'Q10': {'tts': 'Which scheduling algorithm executes the shortest job next?', 'answers': ['Shortest Job First', 'SJF']},
    'Q11': {'tts': 'Which sorting algorithm builds the final sorted array one item at a time?', 'answers': ['Insertion Sort']},
    'Q12': {'tts': 'Which algorithm finds the shortest path in a weighted graph?', 'answers': ["Dijkstra's algorithm", 'Dijkstra algorithm']}
}

for q_id, q_data in section3_standard.items():
    questions_map[f'section3_standard_{q_id}'] = {
        'question': 'Record yourself answering the next audio question: ' + q_data['tts'],
        'tts_text': q_data['tts'],
        'type': 'audio',
        'correct_answers': q_data['answers']
    }

# Section 3 - Control (Audio)
section3_control = {
    'Q1': {'tts': 'What does the acronym S R A M stand for?', 'answers': ['Static Random Access Memory']},
    'Q2': {'tts': 'What does the acronym V P N stand for?', 'answers': ['Virtual Private Network']},
    'Q3': {'tts': 'Which type of software translates high-level code to machine code?', 'answers': ['Compiler']},
    'Q4': {'tts': 'What does the acronym L A N stand for?', 'answers': ['Local Area Network']},
    'Q5': {'tts': 'Which keyword is used to destroy an object in C++?', 'answers': ['delete']},
    'Q6': {'tts': 'Which OOP concept allows subclasses to reuse parent methods?', 'answers': ['Inheritance']},
    'Q7': {'tts': 'Which OOP concept allows one interface to be used for different data types?', 'answers': ['Polymorphism']},
    'Q8': {'tts': 'Which command in Linux lists files and directories?', 'answers': ['ls']},
    'Q9': {'tts': 'Which data structure operates on a Last In First Out basis?', 'answers': ['Stack']},
    'Q10': {'tts': 'Which scheduling algorithm gives equal CPU time to all processes?', 'answers': ['Round Robin']},
    'Q11': {'tts': 'Which algorithm uses divide and conquer for sorting?', 'answers': ['Merge Sort']},
    'Q12': {'tts': 'Which algorithm uses a greedy approach to find the minimum spanning tree?', 'answers': ["Prim's algorithm", 'Prim algorithm']}
}

for q_id, q_data in section3_control.items():
    questions_map[f'section3_control_{q_id}'] = {
        'question': 'Record yourself answering the next audio question: ' + q_data['tts'],
        'tts_text': q_data['tts'],
        'type': 'audio',
        'correct_answers': q_data['answers']
    }

# Load the simplified JSON with transcriptions
with open('simplified_exam_data_with_transcriptions.json', 'r') as f:
    data = json.load(f)

# Add question text to each answer
added_count = 0
for user in data['users']:
    for answer in user['answers']:
        question_id = answer['question_id']
        if question_id in questions_map:
            q_info = questions_map[question_id]
            answer['question_text'] = q_info['question']
            answer['question_type'] = q_info['type']
            if 'tts_text' in q_info:
                answer['question_tts_text'] = q_info['tts_text']
            if 'correct_answers' in q_info:
                # Only add if not already present
                if 'expected_answers' not in answer or not answer['expected_answers']:
                    answer['expected_answers'] = q_info['correct_answers']
            added_count += 1

# Save the updated JSON
output_file = 'simplified_exam_data_with_questions.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added question texts to {added_count} answers")
print(f"Updated data saved to: {output_file}")
print(f"\nEach answer now contains:")
print(f"  - question_text: The full question text")
print(f"  - question_type: blank, audio, or multiple")
print(f"  - question_tts_text: Audio question text (for audio questions)")
print(f"  - expected_answers: Correct answers (when available)")

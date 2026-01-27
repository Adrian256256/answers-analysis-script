# Manual Grading Reference Guide

This folder contains manually corrected CSV files with verified transcriptions and grading.

## Excluded Users

The following users have been excluded from the statistics analysis:

| User ID | Reason | Details |
|---------|--------|---------|
| `yskSrWOMY1dMfleJ1demTFRwmaB3` | Too many tab changes | 14 tab changes - possible cheater |
| `kzHpKFHMcPPnV8KAKZX4skbzRlM2` | Too many tab changes | 11 tab changes - possible cheater |
| `dwtLwhIgAyQAfqgq6BGgRYDqwdi2` | Too many tab changes | 8 tab changes - possible cheater |
| `I95XongADMhnGoykzUkcFxfx2Zg1` | Incomplete answers | In progress / only accommodation questions |
| `2jx38lBdkJZAffOTjapIJUOkcmT2` | Incomplete answers | In progress / only accommodation questions |

**Total users analyzed:** 15 out of 20 (5 excluded)

---

## Impact of Exclusions

Statistics comparison before and after excluding the 5 users:

### Users
- **Total:** 20 → 15 (-5 excluded users)
- **Submitted:** 16 → 13
- **In Progress:** 4 → 2

### Answers
- **Total:** 325 → 283 (-42)
- **Text:** 222 → 188 (-34)
- **Audio:** 103 → 95 (-8)

### Accuracy
- **Overall:** 78.86% → 76.85%
- **Text:** 80.52% → 78.79%
- **Audio:** 76.09% → 73.81%
- **Gap (Text vs Audio):** 4.43% → 4.98%

### Tab Changes
- **Average:** 3.05 → 1.33 (dramatic decrease!)
- **Maximum:** 14 → 6 (removed user with 14 tab changes)
- **Users with 0 tabs:** 10 → 9
- **Users with tabs:** 9 → 6

---

## Correct Answers Reference

Use this guide to grade student answers in the CSV files.

### Section 1: Accommodation Questions

| Question ID | Question | Correct Answer(s) |
|------------|----------|-------------------|
| `section1_accomodation_Q1` | What is your age? | Any number (e.g., 18-25) |
| `section1_accomodation_Q2` | Choose what best describes you | Student / Working student / Working / Other |
| `section1_accomodation_Q3` | What day is it today? | Sunday (4th January 2026) |
| `section1_accomodation_Q4` | Remember information better when you hear or see it? | "I remember better when I read" / "I remember better when I hear" |
| `section1_accomodation_Q5` | What was the first question? | "What is your age?" / "Age" |

---

### Section 2: Written Questions (Standard)

| Question ID | Question | Correct Answer(s) |
|------------|----------|-------------------|
| `section2_standard_Q1` | How many bits in one byte? | 8 / Eight |
| `section2_standard_Q2` | Volatile memory that stores data during execution? | RAM / Random Access Memory |
| `section2_standard_Q3` | Component that performs arithmetic/logical operations? | ALU / Arithmetic Logic Unit |
| `section2_standard_Q4` | Device that forwards packets based on IP addresses? | Router |
| `section2_standard_Q5` | Logic gate that outputs true when all inputs are true? | AND / AND gate |
| `section2_standard_Q6` | OSI layer that handles routing and IP addressing? | Network layer / Layer 3 |
| `section2_standard_Q7` | Protocol for secure file transfer over SSH? | SFTP / SCP |
| `section2_standard_Q8` | Port number used by HTTP? | 80 / Port 80 |
| `section2_standard_Q9` | Data structure with hierarchical parent-child relationships? | Tree |
| `section2_standard_Q10` | SQL clause that filters query results? | WHERE |
| `section2_standard_Q11` | Component that controls data flow within CPU? | Control Unit / CU |
| `section2_standard_Q12` | Big O time complexity of linear search? | O(n) / Linear |

---

### Section 2: Written Questions (Control)

| Question ID | Question | Correct Answer(s) |
|------------|----------|-------------------|
| `section2_control_Q1` | Number system using base 2? | Binary |
| `section2_control_Q2` | Memory that retains data without power? | ROM / Non-volatile memory / Flash |
| `section2_control_Q3` | What does ISA stand for? | Instruction Set Architecture |
| `section2_control_Q4` | Device connecting computers using MAC addresses? | Switch |
| `section2_control_Q5` | Logic gate that outputs opposite of input? | NOT / NOT gate / Inverter |
| `section2_control_Q6` | OSI layer ensuring reliable data delivery? | Transport layer / Layer 4 |
| `section2_control_Q7` | Protocol that secures web communication? | HTTPS / TLS / SSL |
| `section2_control_Q8` | Port number used by HTTPS? | 443 / Port 443 |
| `section2_control_Q9` | Data structure with nodes connected by edges? | Graph |
| `section2_control_Q10` | SQL command removing all data but keeping structure? | TRUNCATE |
| `section2_control_Q11` | CPU part storing instructions and data temporarily? | Cache / Register |
| `section2_control_Q12` | Big O time complexity of binary search? | O(log n) / Logarithmic |

---

### Section 3: Audio Questions (Standard)

| Question ID | Question | Correct Answer(s) |
|------------|----------|-------------------|
| `section3_standard_Q1` | What does DRAM stand for? | Dynamic Random Access Memory |
| `section3_standard_Q2` | What does MAC stand for? | Media Access Control / Medium Access Control |
| `section3_standard_Q3` | Software that manages computer hardware? | Operating System / OS / Kernel |
| `section3_standard_Q4` | What does WAN stand for? | Wide Area Network |
| `section3_standard_Q5` | Keyword to create object in C++? | new |
| `section3_standard_Q6` | OOP concept: same method name, different parameters? | Overloading / Method Overloading / Function Overloading |
| `section3_standard_Q7` | OOP concept that hides implementation details? | Encapsulation / Abstraction |
| `section3_standard_Q8` | Linux command to change directory? | cd |
| `section3_standard_Q9` | Data structure operating on FIFO basis? | Queue |
| `section3_standard_Q10` | Scheduling algorithm executing shortest job next? | SJF / Shortest Job First / Shortest Job Next |
| `section3_standard_Q11` | Sorting building final array one item at a time? | Insertion Sort |
| `section3_standard_Q12` | Algorithm finding shortest path in weighted graph? | Dijkstra / Dijkstra's Algorithm |

---

### Section 3: Audio Questions (Control)

| Question ID | Question | Correct Answer(s) |
|------------|----------|-------------------|
| `section3_control_Q1` | What does SRAM stand for? | Static Random Access Memory |
| `section3_control_Q2` | What does VPN stand for? | Virtual Private Network |
| `section3_control_Q3` | Software translating high-level code to machine code? | Compiler |
| `section3_control_Q4` | What does LAN stand for? | Local Area Network |
| `section3_control_Q5` | Keyword to destroy object in C++? | delete / destructor |
| `section3_control_Q6` | OOP concept: subclasses reuse parent methods? | Inheritance |
| `section3_control_Q7` | OOP concept: one interface for different data types? | Polymorphism |
| `section3_control_Q8` | Linux command listing files and directories? | ls |
| `section3_control_Q9` | Data structure operating on LIFO basis? | Stack |
| `section3_control_Q10` | Scheduling giving equal CPU time to all processes? | Round Robin / RR |
| `section3_control_Q11` | Algorithm using divide and conquer for sorting? | Merge Sort / Quick Sort |
| `section3_control_Q12` | Greedy algorithm for minimum spanning tree? | Prim / Prim's Algorithm / Kruskal / Kruskal's Algorithm |

---

## Grading Guidelines

### Marking Answers

1. **Correct Column**: Mark with `✓` or `1` if the answer is correct
2. **Wrong Column**: Mark with `✗` or `1` if the answer is incorrect
3. **Partial Credit**: For close answers (e.g., minor spelling errors in technical terms), use judgment

### Common Issues to Watch For

#### Audio Transcription Errors
- **"Queue" vs "Cue"**: Should be Queue (data structure)
- **"Stack" vs "Stick"**: Should be Stack
- **"Merge Sort" vs "March Sort"**: Should be Merge Sort
- **"Destructor" vs "Destructer"**: Should be Destructor
- **"Dijkstra" vs "Destra/Dextra"**: Should be Dijkstra
- **"Greedy" vs "Gritty"**: Should be Greedy
- **"Inheritance" vs "Inferitance"**: Should be Inheritance
- **"Wide Area Network" vs "White Area Network"**: Should be Wide
- **"Hip Sort" vs "Heap Sort"**: Should be Heap Sort

#### Acceptable Variations
- Capitalization differences (e.g., "ram" vs "RAM")
- With/without spaces in acronyms (e.g., "W A N" vs "WAN")
- Full vs abbreviated answers (e.g., "Dynamic Random Access Memory" vs "DRAM")
- Minor punctuation differences

#### Unacceptable Answers
- Completely wrong technical terms
- "I don't know" or silence
- Unrelated responses
- Repetitive or corrupted transcriptions (e.g., "March, March, March...")

### Workflow

1. **Open** each user's `answers.csv` in this folder
2. **Compare** each transcription/answer with the reference table above
3. **Correct** any transcription errors in the "Transcription (Audio Answers)" column
4. **Mark** correct/wrong in the respective columns
5. **Count** total correct/wrong answers
6. **Update** the user's `summary.csv` with the totals
7. **Update** `general_statistics/users.csv` with all users' totals

---

## Notes

- Audio questions may have transcription errors - listen to audio files if unsure
- Some questions accept multiple correct answers (see table)
- For subjective questions (Section 1), evaluate reasonableness
- Technical term spelling should be exact for full credit
- Document any edge cases or questionable grading decisions

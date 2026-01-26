#!/bin/bash
# Helper script to run the analysis scripts

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}===================================${NC}"
echo -e "${BLUE}Exam Answers Analysis Script${NC}"
echo -e "${BLUE}===================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}Virtual environment created!${NC}"
    echo ""
fi

# Activate virtual environment
source .venv/bin/activate

# Show menu
echo "What would you like to do?"
echo ""
echo "1) Parse questions from examQuestions.ts"
echo "2) Transcribe audio files"
echo "3) Generate CSV reports"
echo "4) Re-transcribe audio with better accuracy"
echo "5) Run full pipeline (transcribe + generate CSVs)"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo -e "\n${GREEN}Parsing questions...${NC}"
        cd scripts && python3 parse_questions.py
        ;;
    2)
        echo -e "\n${GREEN}Transcribing audio files...${NC}"
        cd scripts && python3 transcribe_audio.py
        ;;
    3)
        echo -e "\n${GREEN}Generating CSV reports...${NC}"
        cd scripts && python3 generate_csv.py
        ;;
    4)
        echo -e "\n${GREEN}Re-transcribing audio files...${NC}"
        cd scripts && python3 retranscribe_audio.py
        ;;
    5)
        echo -e "\n${GREEN}Running full pipeline...${NC}"
        cd scripts
        echo -e "\n${BLUE}Step 1/2: Transcribing audio files...${NC}"
        python3 transcribe_audio.py
        echo -e "\n${BLUE}Step 2/2: Generating CSV reports...${NC}"
        python3 generate_csv.py
        echo -e "\n${GREEN}Full pipeline complete!${NC}"
        ;;
    *)
        echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"

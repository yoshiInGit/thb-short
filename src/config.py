import os

# ===== Directory Settings =====
OUTPUT_DIR = "output"
INTERMEDIATE_DIR = os.path.join(OUTPUT_DIR, "intermediate")
LOG_DIR = "logs"
PROMPT_DIR = "prompts"

# ===== File Paths =====
# Intermediate Data
MAKE_SCRIPT_JSON = os.path.join(INTERMEDIATE_DIR, "make_script.json")
ADD_CHARACTER_JSON = os.path.join(INTERMEDIATE_DIR, "add_character.json")
COEROINK_JSON = os.path.join(INTERMEDIATE_DIR, "coeroink.json")
VOICE_DATA_JSON = os.path.join(INTERMEDIATE_DIR, "voice_data.json")
IMG_REQUEST_JSON = os.path.join(INTERMEDIATE_DIR, "img_request.json")

# Final Outputs
COEROINK_TXT = os.path.join(OUTPUT_DIR, "coeroink.txt")
IMG_REQUEST_TXT = os.path.join(OUTPUT_DIR, "img_request.txt")

# Dummy Data Directory (relative to src)
DUMMY_DIR_NAME = "dummy"

# ===== Model Settings =====
DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"
DEFAULT_TEMPERATURE = 0.7
COEROINK_TEMPERATURE = 0.2

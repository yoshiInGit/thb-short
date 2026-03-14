import os

# ===== Directory Settings =====
OUTPUT_DIR = "output"
INTERMEDIATE_DIR = os.path.join(OUTPUT_DIR, "intermediate")
LOG_DIR = "logs"
PROMPT_DIR = "prompts"
VOICE_DIR = "input/voice"

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
OUTPUT_VOICE = os.path.join(OUTPUT_DIR, "voice.wav")

# Dummy Data Directory (relative to src)
DUMMY_DIR_NAME = "dummy"

# ===== Model Settings =====
DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"
DEFAULT_TEMPERATURE = 0.7
COEROINK_TEMPERATURE = 0.2

# ===== Subtitle Configurations =====
RESOLUTION = (1080, 1920)
BG_COLOR = (0, 255, 0) # Green back
FPS = 24
OUTPUT_MP4 = os.path.join(OUTPUT_DIR, "subtitle.mp4")

# Text Configuration
FONT_SIZE = 72
FONT_COLOR = "white"
STROKE_COLOR = "black"
STROKE_WIDTH = 3
FONT_NAME = "assets/font/LINESeedJP-Bold.ttf" 
WRAP_WIDTH = 12  # 1行あたりの最大文字数
TEXT_POS = ('center', 580)
TRANSITION_DURATION = 0.2  # フェードイン・アウトの時間(秒)
SILENCE_DURATION_MS = 250  # 句読点後の無音時間

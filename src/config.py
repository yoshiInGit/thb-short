import os

# ===== Directory Settings =====
# src/ ディレクトリの絶対パスを取得
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
INTERMEDIATE_DIR = os.path.join(OUTPUT_DIR, "intermediate")
LOG_DIR = os.path.join(BASE_DIR, "logs")
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")
VOICE_DIR = os.path.join(INPUT_DIR, "voice")

# ===== File Paths =====
TRIVIA_INPUT_PATH = os.path.join(INPUT_DIR, "trivia.txt")
# Intermediate Data
MAKE_SCRIPT_JSON = os.path.join(INTERMEDIATE_DIR, "make_script.json")
ADD_CHARACTER_JSON = os.path.join(INTERMEDIATE_DIR, "add_character.json")
COEROINK_JSON = os.path.join(INTERMEDIATE_DIR, "coeroink.json")
VOICE_DATA_JSON = os.path.join(INTERMEDIATE_DIR, "voice_data.json")
IMG_REQUEST_JSON = os.path.join(INTERMEDIATE_DIR, "img_request.json")
SLIDE_IMGS_JSON = os.path.join(INTERMEDIATE_DIR, "slide_imgs.json")

# Final Outputs
COEROINK_TXT = os.path.join(OUTPUT_DIR, "coeroink.txt")
IMG_REQUEST_TXT = os.path.join(OUTPUT_DIR, "img_request.txt")
SLIDE_IMGS_DIR = os.path.join(OUTPUT_DIR, "slide_imgs")
OUTPUT_VOICE = os.path.join(OUTPUT_DIR, "voice.wav")

# API Keys
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "DUMMY_KEY")

# Dummy Data Directory (relative to src)
DUMMY_DIR_NAME = "dummy"

# ===== Model Settings =====
DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"
DEFAULT_TEMPERATURE = 0.7
COEROINK_TEMPERATURE = 0.2

# ===== Prompt Settings =====
MAKE_SCRIPT_PROMPT_FILE = "story_make_script.txt"
MAKE_SCRIPT_VERIFY_PROMPT_FILE = "story_make_script_verify.txt"
ADD_CHARACTER_SCRIPT_PROMPT_FILE = "add_character_script.txt"
OUTPUT_COEROINK_TXT_PROMPT_FILE = "output_coeroink_txt.txt"
GENERATE_IMG_REQUEST_PROMPT_FILE = "generate_img_request.txt"

# ===== Subtitle Configurations =====
RESOLUTION = (1920, 330)
BG_COLOR = (255, 255, 255) # White
FPS = 24
OUTPUT_MP4 = os.path.join(OUTPUT_DIR, "subtitle.mp4")
SLIDESHOW_RESOLUTION = (1920, 1080)
SLIDESHOW_OUTPUT_MP4 = os.path.join(OUTPUT_DIR, "slides.mp4")
SLIDESHOW_FADE_DURATION = 0.3
FINAL_VIDEO_OUTPUT_MP4 = os.path.join(OUTPUT_DIR, "final_video.mp4")

# Text Configuration
FONT_SIZE = 42
FONT_COLOR = "white"
STROKE_COLOR = "black"
STROKE_WIDTH = 8
FONT_NAME = "assets/font/LINESeedJP-Bold.ttf" 
WRAP_WIDTH = 12  # 1行あたりの最大文字数
TEXT_POS = (440, 'center')
TEXT_MARGIN_RIGHT = 40  # 右端の余白
TRANSITION_DURATION = 0.2  # フェードイン・アウトの時間(秒)
SILENCE_DURATION_MS = 350  # 句読点後の無音時間

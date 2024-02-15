from typing import Final

# AI
KNOWLEDGE_DIR: Final[str] = "/Users/MingYuan/Development/capy/copilot/knowledge_dir"
SYSTEM_INSTRUCT_PATH: Final[str] = "/Users/MingYuan/Development/capy/copilot/prompt_v1.txt"

# MODEL
QUESTION_AUGMENTATION_PATH: Final[
    str
] = "/Users/MingYuan/Development/capy/copilot/question_augmentation_v1.txt"
GPT_MODEL: Final[str] = "gpt-4-turbo-preview"
MAX_CONTEXT_LEN=2500
MAX_TOKENS=2500
REDIS_KEY_PREFIX="capy_copilot"

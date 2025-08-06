from agent import AsyncOpenAI, set_tracing_disabled, set_tracing_disabled
import os
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(True)

gemini_api_key=os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)
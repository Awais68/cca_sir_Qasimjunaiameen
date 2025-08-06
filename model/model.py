from agent import OpenAIChatCompletionsModel, AsyncOpenAI
from provider.provider import provider

model = OpenAIChatCompletionsModel(
    openai_client= provider,
    model= "gemini-2.0-flash"
)
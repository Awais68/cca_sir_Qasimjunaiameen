from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging, ModelSettings, RunContextWrapper
from agents.agent import StopAtTools
import os 
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()

enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
gemini_api_key=os.getenv("GEMINI_API_KEY")


@dataclass
class User:
    name: str
    phone: str
    current_conversation: list[str]

    def get_memory(self):
        return f"User {self.name} has a phone number {self.phone}"
    def update_memory(self, memory: str):
        self.memory = memory 

    def update_conversation(self, message: str):
        self.current_conversation.append(message)
# class 
# dataclass, class, pydantic class, typeClass


# async def get_system_prompt(ctx: RunContextWrapper[User], start_agent: Agent):
#     print("\n[Context]==>", ctx.context)
#     print("\n[agent]==>", start_agent)

#     # ctx.context.update_memory(f"User {ctx.context.name} has a phone number {ctx.context.phone}")
#     ctx.context.update_conversation(f"User {ctx.context.name} has a phone number {ctx.context.phone}")
#     return f"Your are a helpful assistant that can answer questions and help with tasks. {ctx.context.get_memory()}"

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider   
)
async def is_weather_enabled(ctx:RunContextWrapper, start_agent: Agent):
    if ctx.context.get("User_type", "basic") == "basic":
        return False
    return True

@function_tool(is_enabled=True)
def get_weather(city: str) -> str:
    """returns weather info for the specified city."""
    return f"The weather in {city} is sunny"
# @function_tool
# def get_support_details(city: str) -> str:
#     #  """returns weather info for the specified city."""
#     return f"The support details for {city} are : 1234567890"
# @function_tool
# def get_weather_in_karachi(city: str) -> str:
#     #  """returns weather info for the specified city."""
#     return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="help user",
    # instructions="Always respond in haiku form",
    model=model,
    tools=[get_weather ],
    # model_settings=ModelSettings(parallel_tool_calls=False),
    # tool_use_behavior=StopAtTools(stop_at_tool_names=["get_support_details"]),
    # reset_tool_choice=True
)

# user_1  = User(name="Awais Niaz", phone= "0335-2204606", current_conversation=[])

result = Runner.run_sync(agent, "what is the weather of karachi?")
print("\n[result.final_output]")
print(result.final_output)

# print("\n[user_1.get_memory)]")
# print(user_1.get_memory)
# print("\n[user_1.current_conversation)]")
# print(user_1.current_conversation)
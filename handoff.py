import asyncio
from agents import Agent, Runner, AsyncOpenAI, handoff,  OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, enable_verbose_stdout_logging, ModelSettings, RunContextWrapper
import os 
from dotenv import load_dotenv
from agents.extensions import handoff_filters
from pydantic import BaseModel

class Currentuser(BaseModel):
    is_logged_in:bool

load_dotenv()
#
# enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)
gemini_api_key=os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider   
)


# billing_agent = Agent(name="Billing agent", model=model)
refund_agent = Agent(name="Refund agent", model=model)

async def decide_refund_customer(local_context: RunContextWrapper[Currentuser], agent: Agent[Currentuser]) -> bool:
    print("local_Context", local_context.context)
    if local_context.context and  local_context.context.is_logged_in:
        return True
    return False



general_agent = Agent(name="General agent", model=model, 
                      handoffs=[handoff(agent=refund_agent, 
                    #   tool_name_override="refund_order", 
                    #   tool_description_override="Handsles all refund the order ",
                    #   input_filter=handoff_filters.remove_all_tools,
                      is_enabled=decide_refund_customer)])
# Summery delegate ho 
# main agent se refund agent  k pass jb handoff ho to history bana kr pass kre ga as it is pass nh kre ga summery bana kr bheje 
# Task 02  summary aye yahan pr or ye jae dusre agent k pass input_filler

async def main():
    current_user = Currentuser(is_logged_in=True)
    result = await Runner.run(
        general_agent,
        "i want refund my order id: 1234567890",
        context=current_user
        # "hi"
    )
    print(result.final_output)
    print("last Agent==>>>>", result.last_agent)


if __name__=="__main__":
    asyncio.run(main())

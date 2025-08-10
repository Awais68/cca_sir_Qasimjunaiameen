import asyncio
import os

from dotenv import load_dotenv, find_dotenv

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.run import AgentRunner, set_default_agent_runner

_ = load_dotenv(find_dotenv())

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

class CustomAgentRunner(AgentRunner):
    async def run(self, starting_agent, input, **kwargs):
        # Custom preprocessing
        
        # Call parent with custom logic
        return await super().run(starting_agent, input, **kwargs)
        # print(f"=== I'm in our custom runner run method====>")
        # input = await self.preprocess(input)
        
        # Call parent with custom logic
        # result = await super().run(starting_agent, input, **kwargs)
        
        # Custom postprocessing & analytics
        # await self.log_analytics(result)
        return "Mock Data"

set_default_agent_runner(CustomAgentRunner())
# low  level: functional -> async function : High level = function_tool

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in english.",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        
    )

    result = await Runner.run(
        agent,
        "Recursion method in Programming?.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
    

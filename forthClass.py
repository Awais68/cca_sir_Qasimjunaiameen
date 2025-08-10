from __future__ import annotations
import asyncio
from agents import Agent, Runner,AsyncOpenAI, OpenAIChatCompletionsModel, ItemHelpers, TResponseInputItem, trace, set_tracing_disabled
import os 
from dotenv import load_dotenv
from agents.extensions import handoff_filters
from dataclasses import dataclass
from typing import Literal 



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

"""This example shows the LLM AS A JUDGE pattern. The first agent generates an outline for a story.
The Second agent judges the outline and provides feedback. we loop until the judge is satisfied with the outline.
"""
story_outline_generator = Agent(
    name="story_outline_generator",
    instructions=("You generate a very short story outline based on the user's input."
                  "If there is any feedback privided, use it to improve the outline."
                  ),
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider),
)    
@dataclass
class EvaluationFeedback:
    feedback: str
    score: Literal["pass", "need_improvement", "fail"]

evaluator = Agent[None](
    name="evaluator",
    instructions=(
        "you evalutate a story outline and decide if it's good enough."
        "If it's not good enough, you provide feedback on what needs to be imporved."
        "Never give it a pass on the first try. After 3 attempts, you can give it a pass if story outline is good enough"
    ),
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider),
    output_type=EvaluationFeedback,
)

async def main() -> None:
    msg = input("What kind of story would you like to hear?")
    input_items: list[TResponseInputItem] = [{"content": msg, "role": "user"}]
    
    latest_outline: str | None = None
    # We'll  run the entire workflow in a single trace 
    with trace("LLM AS A  judge"):
        while True:
            story_outline_result = await Runner.run(
                story_outline_generator,
                input_items,
            )
            
            input_items = story_outline_result.to_input_list()
            latest_outline = ItemHelpers.text_message_outputs(story_outline_result.new_items)
            print("Stroy outline Generated")
            
            evaluator_result = await Runner.run(evaluator, input_items)
            result: EvaluationFeedback = evaluator_result.final_output
            
            print(f"Evaluator score: {result.score}")
            
            if  result.score == "pass":
                print("Story outline is good enough, exiting.")
                break
            print("Re-running with feedback")
            
            input_items.append({"content": f"Feedback: {result.feedback}", "role": "user"})
            
    print(f"Final story ouline: {latest_outline}")
            
            
if __name__=="__main__":
    asyncio.run(main())
    
    
# 1: 12 Fourth class
            
    
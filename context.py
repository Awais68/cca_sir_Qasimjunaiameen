# from agents import Runner, set_tracing_disabled, AsyncOpenAI, OpenAIChatCompletionsModel 
# from my_agent.my_Agents import assistant
# import os 
# from dotenv import load_dotenv
# set_tracing_disabled(True)
# load_dotenv()

# # enable_verbose_stdout_logging()
# set_tracing_disabled(disabled=True)
# gemini_api_key=os.getenv("GEMINI_API_KEY")

# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
# )
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider   
# )


# res = Runner.run_sync(
#     starting_agent=assistant,
#     input = "What is user Age?",
#     context="Aman Lal"
# )

# print(res.final_output)
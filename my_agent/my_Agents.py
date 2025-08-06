from agents import function_tool

@function_tool
def get_age(ctx):
    """"Age function tool"""
    print("age Toool======>")
    print("ctx======>", ctx)
    return f"Your age is 35." 
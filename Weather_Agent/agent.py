from dotenv import load_dotenv
import requests
import json
import subprocess
from pydantic import BaseModel, Field
from typing import Optional
import os
from openai import OpenAI

# Commands from run_cmd run here so mkdir / paths match this project folder,
# not wherever you launched python from.
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)

def run_cmd(cmd: str):
    proc = subprocess.run(
        cmd,
        shell=True,
        cwd=AGENT_DIR,
        capture_output=True,
        text=True,
    )
    parts = [f"exit_code={proc.returncode}"]
    if proc.stdout:
        parts.append(f"stdout:\n{proc.stdout.rstrip()}")
    if proc.stderr:
        parts.append(f"stderr:\n{proc.stderr.rstrip()}")
    return "\n".join(parts)

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong..."

available_tools = {
    "get_weather": get_weather,
    "run_cmd": run_cmd,
}

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of though.
    You work on START, PLAN, OBSERVE, TOOL and OUTPUT steps.
    You need to first plan what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN is done, you need to generate an output.
    You can also call a tool if required from the list of available tools.
    For every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly follow the given JSON output format
    - Only run one step at a time
    - The Sequence of step is START (where user gives an i/p), PLAN (That can be multiple times) and Output is the result.
    - ALWAYS output a SINGLE JSON object. 
    - Do NOT wrap the object in a list [].

    Output JSON format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL" , "content": "string", "tool": "string", "input": "string"}

    Available Tools:
    - get_weather(city: str) : Takes city name as input string and returns the weather
    - run_cmd(cmd: str) : Takes a system linux command as string and executes the command on user's system and returns the output from that command

    Example:
    START: What is the weather in Delhi?
    PLAN: {"step": "PLAN": "content": "Seems like user is interested in weather of Delhi"}
    PLAN: {"step": "PLAN": "content": "Lets see if there are any available tools to get weather info"}
    PLAN: {"step": "PLAN": "content": "Great, we have get_weather tool available for this"}
    PLAN: {"step": "PLAN": "content": "I need to call get_weather tool for Delhi as input city"}
    PLAN: {"step": "TOOL": "tool": "get_weather", "input": "Delhi"}
    PLAN: {"step": "OBSERVE": "tool": "get_weather", "output": "weather of Delhi is currently cloudy with 10 C"}
    PLAN: {"step": "PLAN": "content": "Great, I've got the weather info for delhi"}
    PLAN: {"step": "OUTPUT": "content": "current weather in Delhi is 20"}

"""
class MyOutputFormat(BaseModel):
    step: str = Field(...,description="The ID of the step. Example: PLAN, OUTPUT")
    content: Optional[str] = Field(None, description = "The optional string content")
    tool: Optional[str] = Field(None, description = "The ID of the tool to call")
    input: Optional[str] = Field(None, description = "The input params for the tool")

message_history = [
    {"role": "system" , "content": SYSTEM_PROMPT},
]

user_input = input("🫵🏻 ")
message_history.append({"role" : "user" , "content": user_input})

while True:
    response = client.chat.completions.parse(
        model = "gpt-4o-mini",
        response_format=MyOutputFormat ,
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    print(f"DEBUG: Raw AI Output: {raw_result}")
    message_history.append({"role": "assistant", "content": raw_result})
 
    parsed_result = response.choices[0].message.parsed

    if parsed_result.step == "START":
        print("🔥", parsed_result.content)
        continue

    if parsed_result.step == "PLAN":
        print("🧠", parsed_result.content)
        continue

    if parsed_result.step == "TOOL":
        tool_to_call = parsed_result.tool
        tool_input = parsed_result.input
        print("🔨", {tool_to_call} , {tool_input})

        tool_response = available_tools[tool_to_call](tool_input)
        message_history.append({"role": "developer", "content": json.dumps(
            { "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
        )})
        continue

    if parsed_result.step == "OUTPUT":
        print("🔥", parsed_result.content)
        break

    

    

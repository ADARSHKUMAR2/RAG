from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated

# In this environment, init_chat_model comes from langchain_classic.
from langchain_classic.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

load_dotenv()

# Fixed the model name
llm = init_chat_model(
    model="gpt-4o-mini",
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": ["HI, this is a msg from chatbot Node"]}

def sampleNode(state: State):
    return {"messages": ["HI, this is a msg from sample Node"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleNode", sampleNode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleNode")

# Fixed the missing quotes around "sampleNode"
graph_builder.add_edge("sampleNode", END)

graph = graph_builder.compile()

# --- HOW TO RUN AND TEST IT ---
if __name__ == "__main__":
    # 1. Ask the user for their input in the terminal
    user_text = input("You: ")
    
    # 2. Package the input into the graph's State format.
    # We use a tuple ("user", user_text) so LangGraph knows a human said it.
    initial_state = {"messages": [("user", user_text)]}
    
    print("\nProcessing through the graph...\n")
    
    # 3. Run the graph with your custom input
    result = graph.invoke(initial_state)
    
    # 4. Print the final history
    print("🚀 Final Graph State:")
    for msg in result["messages"]:
        # LangGraph automatically converts your strings into Message objects!
        # We can check who sent the message to print it nicely:
        try:
            print(f"[{msg.type.upper()}]: {msg.content}")
        except AttributeError:
            # Fallback just in case it's a raw string
            print(f"- {msg}")
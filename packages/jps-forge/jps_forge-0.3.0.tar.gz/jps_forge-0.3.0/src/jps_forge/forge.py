#!/usr/bin/env python3
import yaml
import sys

from rich.console import Console
from rich.markdown import Markdown
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from .tools import list_dirty_repos, git_status, current_repo_status

from .constants import DEFAULT_CONFIG_FILE_PATH, DEFAULT_TEMPERATURE, DEFAULT_STORAGE_DIR


console = Console()

with open(DEFAULT_CONFIG_FILE_PATH) as f:
    config = yaml.safe_load(f)

llm = ChatOllama(model=config["ollama_model"], temperature=DEFAULT_TEMPERATURE)

embeddings = HuggingFaceEmbeddings(model_name=config["embedding_model"])

vectorstore = FAISS.load_local(DEFAULT_STORAGE_DIR, embeddings, allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

tools = [list_dirty_repos, git_status, current_repo_status]

# System prompt for the agent
system_prompt = "You are jps-forge, a local coding assistant. Use the provided tools when needed. Always cite source_path from retrieved documents when relevant."

memory = MemorySaver()
agent_executor = create_react_agent(
    llm, 
    tools,
    prompt=system_prompt,
    checkpointer=memory
)

config_dict = {"configurable": {"thread_id": "jps-forge-session"}}

def chat():
    console.print(Markdown("# jps-forge ready"))
    console.print("Type 'exit' or Ctrl+C to quit\n")

    while True:
        try:
            query = input("you: ")
            if query.lower() in ["exit", "quit"]:
                break

            # Retrieve context
            docs = retriever.invoke(query)
            context = "\n\n".join([d.page_content for d in docs])

            full_prompt = f"""Context from your codebase:
{context}

Question: {query}"""

            with console.status("thinking..."):
                result = agent_executor.invoke(
                    {"messages": [("human", full_prompt)]},
                    config=config_dict
                )

            # Display all messages to show tool usage
            messages = result["messages"]
            
            # Show tool calls if any
            for msg in messages[1:-1]:  # Skip the input and final output
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        console.print(f"[dim]🔧 Using tool: {tool_call['name']}[/dim]")
                elif hasattr(msg, 'content') and msg.content and msg.type == 'tool':
                    console.print(f"[dim]📋 Tool result: {msg.content[:100]}...[/dim]")
            
            final_message = messages[-1]
            console.print(Markdown(f"**forge:** {final_message.content}"))
            console.print()  # newline

        except KeyboardInterrupt:
            break

def main():
    """Main entry point for the jps-forge-forge command."""
    chat()

if __name__ == "__main__":
    main()
#!/usr/bin/env python

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import OpenAI, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from tempfile import TemporaryDirectory

from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools import HumanInputRun
from langchain_community.tools.file_management.list_dir import ListDirectoryTool

load_dotenv()


def get_input() -> str:
    """
    Get input from the user.
    """
    print("Insert your text. Enter 'q' or press Ctrl-D (or Ctrl-Z on Windows) to end.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "q":
            break
        contents.append(line)
    return "\n".join(contents)


if __name__ == "__main__":
    # We'll make a temporary directory to avoid clutter
    working_directory = TemporaryDirectory()

    # If you don't provide a root_dir, operations will default to the current working directory
    toolkit = FileManagementToolkit(root_dir="/Users/gautam/source/hello-fastapi")
    file_tools = []
    file_tools += toolkit.get_tools()

    #human_tool = HumanInputRun(input_func=get_input)

    #tools = [TavilySearchResults(max_results=1)]
    #tools = file_tools + [human_tool]
    tools = file_tools

    # Get the prompt to use - you can modify this!
    prompt = ChatPromptTemplate.from_messages(
        [("system",
            """
            Answer the following questions as best you can. You have access to the following tools:

            {tools}

            Use the following format:

            Question: the input question you must answer

            Thought: you should always think about what to do

            Action: the action to take, should be one of [{tool_names}]

            Action Input: the input to the action

            Observation: the result of the action

            ... (this Thought/Action/Action Input/Observation can repeat N times)

            Thought: I now know the final answer

            Final Answer: the final answer to the original input question

            Begin!

            Question: {input}

            Thought:{agent_scratchpad}
                """)
                ])

    # Choose the LLM to use
    #llm = OpenAI(model="gpt-3.5-turbo-instruct")
    #llm = OpenAI(model="gpt-4-turbo")
    llm = ChatOpenAI(model="gpt-4-turbo")

    # Construct the ReAct agent
    agent = create_react_agent(llm, tools, prompt)
    #agent = create_tool_calling_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke({"input": "Describe the project in the current directory"})
    #agent_executor.invoke({"input": "List the files in the current directory"})
    #print([tool for tool in tools if isinstance(tool, ListDirectoryTool)][0].run("pwd"))
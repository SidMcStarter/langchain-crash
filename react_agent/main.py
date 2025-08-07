from dotenv import load_dotenv
from langchain_core.tools import tool, Tool
from langchain.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from typing import List, Union
from langchain.agents.format_scratchpad import format_log_to_str
from .callbacks import AgentCallBackHandler
load_dotenv()

@tool
def get_text_length(text: str) -> int:
    """
    Returns the length of the text by characters
    """
    text = text.strip("'\n").strip('""')
    return len(text)

def get_tool_by_name(tools: List[Tool], name: str) -> Tool:
    for tool in tools:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool with name {name} not found")

if __name__ == "__main__":
    tools: List[Tool] = [get_text_length]
    
    react_prompt_template = """
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
    Thought: {agent_scratchpad}
    """
    

    prompt = PromptTemplate(
        template=react_prompt_template,
        partial_variables={
            "tools": render_text_description(tools),
            "tool_names": ", ".join([tool.name for tool in tools]),
        },
        input_variables=["input"]
    )
    
    intermediate_steps = [] #collection of things done in the llm process
    
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", stop=["\nObservation", "Observation:", "Observation"], callbacks=[AgentCallBackHandler()])
    agent = {
        "input": lambda x: x["input"], 
        "agent_scratchpad": lambda x: x["agent_scratchpad"]
        } | prompt | llm | ReActSingleInputOutputParser()
    
    query = "What is the length of the text 'Hello manhattan world' in characters?"
    
    agent_step = ""
    while not isinstance(agent_step, (AgentFinish)):
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": query, 
                "agent_scratchpad": format_log_to_str(intermediate_steps)
            }
        )  
    # check if response is an AgentAction or AgentFinish
        if isinstance(agent_step, AgentAction):
            action = agent_step.tool # tool name
            tool_to_use = get_tool_by_name(tools, action)
            tool_input = agent_step.tool_input
            observation = tool_to_use.invoke(str(tool_input))
            # print(f"Action: {action}, Tool Input: {tool_input}, Result: {observation}")
            intermediate_steps.append((agent_step, observation))
            # print(f"Intermediate Steps: {format_log_to_str(intermediate_steps)}")
        
    if isinstance(agent_step, AgentFinish):
        print(f"Final Response: {agent_step.return_values}")
        
    
  
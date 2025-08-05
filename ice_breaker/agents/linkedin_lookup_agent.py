from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.agents import create_react_agent
from ice_breaker.tools.tools import get_profile_url_tavily
from dotenv import load_dotenv

def lookup(name: str):
    # define the llm
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    
    # define the template to use for the intial input
    template = """
    Given the full name of the person, {full_name}, I want you to give me a link to their linkedin url.
    When you have found the LinkedIn URL, respond with only the url and nothing else
    """
    
    prompt = PromptTemplate(
        input_variables=["full_name"],
        template=template
    )
    
    # collection of tools to use
    tools = [
        Tool(
            name = "Scrape Google for LinkedIn URL",
            func = get_profile_url_tavily,
            description="useful for looking up person linkedin urls",
        )
    ]
    
    react_prompt = hub.pull("hwchase17/react")  # Pull the react prompt from LangChain Hub
    
    # define teh agent with llm, tools, and the react prompt
    agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt,)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    result = agent_executor.invoke(
        input={"input": prompt.format_prompt(full_name=name)}
    )
    linkedin_url = result["output"]
    return linkedin_url
if __name__ == "__main__":
    load_dotenv()
    linkedin_url = lookup("Siddharth Dileep UofA(alberta)")
    print(f"LinkedIn URL: {linkedin_url}")
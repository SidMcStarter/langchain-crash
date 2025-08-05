from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from ice_breaker.third_parties.linkedin_utils import scrape_from_linkedin
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from ice_breaker.agents.linkedin_lookup_agent import lookup as linkedin_lookup
from ice_breaker.agents.twitter_lookup_agent import lookup as twitter_lookup
from langchain_core.prompts import PromptTemplate
from ice_breaker.third_parties.twitter import scrape_user_tweets
from ice_breaker.parsers.summary_parser import summary_parser, Summary
from typing import Tuple

def ice_break_with(name) -> Tuple[Summary, str]:
    summary_template = """
    Given the linkedin information {information} about a person, and tweets {tweets} from their twitter acount 
    I want you to do the following two things
    1) Generate a brief summary
    2) a summary about their tweets
    \n
    {formatted_instructions}
    """

    summary_prompt = PromptTemplate(inpput_variables=["information"], partial_variables={"formatted_instructions": summary_parser.get_format_instructions()}, template=summary_template)
    
    linkedin_url = linkedin_lookup(name) # get the url
    linkedin_data = scrape_from_linkedin(linkedin_url, mock=False) #pass the url and get linkedin data
    
    twitter_url = twitter_lookup(name) # get the twitter url
    twitter_data = scrape_user_tweets(twitter_url, mock=True) # pass the url
    
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    
    chain = summary_prompt | llm | summary_parser
    
    res = chain.invoke(
        {
            "information": linkedin_data, 
            "tweets": twitter_data,
         },
    )
    
    return res, linkedin_data["photoUrl"]
    

    
if __name__ == "__main__":
    load_dotenv()
    result, url = ice_break_with("Eden Marco")
    print(f"LinkedIn URL: {url}")
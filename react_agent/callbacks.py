from langchain.callbacks.base import BaseCallbackHandler
from typing import List, Any

class AgentCallBackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized: dict, prompts: List[str], **kwargs: Any) -> None:
        print("*************** LLM Start ***************")
        print(f"LLM started with prompts: {prompts[0]}")
        print("*************** LLM Starting ***************")

        
    def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        print("*************** LLM End ***************")
        print(f"LLM ended with response: {response.generations[0][0].text}")
        print("*************** LLM Ending ***************")

    
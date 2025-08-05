from pydantic import BaseModel, Field
from typing import List, Any, Dict
from langchain_core.output_parsers import PydanticOutputParser

class Summary(BaseModel):
    facts: List[str] = Field(description="Facts about the user")
    summary: str = Field(description="summary about the user")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "facts": self.facts,
            "summary": self.summary
        }
        
        
summary_parser = PydanticOutputParser(pydantic_object=Summary)
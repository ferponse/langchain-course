from typing import List, Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="Un resumen breve de la información de LinkedIn")
    facts: List[str] = Field(description="Dos datos interesantes sobre la persona")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "facts": self.facts
        }
    
summary_parser = PydanticOutputParser(pydantic_object=Summary)

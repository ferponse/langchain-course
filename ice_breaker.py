import os
from typing import Any, Dict
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello LangChain!")

    load_dotenv()

    summary_template: str = """
        Dada la información de LinkedIn {information} sobre una persona, quiero que crees:
        1. Un resumen breve
        2. Dos datos interesantes sobre ella
    """

    summary_prompt_template: PromptTemplate = PromptTemplate(template=summary_template, input_variables=["information"])

    llm: ChatOpenAI = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    chain: LLMChain = summary_prompt_template | llm

    linkedin_data: Dict[str, Any] = scrape_linkedin_profile(linkedin_profile_url="https://linkedin.com/in/ferranponsdev/", mock=True)

    result: AIMessage = chain.invoke(input={"information": linkedin_data})

    print(result.content)

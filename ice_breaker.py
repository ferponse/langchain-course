from typing import Tuple
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    summary_template: str = """
        Dada la información de LinkedIn {information} sobre una persona, quiero que crees:
        1. Un resumen breve
        2. Dos datos interesantes sobre ella

        {format_instructions}
    """

    summary_prompt_template: PromptTemplate = PromptTemplate(template=summary_template, input_variables=["information"], partial_variables={"format_instructions": summary_parser.get_format_instructions()})

    llm: ChatOpenAI = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    
    chain: LLMChain = summary_prompt_template | llm | summary_parser

    result: Summary = chain.invoke(input={"information": linkedin_data})

    return result, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    load_dotenv()
    ice_break_with(name="Ferran Pons Serra Linkedin IA")
    

import os
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub

from tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    llm: ChatOpenAI = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    template: str = """Given the full name {name_of_person} I want you to get back the LinkedIn Page URL. Your answer should contain only a URL"""

    prompt: PromptTemplate = PromptTemplate(template=template, input_variables=["name_of_person"])

    tools_for_agent: List[Tool] = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn Page URL"
        )
    ]

    react_prompt: PromptTemplate = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor: AgentExecutor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result: dict = agent_executor.invoke({"input": prompt.format(name_of_person=name)})

    linked_profile_url: str = result["output"]

    return linked_profile_url

if __name__ == "__main__":
    linkedin_url = lookup("Ferran Pons Serra Linkedin IA")
    print(linkedin_url)

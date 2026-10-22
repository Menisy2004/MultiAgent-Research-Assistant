from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.tools.tools import web_search, scrape_url, web_open
from dotenv import load_dotenv

load_dotenv(override=True)

# Model Initialization 
llm_fast = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
llm_smart = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

# Use llm_fast in build_search_agent() and build_reader_agent()
# Use llm_smart in writer_chain and critic_chain

# 1st Agent(Search agent)
def build_search_agent():
    return create_agent(
        model=llm_fast,
        tools=[web_search, web_open],
        system_prompt="""You are an expert research assistant. Always cite your sources, make sure to get reliable sources."""
    )

# 2nd Agent(Reader Agent)
def build_reader_agent():
    return create_agent(
        model=llm_fast,
        tools=[scrape_url],
        system_prompt="""You are a reader agent that is responsible to scrape info from the sources outputed by the search agent.
        IMPORTANT: You do not have a search tool. Do not attempt to call search. You must only use the scrape_url tool by passing valid URLs."""
    )


# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusions
- Sources (list all URLs found in the research)

Be detailed, factual and professiona
"""),
])

writer_chain = writer_prompt | llm_smart | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a top-notch research critic that evaluates researches and forces writer to keep editting until he outputs best version possible of the research. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

    Report:
    {report}

    Respond in this exact format:

    Score: X/10

    Strengths:
    - ...
    - ...

    Areas to Improve:
    - ...
    - ...
    One line verdict:
    ..."""),
])
critic_chain = critic_prompt | llm_smart | StrOutputParser()
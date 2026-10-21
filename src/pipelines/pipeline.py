from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic: str) -> dict:
    # temp memory
    state = {}

    #search agent working 
    print("\n"+" = "*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ", state['search_results'])

    # Step 2 - Reader Agent
    print("\n"+" ="*50)
    print("Step 2 - Reader agent is scraping top sources ...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages" : [("user", 
                       f"Based on the following search results about {topic}, "
                       f"pich the most relevant URL and scrape it for deeper content.\n\n"
                       f"Search Results:\n{state['search_results'][:300]}")]
    })

    state['scrapped_content'] = reader_result['messages'][-1].content

    print("\n Scrapped content: \n", state['scrapped_content'])

    # Step 3 - Writer Chain
    print("\n"+" ="*50)
    print("Step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"Search results : \n {state['search_results']}\n\n"
        f"Detailed scrapped content: \n {state['scrapped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n", state['report'])

    # Step 4 - Critic Chain 
    print("\n"+" ="*50)
    print("Step 4 - Critic is evaluating the report")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n Critic report \n", state['feedback'])

    return state
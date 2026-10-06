#Import Libraries 
import os 
from datetime import datetime
from google import genai
import wikipedia
import arxiv
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
arxiv_client = arxiv.Client(page_size=1, delay_seconds=3)

# ------------------------ TOOLS ------------------------# 
# tavily API Key
def tavily_tool(query:str):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    try:
        response = tavily_client.search(query, max_results=1)
        print("Called Tavily.")
        return response
    except Exception as e:
        return f"Tavily failed:{str(e)}"
    
# arxiv API
#search = arxiv.Search(
#  query="Mechanistic Interpretability in Medical AI",
#  max_results=1,
#  sort_by=arxiv.SortCriterion.Relevance
#)

#for paper in arxiv_client.results(search):
#    print(f"Title: {paper.title}")
    
# Wiki API
def wikipedia_tool(query:str) -> str:
    try:
        results = wikipedia.summary(query, sentences=5)
        print("Called Wiki.")
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Topic-{query} is ambigious."
    except wikipedia.exceptions.PageError:
        return f"Page Error. No page found for {query}"
    except Exception as e:
        return f"Wikipedia Error:{str(e)}"
    
# ------------------------ AGENTs ------------------------# 

# Creating Research Agent which can access current wiki tool 

def research_agent(task:str, model: str = "gemini-3.5-flash-lite") -> str:
    """
    This function takes a task, performs it and returns a summary of the results. 
    """
    print("Called Research Agent.")
    prompt = f"""You are an expert researcher. You will be given a research task. You have access to the following tool 
    -wikipedia_tool: encyclopedia summaries.\n
    Task :{task}
    Today is {datetime.now().strftime('%Y-%m-%d')},
    """.strip()
    try:
        chat = gemini_client.chats.create(
            model=model,
            config={
                "tools":[wikipedia_tool]
            }
        )
        response = chat.send_message(prompt)
        print("Research Agent Finished.")
        return response.text
    except Exception as e:
        print(f"Error in Research Agent- {str(e)}")


# Creating Professor Agent which can answer to professor related queries 

def prof_agent(task:str, model: str = "gemini-3.5-flash-lite") -> str:
    """
    This function takes a task and executes it. 
    """
    print("Called Prof Agent.")
    prompt = f""" You are an expert finder. You will be given a task. You have access to the following tool, if required, to execute the task.
    -tavily_tool: web search and content extraction.\n
    Task :{task}\n
    Today is {datetime.now().strftime('%Y-%m-%d')},
    """.strip()
    try:
           chat = gemini_client.chats.create(
               model=model,
               config={
                   "tools":[tavily_tool]
               }
           )
           response = chat.send_message(prompt)
           print("Prof Agent Finished.")
           return response.text
    except Exception as e:
           print(f"Error in Prof Agent- {str(e)}")


# Creating ResearchSphere Manager Agent which depending on the query will either assign the task 
# to Research Agent or Prof Agent 

def researchSphereManager (user_prompt:str, model:str = "gemini-3.5-flash-lite"):
    """
    This agent behaves as a manager. The agent decides depending on the query, whether to call research agent 
    or prof agent. 
    """

    system_prompt = f"""
    You are a knowledgable agent who is given a user query. Based on the nature of user query, you decide if the 
    query will be answered by Research agent or Prof Agent. 
    -research_agent : answers simple research  or general knowledge queries
    -prof_agent : answers queries related to professors 
    """
    print("Manager is called.")
    try:    
        chat = gemini_client.chats.create(
            model=model,
            config={ 
                    "system_instruction":system_prompt,
                    "tools":[research_agent, prof_agent]
                }
        )
        response = chat.send_message(user_prompt)
        print("Manager Execution Finished. Query Answered.")
        return response.text
    except Exception as e:
        print(f"Error in the Manager - {str(e)}")


if __name__ == "__main__":  
    user_query = "Name one Professor is working on AI in Bangalore city in india. Give the instituition and other details as well. "
    result = researchSphereManager(user_query)
    print(result)
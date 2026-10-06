# ResearchSphere

ResearchSphere is a simple multi-agent AI prototype for handling
research-related queries.

The system uses a **Manager Agent** to route a user's query to one of
two specialized agents:

-   **Research Agent (RA)** --- answers general knowledge and research
    questions using **Wikipedia**.
-   **Professor Agent (PA)** --- answers professor-related queries using
    **Tavily web search**.

## Current Architecture

``` text
                    User Query
                        |
                        v
                  Manager Agent
                   /          \
                  v            v
          Research Agent   Professor Agent
                |                |
                v                v
            Wikipedia          Tavily
```

## Current Features

-   Manager-based query routing
-   General knowledge and research question answering
-   Professor and researcher search
-   Wikipedia tool integration for the Research Agent
-   Tavily search integration for the Professor Agent
-   Gemini-based agents and tool calling

## Example Queries

General research query:

``` text
What is reinforcement learning?
```

The Manager routes this to the **Research Agent**, which can use
Wikipedia.

Professor-related query:

``` text
Name a professor working on AI in Bangalore and provide their institution.
```

The Manager routes this to the **Professor Agent**, which can use
Tavily.

## Setup

### 1. Clone the repository

``` bash
git clone <your-repository-url>
cd ResearchSphere
```

### 2. Install dependencies

``` bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

``` text
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Do not commit the `.env` file to GitHub.

### 4. Run the prototype

``` bash
python researchSphere.py
```

## Status

This is an early prototype. The current goal is to establish a simple
working multi-agent architecture before adding more tools, verification,
and research capabilities.

## Planned Improvements

-   Academic paper search
-   Structured professor/researcher databases
-   Source verification
-   Better routing and multi-agent collaboration
-   More robust error handling
-   Structured responses and citations

## Disclaimer

ResearchSphere is an experimental project. Information returned by
language models and external tools may be incomplete or inaccurate and
should be independently verified.

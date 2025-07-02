from uagents import Context, Model
from typing import List

class NewsRequest(Model):
    query: str

class NewsResult(Model):
    response: str

class WebSearchRequest(Model):
    query: str

class WebSearchResult(Model):
    title: str
    url: str
    content: str

class WebSearchResponse(Model):
    query: str
    results: List[WebSearchResult]

class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str

# Agent addresses
TAVILY_ADDRESS = 'agent1qt5uffgp0l3h9mqed8zh8vy5vs374jl2f8y0mjjvqm44axqseejqzmzx9v8'
ASI_1_MIN_ADDRESS = 'agent1qvn0t4u5jeyewp9l544mykv639szuhq8dhmatrgfuwqphx20n8jn78m9paa'

PROMPT_STRING = """
Analyze the following news headline and the accompanying web search data to determine whether the event actually occurred or is fabricated, regardless of when it happened.

Headline: "{headline}"
Web Search Data: "{web_data}"

Evaluation Criteria:
1. Authenticity: Determine if the event in the headline is fully true, partially true, or false based on the data.
2. Partial Truth: If some parts of the headline are accurate (e.g., event occurred but date/location is wrong), classify it as Partially True.
3. Falsehood: If the event did not happen or cannot be confirmed at all, classify as False.
4. Date Detection: If the event occurred, identify and include the actual date in the summary.
5. Location Verification: Ensure the headline location aligns with the real event location from credible sources.
6. Source Recognition: Extract and mention the names or domains of sources that validate or refute the headline..

Important Guidelines:
1. Mark the headline as Fake only if the event did not occur or is a misrepresentation of reality.
2. Do not assume or rely on external knowledge. Use only the web search data provided.
3. If no reliable source confirms the event, treat it as fake.
4. Keep the Reason and Summary around 80 words each.
5. If the headline is Valid, ensure the summary clearly includes the actual date of the event.
6. If the verdict is False, return "null" for the Summary field.

Format of Output:
Verdict: True / Partially True / False
Reason: [Your reasoning in 80 words]
Summary: [80 words summarizing the event with actual date if applicable OR "null" if verdict is False]
Sources: [List of news source names or domains as shared by Tavily, separated by commas]

"""

async def verify_news(ctx: Context, query: str) -> str:
    """
    Verify news by searching for information and analyzing it with AI
    """
    try:
        # Step 1: Search for information using Tavily
        ctx.logger.info(f"Searching for information about: {query}")
        
        search_reply, search_status = await ctx.send_and_receive(
            TAVILY_ADDRESS, 
            WebSearchRequest(query=query),
            response_type=WebSearchResponse
        )
        
        if not isinstance(search_reply, WebSearchResponse):
            ctx.logger.error(f"Failed to receive search response: {search_status}")
            return "Error: Unable to search for information. Please try again later."
        
        # Step 2: Process search results
        ctx.logger.info(f"Processing search results for: {search_reply.query}")
        data = []
        for result in search_reply.results:
            data.append(result.content)
            ctx.logger.info(f"Found: {result.title} - {result.url}")
        
        if not data:
            return "Error: No search results found for the given query."
        
        # Step 3: Prepare prompt for AI analysis
        web_data = f"Search results summary from Tavily: {data}"
        final_prompt = PROMPT_STRING.format(headline=query, web_data=web_data)
        
        # Step 4: Get AI analysis
        ctx.logger.info("Sending data to AI for verification analysis")
        
        ai_reply, ai_status = await ctx.send_and_receive(
            ASI_1_MIN_ADDRESS,
            ASI1miniRequest(query=final_prompt),
            response_type=ASI1miniResponse
        )
        
        if not isinstance(ai_reply, ASI1miniResponse):
            ctx.logger.error(f"Failed to receive AI response: {ai_status}")
            return "Error: Unable to analyze the information. Please try again later."
        
        ctx.logger.info(f"Verification completed for: {query}")
        return ai_reply.response
        
    except Exception as e:
        ctx.logger.error(f"Error during news verification: {str(e)}")
        return f"Error during news verification: {str(e)}"
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
1. Event Occurrence: Confirm whether the event mentioned in the headline actually took place.
2. Date Detection: Identify the actual date of the event if it occurred.
3. Location Accuracy: Ensure the event location in the headline matches the event location in the sources.
4. Misinformation Detection: If the event was fabricated, misleading, or not mentioned in the data, treat it as Fake.

Important Guidelines:
1. Mark the headline as Fake only if the event did not occur or is a misrepresentation of reality.
2. Do not assume or rely on external knowledge. Use only the web search data provided.
3. If no reliable source confirms the event, treat it as fake.
4. Do not generate summaries for Fake headlines.
5. If the headline is Valid, ensure the summary clearly includes the actual date of the event.

Format of Output:
1. The headline "{headline}" is Valid/Fake. (Choose one based on your analysis)
2. A brief reasoning explaining your validation reasoning.
3. If the news is Valid, add a summary of the incident in 60 words or less.

Note: If the news is Fake, skip the summary section.


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
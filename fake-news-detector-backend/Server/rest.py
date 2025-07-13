import os
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class NewsRequest(Model):
    query: str

class NewsResult(Model):
    response: str

class NewsResponse(Model):
    msg: str

port=8080

rest_agent = Agent(
    name="Rest Agent", 
    seed="I am the Rest Agent", 
    port=port
)

news_agent = 'agent1qwkkq47cjw82uqtw6t8ts3rdsnjy5a2dxnwdla7uy9vnv4a3eynk2yjr638'

fund_agent_if_low(rest_agent.wallet.address())

@rest_agent.on_event('startup')
async def startup(ctx: Context):
    print(f"News Agent is starting up on port {port}...")

@rest_agent.on_rest_get('/', NewsResult)
async def index(ctx: Context) -> NewsResponse:
    return NewsResponse(msg="Welcome to the News Agent!")

@rest_agent.on_rest_post('/news', NewsRequest, NewsResponse)
async def get_news(ctx: Context, request: NewsRequest) -> NewsResponse:
    print(f"Received news request: {request.query}")
    try:
        res, status = await ctx.send_and_receive(news_agent, NewsRequest(query=request.query), response_type=NewsResult)
        if res:
            output = res.response
            print(output)
            return NewsResponse(msg=output)
        else:
            return NewsResponse(msg="No response received from news agent.")
    except Exception as e:
        print(f"Error processing request: {e}")
        return NewsResponse(msg=f"Error processing request: {str(e)}")

@rest_agent.on_rest_get('/health', NewsResult)
async def health_check(ctx: Context) -> NewsResponse:
    return NewsResponse(msg="Service is healthy")

if __name__ == "__main__":
    rest_agent.run()
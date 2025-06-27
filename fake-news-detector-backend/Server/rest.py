from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class NewsRequest(Model):
    query: str

class NewsResult(Model):
    response: str

class NewsResponse(Model):
    msg: str

rest_agent=Agent(name="Rest Agent", seed="I am the Rest Agent", port=8080, endpoint="http://localhost:8080/submit")

news_agent = 'agent1qdd95k4ffs8g32905a6dj5rrc4suqd53ndaw8jafesq7f2z2fhu2ujy43wx'

fund_agent_if_low(rest_agent.wallet.address()) #type:ignore

@rest_agent.on_event('startup')
async def startup(ctx: Context):
    print("News Agent is starting up...")

@rest_agent.on_rest_get('/', NewsResult)
async def index(ctx: Context) -> NewsResponse:
    return NewsResponse(msg="Welcome to the News Agent!")

@rest_agent.on_rest_post('/news', NewsRequest, NewsResponse)
async def get_news(ctx: Context, request: NewsRequest) -> NewsResponse:
    print(f"Received news request: {request.query}")
    res, status = await ctx.send_and_receive(news_agent, NewsRequest(query=request.query), response_type=NewsResult)
    if res:
        output = res.response #type:ignore
        print(output)
        return NewsResponse(msg=output)
    else:
        return NewsResponse(msg="No response received from news rest_agent. ")

if __name__ == "__main__":
    rest_agent.run()
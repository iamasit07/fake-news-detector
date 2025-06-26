import os
from enum import Enum

from uagents import Agent, Context, Model
from uagents.experimental.quota import QuotaProtocol, RateLimit
from uagents.setup import fund_agent_if_low
from uagents_core.models import ErrorMessage

from news_chat_proto import chat_proto, struct_output_client_proto
from news_verification import verify_news, NewsRequest, NewsResult

agent = Agent(name="Main Agent", seed="Main Agent", port=8009, mailbox=True)

fund_agent_if_low(agent.wallet.address()) #type:ignore

proto = QuotaProtocol(
    storage_reference=agent.storage,
    name="News-Verification-Protocol",
    version="0.1.0",
    default_rate_limit=RateLimit(window_size_minutes=60, max_requests=50),
)

@proto.on_message(
    NewsRequest, replies={NewsResult, ErrorMessage}
)
async def handle_news_request(ctx: Context, sender: str, msg: NewsRequest):
    ctx.logger.info("Received news verification request")
    try:
        result = await verify_news(ctx, msg.query)
        ctx.logger.info(f'News verification completed for: {msg.query}')
        ctx.logger.info("Successfully verified news")
        await ctx.send(sender, NewsResult(response=result))
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(sender, ErrorMessage(error=str(err)))

agent.include(proto, publish_manifest=True)

### Health check related code
def agent_is_healthy() -> bool:
    """
    Implement the actual health check logic here.
    For example, check if the agent can connect to the Tavily API and ASI mini.
    """
    try:
        # Simple health check - you can expand this
        return True
    except Exception:
        return False

class HealthCheck(Model):
    pass

class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"

class AgentHealth(Model):
    agent_name: str
    status: HealthStatus

health_protocol = QuotaProtocol(
    storage_reference=agent.storage, name="HealthProtocol", version="0.1.0"
)

@health_protocol.on_message(HealthCheck, replies={AgentHealth})
async def handle_health_check(ctx: Context, sender: str, msg: HealthCheck):
    status = HealthStatus.UNHEALTHY
    try:
        if agent_is_healthy():
            status = HealthStatus.HEALTHY
    except Exception as err:
        ctx.logger.error(err)
    finally:
        await ctx.send(sender, AgentHealth(agent_name="news_verification_agent", status=status))

agent.include(health_protocol, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)
agent.include(struct_output_client_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()
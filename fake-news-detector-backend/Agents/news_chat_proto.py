from datetime import datetime
from uuid import uuid4
from typing import Any

from uagents import Context, Model, Protocol

# Import the necessary components of the chat protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

from news_verification import NewsRequest

# Replace the AI Agent Address with anyone of the following LLMs as they support StructuredOutput required for the processing of this agent.
AI_AGENT_ADDRESS = 'agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y'

if not AI_AGENT_ADDRESS:
    raise ValueError("AI_AGENT_ADDRESS not set")


def create_text_chat(text: str, end_session: bool = True) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session: 
        content.append(EndSessionContent(type="end-session")) #type:ignore
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content, #type:ignore
    )


chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_client_proto = Protocol(
    name="StructuredOutputClientProtocol", version="0.1.0"
)


class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    output: dict[str, Any]


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Safely log the first content item
    first_item = msg.content[0] if msg.content else None
    if isinstance(first_item, TextContent):
        ctx.logger.info(f"Got a message from {sender}: {first_item.text}")
    else:
        ctx.logger.info(f"Got a message from {sender}: {type(first_item).__name__ if first_item else 'No content'}")
    ctx.storage.set(str(ctx.session), sender)
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")
            ctx.storage.set(str(ctx.session), sender)
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=f"Extract the news headline or query to verify from this message: '{item.text}'. The user wants to check if a news story is real or fake.",
                    output_schema=NewsRequest.schema()
                ),
            )
        else:
            ctx.logger.info(f"Got unexpected content from {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}"
    )


@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output_response(
    ctx: Context, sender: str, msg: StructuredOutputResponse
):
    session_sender = ctx.storage.get(str(ctx.session))
    if session_sender is None:
        ctx.logger.error(
            "Discarding message because no session sender found in storage"
        )
        return

    if "<UNKNOWN>" in str(msg.output):
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your news verification request. Please try again with a clear news headline or query."
            ),
        )
        return

    try:
        news_request = NewsRequest.parse_obj(msg.output)
    except Exception as err:
        ctx.logger.error(f"Failed to parse structured output: {err}")
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't understand your request. Please provide a clear news headline to verify."
            ),
        )
        return

    try:
        from news_verification import verify_news
        verification_result = await verify_news(ctx, news_request.query)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your news verification request. Please try again later."
            ),
        )
        return

    chat_message = create_text_chat(verification_result)
    await ctx.send(session_sender, chat_message)
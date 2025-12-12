from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, Depends, HTTPException, status, Header
import time
import uuid
import asyncio
import os
from digital_life.core import ChatBox
from .chat_models import *
from contextlib import asynccontextmanager

# --- (Optional) Authentication Dependency ---
async def verify_api_key(authorization: Optional[str] = Header(None)):
    """
    Placeholder for API key verification.
    In a real application, you'd compare this to a stored list of valid keys.
    """
    if not authorization:
        
        return None
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization scheme")

    token = authorization.split(" ")[1]
    x = os.getenv("server_api_key")
    valid_keys = set(x.split(','))
    if token not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    print(f"Received valid API Key (last 4 chars): ...{token[-4:]}")
    # --- End Replace ---
    return token 

@asynccontextmanager
async def chat_router_lifespan(router: APIRouter):
    global chatbox
    # 路由启动时执行
    print("Chat Router lifespan: Initializing ChatBox...")
    chatbox = ChatBox()
    await chatbox.init_chatbox()
    print("Chat Router lifespan: ChatBox initialized.")
    yield # 路由存活期间
    print("Chat Router lifespan: Shutting down ChatBox...")
    # 这里可以添加 chatbox_instance 的清理逻辑，如果 ChatBox 有的话
    chatbox = None
    print("Chat Router lifespan: ChatBox shut down.")


router = APIRouter(
    tags=["ChatGPTs-V1"],
    dependencies = [Depends(verify_api_key)],
    lifespan=chat_router_lifespan
)

# --- Mock LLM Call ---

async def generate_llm_response(prompt: str, stream: bool, model: str,
                                user_id: str,
                                topic: str
                                ):
    """
    Replace this with your actual LLM call logic.
    This mock function simulates generating text.
    """
    response_id = f"chatcmpl-{uuid.uuid4().hex}"
    created_time = int(time.time())
    if not stream:
        full_response = chatbox.product(prompt_with_history = prompt,model=model)
        # full_response = " ".join(words)
        words = full_response.split(' ')
        choice = Choice(
            index=0,
            message=ChatCompletionMessage(role="assistant", content=full_response),
            finish_reason="stop"
        )
        # Simulate token counts (highly inaccurate)
        usage = UsageInfo(prompt_tokens=len(prompt.split()),
                          completion_tokens=len(words),
                          total_tokens=len(prompt.split()) + len(words))
        return ChatCompletionResponse(
            id=response_id,
            model=model,
            choices=[choice],
            usage=usage,
            created=created_time
        )
    else:
        async def stream_generator():
            # First chunk: Send role
            first_chunk_choice = ChunkChoice(index=0, delta=DeltaMessage(role="assistant"),
                                                                finish_reason=None)
            yield ChatCompletionChunkResponse(
                id=response_id, model=model, choices=[first_chunk_choice], created=created_time
            ).model_dump_json() # Use model_dump_json() for Pydantic v2

            # Subsequent chunks: Send content word by word

            async for word in chatbox.astream_product(prompt_with_history = prompt,
                                                            model=model,
                                                            user_id = user_id,
                                                            topic = topic
                                                            ):
                chunk_choice = ChunkChoice(index=0,
                                        delta=DeltaMessage(content=f"{word}"),
                                                                finish_reason=None)
                yield ChatCompletionChunkResponse(
                    id=response_id, model=model, choices=[chunk_choice], created=created_time
                ).model_dump_json()
                # await asyncio.sleep(0.001) # Simulate token generation time


            # Final chunk: Send finish reason
            final_chunk_choice = ChunkChoice(index=0, delta=DeltaMessage(), finish_reason="stop")
            yield ChatCompletionChunkResponse(
                id=response_id, model=model, choices=[final_chunk_choice], created=created_time
            ).model_dump_json()

            # End of stream marker (specific to SSE)
            yield "[DONE]"

        # Need to wrap the generator for EventSourceResponse
        async def event_publisher():
            try:
                async for chunk in stream_generator():
                    yield {"data": chunk}
                    # await asyncio.sleep(0.01) # Short delay between sending chunks is good practice
            except asyncio.CancelledError as e:
                raise e
            
            except Exception as e:
                yield f"Error details: {str(e)}"
            finally:
                print("Event generator finished.")

        return EventSourceResponse(event_publisher())


@router.get("/models", response_model=ModelList,  tags=["Models"])
async def list_models():
    """ Replace with your actual list of models """
    available_models = [ModelCard(id=ModelCardName) for ModelCardName in chatbox.custom]
    return ModelList(data=available_models)



@router.post(
    "/deepmodel",
    response_model=None, 
    summary="Chat deepmodel",
    description="Creates a model response for the given chat conversation.",
    tags=["Chat"],
)
async def update_deepmodel(
    request: ChatCompletionRequestDeep,
    token: str = Depends(verify_api_key) # Uncomment to enable authentication
):
    try:
        # await chatbox.init_chatbox()
        prompt_for_llm_list = []
        for msgs in request.messages:
            if msgs.content:
                msgs_content = ""
                for msg in msgs.content:
                    if msg.type == 'text':
                        msgs_content += f"{msg.text}\n"
                    else:
                        pass
                            
            prompt_for_llm_list.append(f"{msgs.role}: {msgs_content}")

        prompt_for_llm = "\n".join(prompt_for_llm_list)
        
        return await chatbox.chat_with_deepmodel(prompt_with_history = prompt_for_llm,user_id = request.user_id,topic = request.topic)
    except Exception as e:
        raise HTTPException(status_code=500, 
                            detail=f"Error Info: {e}",) from e


@router.post(
    "/chat/completions",
    response_model=None, 
    summary="Chat Completions",
    description="Creates a model response for the given chat conversation.",
    tags=["Chat"],
)
async def create_chat_completion(
    request: ChatCompletionRequest,
    token: str = Depends(verify_api_key) # Uncomment to enable authentication
):
    """ use """
    # --- 1. Prepare Prompt for your LLM ---
    # This is highly dependent on your specific model.
    # You might concatenate messages, add special tokens, etc.
    # Example simplistic prompt concatenation:
 
    prompt_for_llm_list = []
    for msgs in request.messages:
        if msgs.content:
            msgs_content = ""
            for msg in msgs.content:
                if msg.type == 'text':
                    msgs_content += f"{msg.text}\n"
                else:
                    pass
                           
        prompt_for_llm_list.append(f"{msgs.role}: {msgs_content}")


    prompt_for_llm = "\n".join(prompt_for_llm_list)



    # --- 2. Call your LLM Backend ---
    # Pass necessary parameters like temperature, max_tokens etc. from the request
    try:
        response_data = await generate_llm_response(
            prompt=prompt_for_llm,
            stream=request.stream,
            user_id = request.user_id,
            topic = request.topic,
            model=request.model # Echo back the requested model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM backend error: {str(e)}") from e


    # --- 3. Format and Return Response ---
    if request.stream:
        if not isinstance(response_data, EventSourceResponse):
            raise HTTPException(status_code=500, detail=
                                 "Streaming response was not generated correctly.")
        return response_data # Return the SSE stream directly
    else:
        if not isinstance(response_data, ChatCompletionResponse):
            raise HTTPException(status_code=500,
                                 detail="Non-streaming response was not generated correctly.")
        
        return response_data # FastAPI automatically converts Pydantic model to JSON


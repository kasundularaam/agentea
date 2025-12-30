import json
import logging
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sse_starlette import EventSourceResponse

from injection import DevContainer
from src.application.reply_message import ReplyMessage

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/reply")
@inject
async def reply(new_message: str, generator: ReplyMessage = Depends(Provide[DevContainer.reply_usecase])):
    """
    Standard HTTP endpoint that waits for the full response.
    Returns: JSON {"response": "..."}
    """
    try:
        response = await generator.generate(new_message=new_message)
        return JSONResponse(content={"response": response}, status_code=HTTPStatus.OK)

    except Exception as e:
        logger.error(f"Error processing reply request: {e}", exc_info=True)
        return JSONResponse(content={"error": "Internal server error occurred", "detail": str(e)},
                            status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


@router.post("/stream")
@inject
async def reply_stream(new_message: str, generator: ReplyMessage = Depends(Provide[DevContainer.reply_usecase])):
    async def safe_stream_wrapper(stream_gen):
        try:
            async for chunk in stream_gen:
                payload = {"response": chunk}
                yield {"data": payload}

        except Exception as e:
            logger.error(f"Stream interrupted: {e}", exc_info=True)
            yield {"event": "error", "data": json.dumps({"error": "Stream interrupted", "detail": str(e)})}

    try:
        stream = generator.stream(new_message=new_message)
        return EventSourceResponse(safe_stream_wrapper(stream))  # type: ignore
    except Exception as e:
        logger.error(f"Failed to initialize stream: {e}", exc_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Could not start stream")

from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def root():
    return JSONResponse(content={"message": "Your Helpful Agent is running."}, status_code=HTTPStatus.OK)

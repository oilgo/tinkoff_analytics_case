from fastapi import (
    APIRouter,
    status
)
from .schemas import PurcaseRequest
from .services import _purchase_info


router = APIRouter(
    prefix="/purchase",
    tags=["Запись информации о покупках по партнерской акции"])

@router.post(
    path="/info",
    status_code=status.HTTP_200_OK,)
async def purchase_info(
    request: PurcaseRequest
):
    """ Endpoint для получения информации о покупках по партнерской акции
    """
    await _purchase_info(request)
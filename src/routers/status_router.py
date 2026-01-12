import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from injection import DevContainer
from src.domain.ports.remote_instruction_port import InstructionPort
from src.domain.ports.observer_port import ObserverPort
from src.domain.status.service_status import ServiceStatus

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/system", tags=["System Health & Controls"])


# --- OBSERVER SERVICE ENDPOINTS ---

@router.get("/observer_service", response_model=ServiceStatus)
@inject
async def observer_service_status(service: ObserverPort = Depends(Provide[DevContainer.observer_adapter])):
    return service.health_check()


@router.post("/observer_service/enable", response_model=ServiceStatus)
@inject
async def observer_service_enable(service: ObserverPort = Depends(Provide[DevContainer.observer_adapter])):
    service.enable()
    return service.health_check()


@router.post("/observer_service/disable", response_model=ServiceStatus)
@inject
async def observer_service_disable(service: ObserverPort = Depends(Provide[DevContainer.observer_adapter])):
    service.disable()
    return service.health_check()


# --- INSTRUCTION SERVICE ENDPOINTS ---

@router.get("/instructions_service", response_model=ServiceStatus)
@inject
async def instructions_service_status(service: InstructionPort = Depends(Provide[DevContainer.instruction_adapter])):
    return service.health_check()


@router.post("/instructions_service/enable", response_model=ServiceStatus)
@inject
async def instructions_service_enable(service: InstructionPort = Depends(Provide[DevContainer.instruction_adapter])):
    service.enable()
    return service.health_check()


@router.post("/instructions_service/disable", response_model=ServiceStatus)
@inject
async def instructions_service_disable(service: InstructionPort = Depends(Provide[DevContainer.instruction_adapter])):
    service.disable()
    return service.health_check()

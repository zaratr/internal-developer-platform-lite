from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from pathlib import Path
from platform.cli.idp import create_service, get_available_templates, ROOT

router = APIRouter()

class ServiceCreate(BaseModel):
    name: str
    template: str
    ai_enhance: bool = False

class ServiceResponse(BaseModel):
    name: str
    path: str
    template: Optional[str] = None
    status: str = "Active"

@router.get("/", response_model=List[ServiceResponse])
async def list_services():
    examples_dir = ROOT / "examples"
    services = []
    if examples_dir.exists():
        for p in examples_dir.iterdir():
            if p.is_dir():
                # Naive check: if it has a Dockerfile, it's a service
                if (p / "Dockerfile").exists():
                    services.append(ServiceResponse(
                        name=p.name,
                        path=str(p),
                        status="Active"
                    ))
    return services

@router.get("/templates")
async def list_templates_endpoint():
    return get_available_templates()

@router.post("/", response_model=ServiceResponse)
async def create_new_service(service: ServiceCreate):
    try:
        # Check against list of available templates
        if service.template not in get_available_templates():
             raise HTTPException(status_code=400, detail=f"Invalid template. Available: {get_available_templates()}")

        path = create_service(
            name=service.name, 
            template_name=service.template,
            ai_enhance=service.ai_enhance
        )
        return ServiceResponse(
            name=service.name,
            path=str(path),
            template=service.template
        )
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

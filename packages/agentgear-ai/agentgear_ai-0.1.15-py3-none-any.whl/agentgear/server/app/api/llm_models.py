from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.db import get_db
from agentgear.server.app.models import LLMModel

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("", response_model=List[schemas.LLMModelRead])
def list_models(db: Session = Depends(get_db)):
    return db.query(LLMModel).all()


@router.post("", response_model=schemas.LLMModelRead, status_code=status.HTTP_201_CREATED)
def create_model(payload: schemas.LLMModelCreate, db: Session = Depends(get_db)):
    model = LLMModel(
        name=payload.name,
        provider=payload.provider,
        api_key=payload.api_key,
        base_url=payload.base_url,
        config=payload.config
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_model(model_id: str, db: Session = Depends(get_db)):
    model = db.query(LLMModel).filter(LLMModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    db.delete(model)
    db.commit()

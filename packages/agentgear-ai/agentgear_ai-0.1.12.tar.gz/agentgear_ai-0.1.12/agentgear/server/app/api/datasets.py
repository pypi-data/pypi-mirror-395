from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from agentgear.server.app import schemas
from agentgear.server.app.config import get_settings
from agentgear.server.app.db import get_db
from agentgear.server.app.models import Dataset, DatasetExample, Project
from agentgear.server.app.deps import require_scopes

router = APIRouter(prefix="/api/datasets", tags=["datasets"])

@router.post("", response_model=schemas.DatasetRead, status_code=status.HTTP_201_CREATED)
def create_dataset(
    payload: schemas.DatasetCreate,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["datasets.write"])),
):
    settings = get_settings()
    # RBAC check
    if not settings.local_mode and request.state.project_id and request.state.project_id != payload.project_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    dataset = Dataset(
        project_id=payload.project_id,
        name=payload.name,
        description=payload.description,
        tags=payload.tags,
        metadata_=payload.metadata
    )
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset

@router.get("", response_model=List[schemas.DatasetRead])
def list_datasets(
    project_id: str | None = Query(default=None),
    request: Request = None,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["datasets.read"])),
):
    settings = get_settings()
    query = db.query(Dataset)
    
    # Filter by user's project if strict mode
    if not settings.local_mode and request.state.project_id:
        query = query.filter(Dataset.project_id == request.state.project_id)
    elif project_id:
        query = query.filter(Dataset.project_id == project_id)
        
    return query.order_by(Dataset.created_at.desc()).all()

@router.get("/{dataset_id}", response_model=schemas.DatasetRead)
def get_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["datasets.read"])),
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.post("/{dataset_id}/examples", response_model=schemas.DatasetExampleRead)
def create_example(
    dataset_id: str,
    payload: schemas.DatasetExampleCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["datasets.write"])),
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    example = DatasetExample(
        dataset_id=dataset_id,
        input_text=payload.input_text,
        expected_output=payload.expected_output,
        metadata_=payload.metadata
    )
    db.add(example)
    db.commit()
    db.refresh(example)
    return example

@router.get("/{dataset_id}/examples", response_model=List[schemas.DatasetExampleRead])
def list_examples(
    dataset_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["datasets.read"])),
):
    return db.query(DatasetExample).filter(DatasetExample.dataset_id == dataset_id).all()

@router.delete("/{dataset_id}/examples/{example_id}", status_code=204)
def delete_example(
    dataset_id: str,
    example_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["datasets.write"])),
):
    example = db.query(DatasetExample).filter(DatasetExample.id == example_id, DatasetExample.dataset_id == dataset_id).first()
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    
    db.delete(example)
    db.commit()

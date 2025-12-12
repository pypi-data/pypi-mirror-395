from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status, UploadFile, File
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
    pid = payload.project_id or request.state.project_id
    if not pid:
         # Fallback to default project if local mode or loose auth? 
         # Ideally request.state.project_id is always set by auth middleware.
         raise HTTPException(status_code=400, detail="Project ID required")

    if not settings.local_mode and request.state.project_id and request.state.project_id != pid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project mismatch")

    dataset = Dataset(
        project_id=pid,
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

@router.post("/{dataset_id}/upload", status_code=201)
async def upload_dataset_file(
    dataset_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: None = Depends(require_scopes(["datasets.write"])),
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    content = await file.read()
    filename = file.filename.lower()
    
    examples_to_add = []
    
    import csv
    import json
    import io

    try:
        if filename.endswith(".csv"):
            # Expect header: input, output (optional)
            text = content.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            for row in reader:
                # Flexible column matching
                input_text = row.get("input") or row.get("input_text") or row.get("prompt")
                expected_output = row.get("output") or row.get("expected_output") or row.get("completion")
                
                if input_text:
                    examples_to_add.append({
                        "input_text": input_text,
                        "expected_output": expected_output
                    })
                    
        elif filename.endswith(".json"):
            data = json.loads(content)
            if isinstance(data, list):
                for item in data:
                    input_text = item.get("input") or item.get("input_text") or item.get("prompt")
                    expected_output = item.get("output") or item.get("expected_output") or item.get("completion")
                    if input_text:
                        examples_to_add.append({
                            "input_text": input_text,
                            "expected_output": expected_output
                        })
        else:
             raise HTTPException(status_code=400, detail="Unsupported file type. Use .csv or .json")
             
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if not examples_to_add:
        return {"message": "No valid examples found", "count": 0}

    # Bulk insert
    objects = [
        DatasetExample(
            dataset_id=dataset_id, 
            input_text=ex["input_text"], 
            expected_output=ex.get("expected_output")
        ) 
        for ex in examples_to_add
    ]
    db.add_all(objects)
    db.commit()
    
    return {"message": "Successfully uploaded examples", "count": len(objects)}

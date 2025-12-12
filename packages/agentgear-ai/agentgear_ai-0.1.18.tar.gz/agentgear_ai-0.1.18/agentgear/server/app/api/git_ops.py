
import subprocess
import os
import yaml
import json
import csv
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from agentgear.server.app.db import get_db
from agentgear.server.app.models import Prompt, Dataset, DatasetExample
from agentgear.server.app.deps import require_scopes

router = APIRouter(prefix="/api/git", tags=["git"])

class GitCommitRequest(BaseModel):
    message: str

class GitConfig(BaseModel):
    remote_url: str
    user_name: str | None = None
    user_email: str | None = None

def run_git(args: list[str], cwd: Path) -> str:
    try:
        result = subprocess.run(
            ["git"] + args, 
            cwd=str(cwd), 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Git error: {e.stderr}")

def export_data(db: Session, base_path: Path):
    data_dir = base_path / "agentgear_data"
    data_dir.mkdir(exist_ok=True)
    
    # Export Prompts
    prompts_dir = data_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    prompts = db.query(Prompt).all()
    for p in prompts:
        # Get latest version? Or all? Let's dump the prompt metadata and versions.
        # Simple for now: dump structure
        p_data = {
            "name": p.name,
            "description": p.description,
            "versions": [
                {"version": v.version, "content": v.content} for v in p.versions
            ]
        }
        safe_name = "".join([c if c.isalnum() else "_" for c in p.name])
        with open(prompts_dir / f"{safe_name}.yaml", "w") as f:
            yaml.dump(p_data, f)
            
    # Export Datasets
    datasets_dir = data_dir / "datasets"
    datasets_dir.mkdir(exist_ok=True)
    datasets = db.query(Dataset).all()
    for d in datasets:
        safe_name = "".join([c if c.isalnum() else "_" for c in d.name])
        # Export as CSV
        examples = db.query(DatasetExample).filter(DatasetExample.dataset_id == d.id).all()
        with open(datasets_dir / f"{safe_name}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["input", "output"])
            for ex in examples:
                writer.writerow([ex.input_text, ex.expected_output])

@router.get("/status")
def git_status():
    repo_path = Path.cwd() # Root of server execution?
    # We ideally want the root of the project where user stores data or code.
    # Assuming CWD for now, or user can configure.
    try:
        if not (repo_path / ".git").exists():
            return {"initialized": False}
        
        status = run_git(["status", "--short"], repo_path)
        branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"], repo_path)
        return {"initialized": True, "branch": branch, "changed": bool(status), "status_text": status}
    except Exception as e:
        return {"initialized": False, "error": str(e)}

@router.post("/init")
def git_init():
    repo_path = Path.cwd()
    if (repo_path / ".git").exists():
        return {"message": "Already initialized"}
    run_git(["init"], repo_path)
    return {"message": "Initialized git repository"}

@router.post("/commit")
def git_commit(payload: GitCommitRequest, db: Session = Depends(get_db)):
    repo_path = Path.cwd()
    if not (repo_path / ".git").exists():
        raise HTTPException(status_code=400, detail="Not a git repository")
    
    # Export Data
    try:
        export_data(db, repo_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {e}")
        
    # Git Add
    run_git(["add", "agentgear_data"], repo_path)
    
    # Check if anything to commit
    status = run_git(["status", "--porcelain"], repo_path)
    if not status:
        return {"message": "Nothing to commit"}
        
    run_git(["commit", "-m", payload.message], repo_path)
    return {"message": "Committed changes"}

@router.post("/push")
def git_push():
    repo_path = Path.cwd()
    try:
        out = run_git(["push"], repo_path)
        return {"message": "Push successful", "output": out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Push failed: {e}")

@router.post("/config")
def git_config(config: GitConfig):
    repo_path = Path.cwd()
    if config.remote_url:
        try:
            # check if remote exists
            remotes = run_git(["remote"], repo_path)
            if "origin" in remotes:
                run_git(["remote", "set-url", "origin", config.remote_url], repo_path)
            else:
                run_git(["remote", "add", "origin", config.remote_url], repo_path)
        except Exception as e:
             raise HTTPException(status_code=500, detail=f"Failed to set remote: {e}")
             
    if config.user_name:
        run_git(["config", "user.name", config.user_name], repo_path)
    if config.user_email:
        run_git(["config", "user.email", config.user_email], repo_path)
        
    return {"message": "Configuration updated"}

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db

from typing import Optional

from .models import HealthStatus
from .schemas import (
    TreeCreate,
    TreeUpdate,
    TreeResponse,
    TreeListResponse,
)
from . import crud

router = APIRouter()

@router.get("/")
def list_trees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of records"),
    health: Optional[HealthStatus] = Query(
        None, description="Filter by health status"
    ),
    search: Optional[str] = Query(
        None, description="Search in species or location"
    ),
    db: Session = Depends(get_db),
    ):
    # GET all trees
    trees, total = crud.get_trees(
        db=db,
        skip=skip,
        limit=limit,
        health=health,
        search=search,
    )
    return TreeListResponse(total=total, trees=trees)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_tree(
    tree: TreeCreate,
    db: Session = Depends(get_db)):
    # POST new tree
    return crud.create_tree(db=db, tree_data=tree)

@router.get("/{tree_id}")
def get_tree(tree_id: int, db: Session = Depends(get_db)):
    # GET single tree
    tree = crud.get_tree(db=db, tree_id=tree_id)
    if not tree:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tree with id {tree_id} not found",
        )
    return tree

@router.put("/{tree_id}")
def update_tree(
    tree_id: int,
    updates: TreeUpdate,
    db: Session = Depends(get_db),
    ):
    # PUT update tree
    updated = crud.update_tree(
        db=db,
        tree_id=tree_id,
        tree_data=updates,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tree with id {tree_id} not found",
        )
    return updated

@router.delete("/{tree_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tree(
    tree_id: int,
    db: Session = Depends(get_db)
    ):
    # DELETE tree
    deleted = crud.delete_tree(db=db, tree_id=tree_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tree with id {tree_id} not found",
        )
    return None
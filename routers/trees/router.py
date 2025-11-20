"""
Tree Router
FastAPI endpoints for tree management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from .models import HealthStatus
from .schemas import TreeCreate, TreeUpdate, TreeResponse, TreeListResponse
from . import crud

router = APIRouter()


@router.get("/", response_model=TreeListResponse)
def list_trees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Maximum records to return"),
    health_status: Optional[HealthStatus] = Query(None, description="Filter by health status"),
    search: Optional[str] = Query(None, description="Search in location"),
    db: Session = Depends(get_db)
):
    """
    List all trees with optional filtering
    - **skip**: Pagination offset
    - **limit**: Maximum number of results
    - **health_status**: Filter by health status (excellent, good, fair, poor, dead)
    - **search**: Search term for location (case-insensitive)
    """
    trees, total = crud.get_trees(
        db=db,
        skip=skip,
        limit=limit,
        health_status=health_status,
        search=search
    )
    return TreeListResponse(total=total, trees=trees)


@router.post("/", response_model=TreeResponse, status_code=status.HTTP_201_CREATED)
def create_tree(
    tree: TreeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new tree
    Provide all required tree information including:
    - Species and location
    - Health status
    """
    return crud.create_tree(db=db, tree_data=tree)


@router.get("/{tree_id}", response_model=TreeResponse)
def get_tree(
    tree_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific tree by ID
    Returns detailed information about a single tree.
    """
    tree = crud.get_tree(db=db, tree_id=tree_id)
    if not tree:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tree with id {tree_id} not found"
        )
    return tree


@router.put("/{tree_id}", response_model=TreeResponse)
def update_tree(
    tree_id: int,
    tree: TreeUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing tree
    All fields are optional - only provided fields will be updated.
    Use this to update inspection dates, health status, or any other tree information.
    """
    updated_tree = crud.update_tree(db=db, tree_id=tree_id, tree_data=tree)
    if not updated_tree:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tree with id {tree_id} not found"
        )
    return updated_tree


@router.delete("/{tree_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tree(
    tree_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a tree
    Permanently removes a tree from the system.
    Returns 204 No Content on success.
    """
    deleted = crud.delete_tree(db=db, tree_id=tree_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tree with id {tree_id} not found"
        )
    return None
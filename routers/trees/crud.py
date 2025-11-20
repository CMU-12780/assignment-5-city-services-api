"""
Tree CRUD operations
Database operations for trees
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, Tuple, List
from .models import Tree, HealthStatus
from .schemas import TreeCreate, TreeUpdate


def get_trees(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    health_status: Optional[HealthStatus] = None,
    search: Optional[str] = None
) -> Tuple[List[Tree], int]:
    """
    Get list of trees with optional filtering

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        health_status: Filter by health status
        search: Search term for location

    Returns:
        Tuple of (list of trees, total count)
    """
    query = db.query(Tree)

    # Apply filters
    if health_status:
        query = query.filter(Tree.health_status == health_status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Tree.location.ilike(search_term)
        )

    # Get total count before pagination
    total = query.count()

    # Apply pagination and get results
    trees = query.offset(skip).limit(limit).all()

    return trees, total


def get_tree(db: Session, tree_id: int) -> Optional[Tree]:
    """
    Get a specific tree by ID

    Args:
        db: Database session
        tree_id: Tree ID

    Returns:
        Tree object or None if not found
    """
    return db.query(Tree).filter(Tree.id == tree_id).first()


def create_tree(db: Session, tree_data: TreeCreate) -> Tree:
    """
    Create a new tree

    Args:
        db: Database session
        tree_data: Tree creation data

    Returns:
        Created tree object
    """
    tree = Tree(**tree_data.model_dump())
    db.add(tree)
    db.commit()
    db.refresh(tree)
    return tree


def update_tree(
    db: Session,
    tree_id: int,
    tree_data: TreeUpdate
) -> Optional[Tree]:
    """
    Update an existing tree

    Args:
        db: Database session
        tree_id: Tree ID
        tree_data: Tree update data

    Returns:
        Updated tree object or None if not found
    """
    tree = get_tree(db, tree_id)
    if not tree:
        return None

    # Update only provided fields
    update_data = tree_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tree, field, value)

    db.commit()
    db.refresh(tree)
    return tree


def delete_tree(db: Session, tree_id: int) -> bool:
    """
    Delete a tree

    Args:
        db: Database session
        tree_id: Tree ID

    Returns:
        True if deleted, False if not found
    """
    tree = get_tree(db, tree_id)
    if not tree:
        return False

    db.delete(tree)
    db.commit()
    return True
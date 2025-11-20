from sqlalchemy.orm import Session
from typing import Optional
from .models import Tree, HealthStatus
from .schemas import TreeCreate, TreeUpdate

from sqlalchemy import or_

def get_trees(db: Session,
             skip: int = 0,
             limit: int = 100,
             health: Optional[HealthStatus] = None,
             search: Optional[str] = None
             ) -> tuple[list[Tree], int]:
    # Implementation
    query = db.query(Tree)

    if health:
        query = query.filter(Tree.health_status == health)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Tree.species.ilike(search_term),
                Tree.location.ilike(search_term)
            )
        )

    total = query.count()
    trees = query.offset(skip).limit(limit).all()
    return trees, total

def get_tree(db: Session, tree_id: int) -> Optional[Tree]:
    # Implementation
    return db.query(Tree).filter(Tree.id == tree_id).first()

def create_tree(db: Session, tree_data: TreeCreate) -> Tree:
    # Implementation
    tree = Tree(**tree_data.model_dump())
    db.add(tree)
    db.commit()
    db.refresh(tree)
    return tree

def update_tree(db: Session, 
                tree_id: int, 
                tree_data: TreeUpdate) -> Optional[Tree]:
    # Implementation
    tree = get_tree(db, tree_id)
    if not tree:
        return None
    
    update_data = tree_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tree, field, value)

    db.commit()
    db.refresh(tree)
    return tree

def delete_tree(db: Session, tree_id: int) -> bool:
    # Implementation
    tree = get_tree(db, tree_id)
    if not tree:
        return False

    db.delete(tree)
    db.commit()
    return True
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database import get_db
from app.services.cat_api import validate_breed

router = APIRouter(prefix="/cats", tags=["Spy Cats"])


@router.post("/", response_model=schemas.SpyCat, status_code=status.HTTP_201_CREATED)
async def create_spy_cat(cat: schemas.SpyCatCreate, db: Session = Depends(get_db)):
    """
    Create a new spy cat.
    Validates breed using TheCatAPI.
    """
    is_valid_breed = await validate_breed(cat.breed)
    if not is_valid_breed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid breed: {cat.breed}. Please provide a valid cat breed."
        )

    return crud.create_spy_cat(db=db, cat=cat)


@router.get("/", response_model=List[schemas.SpyCat])
def list_spy_cats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all spy cats.
    """
    cats = crud.get_spy_cats(db, skip=skip, limit=limit)
    return cats


@router.get("/{cat_id}", response_model=schemas.SpyCat)
def get_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    """
    Get a single spy cat by ID.
    """
    cat = crud.get_spy_cat(db, cat_id=cat_id)
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spy cat not found"
        )
    return cat


@router.patch("/{cat_id}", response_model=schemas.SpyCat)
def update_spy_cat(cat_id: int, cat_update: schemas.SpyCatUpdate, db: Session = Depends(get_db)):
    """
    Update spy cat salary.
    """
    cat = crud.update_spy_cat_salary(db, cat_id=cat_id, salary=cat_update.salary)
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spy cat not found"
        )
    return cat


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    """
    Delete a spy cat from the system.
    """
    success = crud.delete_spy_cat(db, cat_id=cat_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spy cat not found"
        )
    return None

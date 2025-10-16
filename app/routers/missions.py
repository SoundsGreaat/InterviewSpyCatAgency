from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.post("/", response_model=schemas.Mission, status_code=status.HTTP_201_CREATED)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    """
    Create a new mission with targets.
    Targets are created along with the mission (1-3 targets).
    """
    return crud.create_mission(db=db, mission=mission)


@router.get("/", response_model=List[schemas.MissionDetail])
def list_missions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all missions with their targets and assigned cats.
    """
    missions = crud.get_missions(db, skip=skip, limit=limit)
    return missions


@router.get("/{mission_id}", response_model=schemas.MissionDetail)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    """
    Get a single mission by ID with its targets and assigned cat.
    """
    mission = crud.get_mission(db, mission_id=mission_id)
    if mission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found"
        )
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    """
    Delete a mission.
    Cannot delete if mission is assigned to a cat.
    """
    mission = crud.get_mission(db, mission_id=mission_id)
    if mission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found"
        )

    if mission.cat_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete mission that is assigned to a cat"
        )

    success = crud.delete_mission(db, mission_id=mission_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete mission"
        )
    return None


@router.post("/{mission_id}/assign", response_model=schemas.Mission)
def assign_cat_to_mission(
        mission_id: int,
        assignment: schemas.MissionAssignCat,
        db: Session = Depends(get_db)
):
    """
    Assign a cat to a mission.
    A cat can only have one active mission at a time.
    """
    mission = crud.get_mission(db, mission_id=mission_id)
    if mission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found"
        )

    if mission.cat_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mission is already assigned to a cat"
        )

    cat = crud.get_spy_cat(db, cat_id=assignment.cat_id)
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spy cat not found"
        )

    if crud.cat_has_active_mission(db, cat_id=assignment.cat_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cat already has an active mission"
        )

    updated_mission = crud.assign_cat_to_mission(db, mission_id=mission_id, cat_id=assignment.cat_id)
    if updated_mission is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to assign cat to mission"
        )

    return updated_mission


@router.patch("/{mission_id}/targets/{target_id}", response_model=schemas.Target)
def update_target(
        mission_id: int,
        target_id: int,
        target_update: schemas.TargetUpdate,
        db: Session = Depends(get_db)
):
    """
    Update a target's notes and/or completion status.
    Notes cannot be updated if the target or mission is complete.
    """
    target = crud.get_target(db, target_id=target_id)
    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found"
        )

    if target.mission_id != mission_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target does not belong to this mission"
        )

    if target_update.notes is not None and (target.is_complete or target.mission.is_complete):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update notes. Target or mission is already complete."
        )

    updated_target = crud.update_target(db, target_id=target_id, target_update=target_update)
    if updated_target is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update target"
        )

    return updated_target

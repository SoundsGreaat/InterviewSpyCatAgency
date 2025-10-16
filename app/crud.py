from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas


def get_spy_cat(db: Session, cat_id: int) -> Optional[models.SpyCat]:
    return db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()


def get_spy_cats(db: Session, skip: int = 0, limit: int = 100) -> List[models.SpyCat]:
    return db.query(models.SpyCat).offset(skip).limit(limit).all()


def create_spy_cat(db: Session, cat: schemas.SpyCatCreate) -> models.SpyCat:
    db_cat = models.SpyCat(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def update_spy_cat_salary(db: Session, cat_id: int, salary: float) -> Optional[models.SpyCat]:
    db_cat = get_spy_cat(db, cat_id)
    if db_cat:
        db_cat.salary = salary
        db.commit()
        db.refresh(db_cat)
    return db_cat


def delete_spy_cat(db: Session, cat_id: int) -> bool:
    db_cat = get_spy_cat(db, cat_id)
    if db_cat:
        db.delete(db_cat)
        db.commit()
        return True
    return False


def cat_has_active_mission(db: Session, cat_id: int) -> bool:
    active_mission = db.query(models.Mission).filter(
        models.Mission.cat_id == cat_id,
        models.Mission.is_complete == False
    ).first()
    return active_mission is not None


def get_mission(db: Session, mission_id: int) -> Optional[models.Mission]:
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()


def get_missions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Mission]:
    return db.query(models.Mission).offset(skip).limit(limit).all()


def create_mission(db: Session, mission: schemas.MissionCreate) -> models.Mission:
    db_mission = models.Mission()
    db.add(db_mission)
    db.flush()

    for target_data in mission.targets:
        db_target = models.Target(
            mission_id=db_mission.id,
            **target_data.model_dump()
        )
        db.add(db_target)

    db.commit()
    db.refresh(db_mission)
    return db_mission


def delete_mission(db: Session, mission_id: int) -> bool:
    db_mission = get_mission(db, mission_id)
    if db_mission and db_mission.cat_id is None:
        db.delete(db_mission)
        db.commit()
        return True
    return False


def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int) -> Optional[models.Mission]:
    db_mission = get_mission(db, mission_id)
    if db_mission and db_mission.cat_id is None:
        db_mission.cat_id = cat_id
        db.commit()
        db.refresh(db_mission)
        return db_mission
    return None


def get_target(db: Session, target_id: int) -> Optional[models.Target]:
    return db.query(models.Target).filter(models.Target.id == target_id).first()


def update_target(db: Session, target_id: int, target_update: schemas.TargetUpdate) -> Optional[models.Target]:
    db_target = get_target(db, target_id)

    if not db_target:
        return None

    if db_target.is_complete or db_target.mission.is_complete:
        if target_update.notes is not None:
            return None

    if target_update.notes is not None and not db_target.is_complete and not db_target.mission.is_complete:
        db_target.notes = target_update.notes

    if target_update.is_complete is not None:
        db_target.is_complete = target_update.is_complete

        if target_update.is_complete:
            all_complete = all(t.is_complete for t in db_target.mission.targets)
            if all_complete:
                db_target.mission.is_complete = True

    db.commit()
    db.refresh(db_target)
    return db_target

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class SpyCatBase(BaseModel):
    name: str = Field(..., min_length=1)
    years_of_experience: int = Field(..., ge=0)
    breed: str = Field(..., min_length=1)
    salary: float = Field(..., gt=0)


class SpyCatCreate(SpyCatBase):
    pass


class SpyCatUpdate(BaseModel):
    salary: float = Field(..., gt=0)


class SpyCat(SpyCatBase):
    id: int

    class Config:
        from_attributes = True


class TargetBase(BaseModel):
    name: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    notes: str = Field(default="")
    is_complete: bool = Field(default=False)


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None


class Target(TargetBase):
    id: int
    mission_id: int

    class Config:
        from_attributes = True


class MissionBase(BaseModel):
    is_complete: bool = Field(default=False)


class MissionCreate(BaseModel):
    targets: List[TargetCreate] = Field(..., min_length=1, max_length=3)

    @field_validator('targets')
    @classmethod
    def validate_targets_count(cls, v):
        if len(v) < 1 or len(v) > 3:
            raise ValueError('Mission must have between 1 and 3 targets')
        return v


class MissionAssignCat(BaseModel):
    cat_id: int


class Mission(MissionBase):
    id: int
    cat_id: Optional[int] = None
    targets: List[Target] = []

    class Config:
        from_attributes = True


class MissionDetail(Mission):
    cat: Optional[SpyCat] = None

    class Config:
        from_attributes = True

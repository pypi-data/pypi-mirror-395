"""
Hero models and DTOs
"""
from typing import Optional
from sqlmodel import SQLModel, Field


class HeroBase(SQLModel):
    """Base Hero model with common fields"""
    name: str = Field(min_length=2, max_length=120)
    secret_name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=200)


class Hero(HeroBase, table=True):
    """Hero database model"""
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class HeroCreate(HeroBase):
    """Schema for creating a new hero"""
    pass


class HeroUpdate(HeroBase):
    """Schema for updating a hero"""
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    secret_name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=200)


class HeroRead(HeroBase):
    """Schema for reading a hero"""
    id: int
    model_config = {"from_attributes": True}
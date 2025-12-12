"""
Hero repository for database operations
"""
from typing import List, Optional
from sqlmodel import Session, select
from .models import Hero, HeroCreate, HeroUpdate


class HeroRepository:
    """Repository for Hero database operations"""
    
    def get(self, session: Session, hero_id: int) -> Optional[Hero]:
        """Get a hero by ID"""
        return session.get(Hero, hero_id)
    
    def list(self, session: Session, offset: int = 0, limit: int = 100) -> List[Hero]:
        """List heroes with pagination"""
        stmt = select(Hero).offset(offset).limit(limit)
        return list(session.exec(stmt))
    
    def create(self, session: Session, hero_data: HeroCreate) -> Hero:
        """Create a new hero"""
        hero = Hero.model_validate(hero_data)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero
    
    def update(self, session: Session, hero: Hero, hero_data: HeroUpdate) -> Hero:
        """Update an existing hero"""
        data_dict = hero_data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(hero, key, value)
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero
    
    def delete(self, session: Session, hero: Hero) -> None:
        """Delete a hero"""
        session.delete(hero)
        session.commit()
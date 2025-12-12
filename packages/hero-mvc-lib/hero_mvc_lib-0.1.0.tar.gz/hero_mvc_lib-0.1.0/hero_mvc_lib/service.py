"""
Hero service layer for business logic
"""
from typing import List, Optional
from sqlmodel import Session
from .repository import HeroRepository
from .models import Hero, HeroCreate, HeroUpdate
from .database import get_hero_session


class HeroService:
    """Service layer for Hero business logic"""
    
    def __init__(self):
        self.repository = HeroRepository()
    
    def get_hero(self, hero_id: int, session: Optional[Session] = None) -> Optional[Hero]:
        """Get a hero by ID"""
        if session is None:
            session_gen = get_hero_session()
            session = next(session_gen)
        
        return self.repository.get(session, hero_id)
    
    def list_heroes(self, offset: int = 0, limit: int = 100, session: Optional[Session] = None) -> List[Hero]:
        """List heroes with pagination"""
        if session is None:
            session_gen = get_hero_session()
            session = next(session_gen)
        
        return self.repository.list(session, offset, limit)
    
    def create_hero(self, hero_data: HeroCreate, session: Optional[Session] = None) -> Hero:
        """Create a new hero"""
        if session is None:
            session_gen = get_hero_session()
            session = next(session_gen)
        
        return self.repository.create(session, hero_data)
    
    def update_hero(self, hero_id: int, hero_data: HeroUpdate, session: Optional[Session] = None) -> Optional[Hero]:
        """Update an existing hero"""
        if session is None:
            session_gen = get_hero_session()
            session = next(session_gen)
        
        hero = self.repository.get(session, hero_id)
        if not hero:
            return None
        
        return self.repository.update(session, hero, hero_data)
    
    def delete_hero(self, hero_id: int, session: Optional[Session] = None) -> bool:
        """Delete a hero"""
        if session is None:
            session_gen = get_hero_session()
            session = next(session_gen)
        
        hero = self.repository.get(session, hero_id)
        if not hero:
            return False
        
        self.repository.delete(session, hero)
        return True
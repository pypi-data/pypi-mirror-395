"""
Hero FastAPI controller/router
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from .database import get_hero_session
from .service import HeroService
from .models import Hero, HeroCreate, HeroUpdate, HeroRead


def get_hero_router() -> APIRouter:
    """Get the Hero FastAPI router"""
    router = APIRouter(prefix="/heroes", tags=["heroes"])
    hero_service = HeroService()
    
    @router.post("/", response_model=HeroRead, status_code=201)
    def create_hero(hero_data: HeroCreate, session: Session = Depends(get_hero_session)):
        """Create a new hero"""
        return hero_service.create_hero(hero_data, session)
    
    @router.get("/", response_model=List[HeroRead])
    def list_heroes(
        session: Session = Depends(get_hero_session),
        offset: int = 0,
        limit: int = Query(100, le=200)
    ):
        """List all heroes"""
        return hero_service.list_heroes(offset, limit, session)
    
    @router.get("/{hero_id}", response_model=HeroRead)
    def get_hero(hero_id: int, session: Session = Depends(get_hero_session)):
        """Get a hero by ID"""
        hero = hero_service.get_hero(hero_id, session)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero
    
    @router.patch("/{hero_id}", response_model=HeroRead)
    def update_hero(hero_id: int, hero_data: HeroUpdate, session: Session = Depends(get_hero_session)):
        """Update a hero"""
        hero = hero_service.update_hero(hero_id, hero_data, session)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero
    
    @router.delete("/{hero_id}", status_code=204)
    def delete_hero(hero_id: int, session: Session = Depends(get_hero_session)):
        """Delete a hero"""
        success = hero_service.delete_hero(hero_id, session)
        if not success:
            raise HTTPException(status_code=404, detail="Hero not found")
    
    return router
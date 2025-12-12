"""
Hero MVC Library - A simple MVC library for Hero management
"""

__version__ = "0.1.0"

# Import modules to make them available
from . import database
from . import models
from . import repository
from . import service
from . import controller

# Import specific classes and functions for convenience
from .database import init_hero_db, get_hero_session
from .service import HeroService
from .controller import get_hero_router
from .models import Hero, HeroCreate, HeroUpdate, HeroRead

__all__ = [
    "init_hero_db",
    "get_hero_session", 
    "HeroService",
    "get_hero_router",
    "Hero",
    "HeroCreate", 
    "HeroUpdate",
    "HeroRead",
    "database",
    "models", 
    "repository",
    "service",
    "controller",
]
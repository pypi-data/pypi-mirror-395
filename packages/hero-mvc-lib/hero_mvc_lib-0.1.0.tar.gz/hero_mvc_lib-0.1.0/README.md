# Hero MVC Library

A simple, clean MVC (Model-View-Controller) library for Hero management with in-memory database support.

## Features

- Clean MVC architecture
- Generic CRUD operations
- In-memory SQLite database support
- FastAPI integration
- Type-safe with Pydantic models
- Extensible hooks system

## Installation

```bash
pip install hero-mvc-lib
```

## Quick Start

```python
from hero_mvc_lib import HeroService, init_hero_db
from hero_mvc_lib.models import HeroCreate

# Initialize the database
init_hero_db()

# Create a hero service
hero_service = HeroService()

# Create a new hero
hero_data = HeroCreate(name="Superman", secret_name="Clark Kent", age=30)
hero = hero_service.create_hero(hero_data)

print(f"Created hero: {hero.name}")
```

## Usage with FastAPI

```python
from fastapi import FastAPI
from hero_mvc_lib import get_hero_router, init_hero_db

app = FastAPI()

# Initialize database
init_hero_db()

# Include hero routes
app.include_router(get_hero_router(), prefix="/api")
```

## License

MIT License
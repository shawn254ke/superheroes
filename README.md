# Superheroes Flask API

This project implements a RESTful API for managing superheroes, their powers, and the relationships between them using Flask, SQLAlchemy, and Flask-Migrate.

## Models & Relationships

- **Hero**: Has many Powers through HeroPower
- **Power**: Has many Heroes through HeroPower
- **HeroPower**: Belongs to a Hero and a Power (with cascade deletes)

## Validations

- **HeroPower**: `strength` must be one of: `Strong`, `Weak`, `Average`
- **Power**: `description` must be present and at least 20 characters long

## API Endpoints

### GET /heroes
Returns a list of all heroes.

### GET /heroes/:id
Returns a hero with their powers. Returns 404 if not found.

### GET /powers
Returns a list of all powers.

### GET /powers/:id
Returns a power. Returns 404 if not found.

### PATCH /powers/:id
Updates a power's description. Returns errors if validation fails or 404 if not found.

### POST /hero_powers
Creates a new HeroPower. Returns errors if validation fails.

## Setup & Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `flask db upgrade`
3. Seed the database (see `seed.py` or use your own data)
4. Start the server: `flask run`


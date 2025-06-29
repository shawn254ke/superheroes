#!/usr/bin/env python3

from app import app
from models import db, Heroes, Power, HeroPower

def seed_data():
    with app.app_context():
        print("Clearing existing data...")
        # Clear existing data
        HeroPower.query.delete()
        Heroes.query.delete()
        Power.query.delete()
        
        print("Creating heroes...")
        # Create Heroes
        heroes_data = [
            {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
            {"name": "Doreen Green", "super_name": "Squirrel Girl"},
            {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
            {"name": "Janet Van Dyne", "super_name": "The Wasp"},
            {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
            {"name": "Carol Danvers", "super_name": "Captain Marvel"},
            {"name": "Jean Grey", "super_name": "Dark Phoenix"},
            {"name": "Ororo Munroe", "super_name": "Storm"},
            {"name": "Kitty Pryde", "super_name": "Shadowcat"},
            {"name": "Elektra Natchios", "super_name": "Elektra"}
        ]
        
        heroes = []
        for hero_data in heroes_data:
            hero = Heroes(name=hero_data["name"], super_name=hero_data["super_name"])
            heroes.append(hero)
            db.session.add(hero)
        
        print("Creating powers...")
        # Create Powers
        powers_data = [
            {
                "name": "super strength",
                "description": "gives the wielder super-human strengths"
            },
            {
                "name": "flight",
                "description": "gives the wielder the ability to fly through the skies at supersonic speed"
            },
            {
                "name": "super human senses",
                "description": "allows the wielder to use her senses at a super-human level"
            },
            {
                "name": "elasticity",
                "description": "can stretch the human body to extreme lengths"
            },
            {
                "name": "telekinesis",
                "description": "allows the wielder to move objects with their mind"
            },
            {
                "name": "energy projection",
                "description": "gives the wielder the ability to project various forms of energy"
            },
            {
                "name": "weather control",
                "description": "allows the wielder to control and manipulate weather patterns"
            },
            {
                "name": "phasing",
                "description": "gives the wielder the ability to phase through solid objects"
            },
            {
                "name": "enhanced agility",
                "description": "provides superhuman agility and acrobatic abilities"
            },
            {
                "name": "martial arts mastery",
                "description": "grants expert-level proficiency in various martial arts disciplines"
            }
        ]
        
        powers = []
        for power_data in powers_data:
            power = Power(name=power_data["name"], description=power_data["description"])
            powers.append(power)
            db.session.add(power)
        
        # Commit heroes and powers first
        db.session.commit()
        
        print("Creating hero-power relationships...")
        # Create HeroPower relationships
        hero_powers_data = [
            {"hero_id": 1, "power_id": 4, "strength": "Strong"},  # Ms. Marvel - elasticity
            {"hero_id": 1, "power_id": 1, "strength": "Average"},  # Ms. Marvel - super strength
            {"hero_id": 2, "power_id": 1, "strength": "Weak"},  # Squirrel Girl - super strength
            {"hero_id": 2, "power_id": 9, "strength": "Strong"},  # Squirrel Girl - enhanced agility
            {"hero_id": 3, "power_id": 1, "strength": "Strong"},  # Spider-Gwen - super strength
            {"hero_id": 3, "power_id": 3, "strength": "Strong"},  # Spider-Gwen - super human senses
            {"hero_id": 3, "power_id": 9, "strength": "Strong"},  # Spider-Gwen - enhanced agility
            {"hero_id": 4, "power_id": 2, "strength": "Strong"},  # The Wasp - flight
            {"hero_id": 4, "power_id": 6, "strength": "Average"},  # The Wasp - energy projection
            {"hero_id": 5, "power_id": 5, "strength": "Strong"},  # Scarlet Witch - telekinesis
            {"hero_id": 5, "power_id": 6, "strength": "Strong"},  # Scarlet Witch - energy projection
            {"hero_id": 6, "power_id": 2, "strength": "Strong"},  # Captain Marvel - flight
            {"hero_id": 6, "power_id": 1, "strength": "Strong"},  # Captain Marvel - super strength
            {"hero_id": 6, "power_id": 6, "strength": "Strong"},  # Captain Marvel - energy projection
            {"hero_id": 7, "power_id": 5, "strength": "Strong"},  # Dark Phoenix - telekinesis
            {"hero_id": 7, "power_id": 6, "strength": "Strong"},  # Dark Phoenix - energy projection
            {"hero_id": 7, "power_id": 2, "strength": "Strong"},  # Dark Phoenix - flight
            {"hero_id": 8, "power_id": 7, "strength": "Strong"},  # Storm - weather control
            {"hero_id": 8, "power_id": 2, "strength": "Strong"},  # Storm - flight
            {"hero_id": 9, "power_id": 8, "strength": "Strong"},  # Shadowcat - phasing
            {"hero_id": 9, "power_id": 10, "strength": "Average"},  # Shadowcat - martial arts mastery
            {"hero_id": 10, "power_id": 10, "strength": "Strong"},  # Elektra - martial arts mastery
            {"hero_id": 10, "power_id": 9, "strength": "Strong"},  # Elektra - enhanced agility
        ]
        
        for hp_data in hero_powers_data:
            hero_power = HeroPower(
                hero_id=hp_data["hero_id"],
                power_id=hp_data["power_id"],
                strength=hp_data["strength"]
            )
            db.session.add(hero_power)
        
        # Commit all changes
        db.session.commit()
        
        print("Seed data created successfully!")
        print(f"Created {len(heroes)} heroes")
        print(f"Created {len(powers)} powers")
        print(f"Created {len(hero_powers_data)} hero-power relationships")

if __name__ == "__main__":
    seed_data()

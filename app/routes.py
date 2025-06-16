from flask import request, jsonify
from app import app, db
from app.models import Hero, Power, HeroPower

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([h.to_dict() for h in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.to_dict(include_powers=True))

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([p.to_dict() for p in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.to_dict())

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    data = request.get_json()
    description = data.get('description')
    errors = []
    if not description or len(description) < 20:
        errors.append('Description must be at least 20 characters long')
    if errors:
        return jsonify({'errors': errors}), 400
    power.description = description
    db.session.commit()
    return jsonify(power.to_dict())

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')
    errors = []
    if strength not in ['Strong', 'Weak', 'Average']:
        errors.append('Strength must be Strong, Weak, or Average')
    if not Power.query.get(power_id):
        errors.append('Power not found')
    if not Hero.query.get(hero_id):
        errors.append('Hero not found')
    if errors:
        return jsonify({'errors': errors}), 400
    hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
    db.session.add(hero_power)
    db.session.commit()
    return jsonify(hero_power.to_dict(include_power=True, include_hero=True)), 201

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Heroes, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Heroes.query.all()
    return jsonify([hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes])

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Heroes.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    

    hero_data = hero.to_dict(only=('id', 'name', 'super_name', 'hero_powers'))
    
    
    hero_powers_data = []
    for hp in hero.hero_powers:
        hp_data = {
            'id': hp.id,
            'hero_id': hp.hero_id,
            'power_id': hp.power_id,
            'strength': hp.strength,
            'power': hp.power.to_dict(only=('id', 'name', 'description'))
        }
        hero_powers_data.append(hp_data)
    
    hero_data['hero_powers'] = hero_powers_data
    return jsonify(hero_data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict(only=('id', 'name', 'description')) for power in powers])

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    return jsonify(power.to_dict(only=('id', 'name', 'description')))

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            power.description = data['description']
        
        db.session.commit()
        return jsonify(power.to_dict(only=('id', 'name', 'description')))
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["An error occurred while updating the power"]}), 400

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    try:
        # Validate required fields
        if not all(key in data for key in ['strength', 'power_id', 'hero_id']):
            return jsonify({"errors": ["Missing required fields: strength, power_id, hero_id"]}), 400
        
        # Check if hero and power exist
        hero = Heroes.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])
        
        if not hero:
            return jsonify({"errors": ["Hero not found"]}), 400
        if not power:
            return jsonify({"errors": ["Power not found"]}), 400
        
        # Create new HeroPower
        hero_power = HeroPower(
            strength=data['strength'],
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        
        db.session.add(hero_power)
        db.session.commit()
        
        # Return the created HeroPower with nested hero and power data
        response_data = {
            'id': hero_power.id,
            'hero_id': hero_power.hero_id,
            'power_id': hero_power.power_id,
            'strength': hero_power.strength,
            'hero': hero_power.hero.to_dict(only=('id', 'name', 'super_name')),
            'power': hero_power.power.to_dict(only=('id', 'name', 'description'))
        }
        
        return jsonify(response_data), 201
    
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["An error occurred while creating the hero power"]}), 400

if __name__ == '__main__':
    app.run(debug=True)



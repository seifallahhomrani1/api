from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'{self.id} - {self.name} - {self.description}'

@app.route('/')
def index():


    return "Hello!"


@app.route('/drinks')
def get_drinks():
    drinks = drink.query.all()

    output = []
    for Drink in drinks :
        Drink_data = {'description':Drink.description,'name': Drink.name}
        output.append(Drink_data)
    
    return {"drinks": output}



@app.route('/drinks/<id>')

def get_drink(id): 
    Drink = drink.query.get_or_404(id)
    return {"name": Drink.name, "description": Drink.description}


@app.route('/drinks', methods=['POST'])

def add_drink():
    Drink = drink( description=request.json['description'], name=request.json['name'])
    db.session.add(Drink)
    db.session.commit()

    return {"id": Drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])

def delete_drink(id):
    Drink = drink.query.get(id)
    if Drink is None: 
        return {"ERROR": "Drink not found"}
    db.session.delete(Drink)
    db.session.commit()

    return {"Success": f"{Drink.name} Deleted"}




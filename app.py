from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from environs import Env
import os

app = Flask(__name__)
CORS(app)
heroku = Heroku(app)

# env = Env()
# env.read_env()
# DATABASE_URL = env("DATABASE_URL")


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Create ASL Table
class Asl(db.Model):
    __tablename__ = "asl"
    id = db.Column(db.Integer, primary_key=True)
    char = db.Column(db.String(10), nullable=False)
    imageWithChar = db.Column(db.String(500), nullable=False)
    imageWithoutChar = db.Column(db.String(500), nullable=False)

    def __init__(self, char, imageWithChar, imageWithoutChar):
        self.char = char
        self.imageWithChar = imageWithChar
        self.imageWithoutChar = imageWithoutChar


class AslSchema(ma.Schema):
    class Meta:
        fields = ('id', 'char', 'imageWithChar', 'imageWithoutChar')


asl_schema = AslSchema()
asls_schema = AslSchema(many=True)


# Create Table Braille
class Braille(db.Model):
    __tablename__ = "braille"
    id = db.Column(db.Integer, primary_key=True)
    char = db.Column(db.String(10), nullable=False)
    imageWithChar = db.Column(db.String(500), nullable=False)
    imageWithoutChar = db.Column(db.String(500), nullable=False)

    def __init__(self, char, imageWithChar, imageWithoutChar):
        self.char = char
        self.imageWithChar = imageWithChar
        self.imageWithoutChar = imageWithoutChar


class BrailleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'char', 'imageWithChar', 'imageWithoutChar')


braille_schema = BrailleSchema()
brailles_schema = BrailleSchema(many=True)


@app.route('/', methods=["GET"])
def home():
    return "<h1>ASL and Braille flashcard API</h1>"


# Endpoints for ASL -------------------------------------------------------
@app.route('/asl', methods=['POST'])
def add_asl():
    char = request.json['char']
    imageWithChar = request.json['imageWithChar']
    imageWithoutChar = request.json['imageWithoutChar']

    new_asl = Asl(char, imageWithChar, imageWithoutChar)

    db.session.add(new_asl)
    db.session.commit()

    asl = Asl.query.get(new_asl.id)
    return asl_schema.jsonify(asl)


@app.route('/asls', methods=["GET"])
def get_asls():
    all_asls = Asl.query.all()
    result = asls_schema.dump(all_asls)

    return jsonify(result)


@app.route('/asl/<id>', methods=['GET'])
def get_asl(id):
    asl = Asl.query.get(id)

    result = asl_schema.dump(asl)
    return jsonify(result)

# @app.route('/product/<id>', methods=['PATCH'])
# def update_category(id):
#     product = Product.query.get(id)

#     new_inventory = request.json['inventory']

#     product.inventory = new_inventory

#     db.session.commit()
#     return product_schema.jsonify(product)


@app.route('/asl/<id>', methods=['DELETE'])
def delete_asl(id):
    record = Asl.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')

# Endpoints for Braille -------------------------------------------------------
@app.route('/braille', methods=['POST'])
def add_braille():
    char = request.json['char']
    imageWithChar = request.json['imageWithChar']
    imageWithoutChar = request.json['imageWithoutChar']

    new_braille = Braille(char, imageWithChar, imageWithoutChar)

    db.session.add(new_braille)
    db.session.commit()

    braille = Braille.query.get(new_braille.id)
    return braille_schema.jsonify(braille)


@app.route('/brailles', methods=["GET"])
def get_brailles():
    all_brailles = Braille.query.all()
    result = brailles_schema.dump(all_brailles)

    return jsonify(result)


@app.route('/braille/<id>', methods=['GET'])
def get_braille(id):
    braille = Braille.query.get(id)

    result = braille_schema.dump(braille)
    return jsonify(result)


@app.route('/braille/<id>', methods=['DELETE'])
def delete_braille(id):
    record = Braille.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify('Item deleted')


if __name__ == "__main__":
    app.debug = True
    app.run()

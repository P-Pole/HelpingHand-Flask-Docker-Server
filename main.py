from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/flask_db'
CORS(app)

db = SQLAlchemy(app)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(200))
    user_id = db.Column(db.Integer)
    charities = db.Column(db.String(10000))
    subscription = db.Column(db.Boolean)
    amount = db.Column(db.Integer)

def model_to_dict(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}


@app.route('/transactions/', methods=['GET'])
def get_transactions():
    transactions = Transactions.query.all()
    response = jsonify([model_to_dict(transaction) for transaction in transactions])
    response.status_code =200
    return response

@app.route('/transactions/', methods=["POST"])
def add_transactions():
    data = request.get_json()
    new_transaction = Transactions(date=data['date'], user_id=data['user_id'], charities=data['charities'], subscription=data['subscription'], amount=data['amount'] )
    db.session.add(new_transaction)
    db.session.commit()
    response = jsonify(model_to_dict(new_transaction))
    response.status_code=201
    return response

@app.route('/transactions/<id>', methods=['PUT'])
def upgrade_transactions(id):
    transaction = Transactions.query.get(id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    transaction_data = request.get_json()
    transaction.date = transaction_data['date']
    transaction.user_id = transaction_data['user_id']
    transaction.charities = transaction_data['charities']

    db.session.commit()

    return jsonify(transaction.__dict__), 200

@app.route('/transactions/<id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transactions.query.get(id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction deleted successfully'}), 204

@app.route('/')
def index():
    return 'Hello'


if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')
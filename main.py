
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Set configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create user Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

# Create a Party Model
class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    category = db.Column(db.String(120))
    place = db.Column(db.String(120))
    address = db.Column(db.String(120))
    start_date = db.Column(db.String(120))
    end_date = db.Column(db.String(120))
    is_face_to_face = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create a registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template('registered.html')
    return render_template('register.html')

# Create a login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return render_template('logged_in.html')
        else:
            return render_template('wrong_details.html')
    return render_template('login.html')

# Create a create party page
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        place = request.form['place']
        address = request.form['address']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        is_face_to_face = request.form['is_face_to_face']
        user_id = request.form['user_id']
        party = Party(name=name, category=category, place=place, address=address, start_date=start_date, end_date=end_date, is_face_to_face=is_face_to_face, user_id=user_id)
        db.session.add(party)
        db.session.commit()
        return render_template('party_created.html')
    return render_template('create.html')

# Create an edit party page
@app.route('/edit/<int:party_id>', methods=['GET', 'POST'])
def edit(party_id):
    party = Party.query.filter_by(id=party_id).first()
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        place = request.form['place']
        address = request.form['address']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        is_face_to_face = request.form['is_face_to_face']
        user_id = request.form['user_id']
        party.name = name
        party.category = category
        party.place = place
        party.address = address
        party.start_date = start_date
        party.end_date = end_date
        party.is_face_to_face = is_face_to_face
        party.user_id = user_id
        db.session.commit()
        return render_template('party_edited.html')
    return render_template('edit.html', party=party)

# Create a delete party page
@app.route('/delete/<int:party_id>', methods=['GET', 'POST'])
def delete(party_id):
    party = Party.query.filter_by(id=party_id).first()
    if request.method == 'POST':
        db.session.delete(party)
        db.session.commit()
        return render_template('party_deleted.html')
    return render_template('delete.html', party=party)

# Create a list of parties page
@app.route('/list', methods=['GET', 'POST'])
def list():
    parties = Party.query.order_by(Party.id.desc()).all()
    return render_template('list.html', parties=parties)

if __name__ == '__main__':
    app.run(debug=True)
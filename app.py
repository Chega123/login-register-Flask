'''Ejemplo de login y register con el framework flask'''
from flask import Flask, request, render_template,redirect,session,jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'clavecita:D'
class  User(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    lastname=db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100), unique=True)
    password=db.Column(db.String(100))
    number=db.Column(db.Integer)

    def __init__(self, name, lastname, email, password, number):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.number=number

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect('/index')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/index')


@app.route('/signup',methods=['GET','POST'])
def register():
    if request.method=='POST':
        if request.get_json():
            name = request.get_json().get("name")
            lastname = request.get_json().get("lastname")
            email = request.get_json().get("email")
            password = request.get_json().get("password")
            number = request.get_json().get("phonenumber")

            existing_user=User.query.filter_by(email=email).first()
            if not existing_user:
                new_user=User(name=name,lastname=lastname,email=email,password=password,number=number)
                db.session.add(new_user)
                db.session.commit()
                return jsonify(status=200, message="Se ha registrado al Usuario con éxito"), 200
            return jsonify(status=400, message="Ya existe un usuario con ese correo"), 400
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')

@app.route('/index',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.get_json().get('email')
        password = request.get_json().get('password')
        
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['name']=user.name
            session['email']=user.email
            session['password']=user.password
            return jsonify(status=200, message="acceso correcto"), 200
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)

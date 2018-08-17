from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security,SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost/sample'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'
app.debug=True
#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(80))
#    email = db.Column(db.String(100), unique = True)

#    def __init__(self, username, email):
#        self.username = username
#        self.email = email

#    def __repr__(self):
#        return '<User %r>' %self.username

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
#@app.before_first_request
#def create_user():
#    db.create_all()
#    user_datastore.create_user(email='abc@xyz.com', password='test123')
#    db.session.commit()


@app.route('/')
#def index():
#    users = {'name':'mak','username':'hus'}
#    return render_template('index.html', users=users)

def index():
    return render_template('add_user.html')

@app.route('/post_user', methods=['POST'])
def post_user():
    user = User(request.form['username'], request.form['email'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/users')
def get_users():
    users = User.query.all()
    return render_template('get_user.html', users = users)

@app.route('/homepage')
def display_homepage():
    return 'Display homepage'

@app.route('/profile_page/<username>')
def get_profile(username):
    singleUser=User.query.filter_by(username=username).first()
    return render_template('profile_page.html', singleUser = singleUser)

if __name__ =='__main__':
    app.run()

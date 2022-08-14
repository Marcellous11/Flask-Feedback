from flask import Flask 
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask , request, render_template, redirect,flash ,session
from forms import NewUserForm, LoginUser
from models import User, connect_db, db
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///myTwitter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "secret"
app.config['DEBIG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
connect_db(app)


@app.route('/')
def to_main():  
    return redirect('/register')    

@app.route('/register',methods=['GET','POST'])
def register():
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username=username,password= password,first_name=first_name,last_name=last_name)
        
        db.session.add(new_user)
        try:
            db.session.commit()
        except :
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('index.html', form=form)

        else:
            session['user_id'] = new_user.id
            flash('Welcome! Successfully Created Your Account!', "success")
            return render_template('secret.html')

    
    return render_template('index.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.authenticate(username=username,password=password)
        if new_user:
            session["user_id"] = new_user.id
        else:
            form.username.errors = ['Invalid username/password.']
        # try:
        db.session.commit()
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    session.pop("user_id")
    return redirect('/login')
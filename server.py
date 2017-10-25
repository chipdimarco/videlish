from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import label
from database import db_session, init_db
from models import Base, Recipe, RecipeLike, Account, User, Role
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required,  SQLAlchemySessionUserDatastore, utils

from flask import Flask, render_template_string
from flask_security import Security, current_user, login_required, \
     SQLAlchemySessionUserDatastore
from database import db_session, init_db
from models import User, Role



# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret-random-salt'

    
    
# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    init_db()


 
@app.route("/")
def hello():
   #recipes = session.query(Recipe)
   recipes = db_session.query(label('likeCount', func.count(Recipe.id)),Recipe.name,Recipe.id,Recipe.credit, Recipe.photo,label('user_name', Account.name)).outerjoin(RecipeLike).outerjoin(Account).group_by(Recipe.id).order_by(RecipeLike.create_date).all()

   return render_template('feedGeneric.html', recipes=recipes)
   
@app.route("/mimic-logged-in")
@login_required
def logged_in():
   #recipes = session.query(Recipe)
   recipes = db_session.query(label('likeCount', func.count(Recipe.id)),Recipe.name,Recipe.id,Recipe.credit, Recipe.photo,label('user_name', Account.name)).outerjoin(RecipeLike).outerjoin(Account).group_by(Recipe.id).order_by(RecipeLike.create_date).all()

   return render_template('feed.html', recipes=recipes, username='Emma')
   
@app.route("/getVideo/<int:recipe_id>")
def getVideo(recipe_id):
    recipe = db.session.query(Recipe).filter_by(id=recipe_id).one()
    return render_template('youtubeVideo.html',recipe = recipe)
    
@app.route("/add_video", methods=['GET','POST'])
def addVideo():
    if request.method == 'POST':
        if request.form['youtube_id'] and request.form['video_name']:
            newRecipe = Recipe(hostId = request.form['youtube_id'], name=request.form['video_name'], host='YouTube', credit=request.form['channel'], photo='https://img.youtube.com/vi/' + request.form['youtube_id'] + '/mqdefault.jpg')
            session.add(newRecipe)
            session.commit()
            flash( newRecipe.name + " edited!")
    return redirect(url_for('logged_in'))

    
@app.route("/yourpage")
@login_required
def yourpage():
    return render_template_string('Hello World!')
    
    

 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
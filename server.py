from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import label
from database_setup import Base, Recipe, RecipeLike, Account, User
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required


app = Flask(__name__)

engine = create_engine('sqlite:///videlish.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


 
@app.route("/")
def hello():
   #recipes = session.query(Recipe)
   recipes = session.query(label('likeCount', func.count(Recipe.id)),Recipe.name,Recipe.id,Recipe.credit, Recipe.photo,label('user_name', Account.name)).outerjoin(RecipeLike).outerjoin(Account).group_by(Recipe.id).order_by(RecipeLike.create_date).all()

   return render_template('feedGeneric.html', recipes=recipes)
   
@app.route("/getVideo/<int:recipe_id>")
def getVideo(recipe_id):
    recipe = session.query(Recipe).filter_by(id=recipe_id).one()
    return render_template('youtubeVideo.html',recipe = recipe)
    
@app.route("/yourpage")
@login_required
def yourpage():
    return render_template('helloWorld.html')
 
if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
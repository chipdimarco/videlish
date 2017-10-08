from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Recipe, User, Account, RecipeLike, Role


engine = create_engine('sqlite:///videlish.db')
app = Flask(__name__)
# Create database connection object
db = SQLAlchemy(app)
app.secret_key = 'super_secret_key'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videlish.db'

    
    
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

newRecipe1 = Recipe(name = 'Spanish Omlet', host = 'YouTube', credit = 'Tasty', hostId = 'ah4YoiIbRpc', photo = "https://img.youtube.com/vi/ah4YoiIbRpc/mqdefault.jpg"
)
newRecipe2 = Recipe(name = 'Almond Butter Oatmeal Muffins', host = 'YouTube', credit = 'Quaker', hostId = 'OqfNwI0Qxww', photo = "https://img.youtube.com/vi/OqfNwI0Qxww/mqdefault.jpg" )

user1 = Account(name = 'Emma Green', username = 'emma.green.software@gmail.com')
user_datastore.create_user(email='emmalynng@sbcglobal.net', password='password')

recipeLike1 = RecipeLike(account = user1, recipe=newRecipe1)

session.add(newRecipe1)
session.add(newRecipe2)
session.add(user1)
session.commit()
session.add(recipeLike1)


session.commit()
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from flask.ext.security import UserMixin, RoleMixin


Base = declarative_base()


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    host = Column(String(100), nullable=False)
    credit = Column(String(250), nullable=False)
    hostId = Column(String(100), nullable=False)
    photo = Column(String, nullable=False)

class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    photo = Column(String, nullable=True)
 

roles_users = Table('roles_users',Base.metadata, Column('user_id', Integer(), ForeignKey('user.id')), Column('role_id', Integer(), ForeignKey('role.id')))
        
class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))



    
class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'))
    account = relationship(Account)
    password = Column(String(255))
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary=roles_users,
                            backref=backref('users', lazy='dynamic'))

class RecipeLike(Base):
    __tablename__ = 'recipeLike'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    account = relationship(Account)      
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship(Recipe)
     # define 'create_date' to default to now()
    create_date = Column(DateTime)

engine = create_engine('sqlite:///videlish.db')

Base.metadata.create_all(engine)


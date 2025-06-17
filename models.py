from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now()) 
    
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    nickname = Column(String(50), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())  
    password = Column(String(100), nullable=False)
    role = relationship("Role", back_populates="users")
    ads = relationship("Ad", back_populates="author")
    responses = relationship("Response", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())  
    
    ads = relationship("Ad", back_populates="category")

class Ad(Base):
    __tablename__ = 'ads'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float)
    created_at = Column(DateTime, server_default=func.now()) 
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
    author = relationship("User", back_populates="ads")
    category = relationship("Category", back_populates="ads")
    responses = relationship("Response", back_populates="ad")
    favorites = relationship("Favorite", back_populates="ad")

class Response(Base):
    __tablename__ = 'responses'
    
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())  
    ad_id = Column(Integer, ForeignKey('ads.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    ad = relationship("Ad", back_populates="responses")
    user = relationship("User", back_populates="responses")

class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())  
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ad_id = Column(Integer, ForeignKey('ads.id'), nullable=False)
    
    user = relationship("User", back_populates="favorites")
    ad = relationship("Ad", back_populates="favorites")
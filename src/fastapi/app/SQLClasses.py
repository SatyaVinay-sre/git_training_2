from sqlalchemy.types import *
from sqlalchemy.sql import func

from sqlalchemy import Column, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Many-to-Many bridge table for User and Role
Users_Roles_Bridge = Table(
    "UserRoles",
    Base.metadata,
    Column("roleid", ForeignKey("Role.roleid", name="fk_roleid_userRoleBridge"), primary_key=True),
    Column("userid", ForeignKey("User.userid", name="fk_userid_userRoleBridge"), primary_key=True)
)

# User Model
class User(Base):
    __tablename__ = 'User'

    userid = Column(Integer, primary_key=True)
    uname = Column(String(45), unique=True)
    password = Column(String(45))
    role = relationship('Role', secondary=Users_Roles_Bridge, back_populates='user')
    # Renamed relationship to 'orders' for clarity
    orders = relationship('Order', back_populates='user')
    dateJoined = Column(DateTime, server_default=func.now())

# Role Model
class Role(Base):
    __tablename__ = 'Role'
    
    roleid = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True)
    user = relationship('User', secondary=Users_Roles_Bridge, back_populates="role")

# Product Model (No back_populates on order)
class Product(Base):
    __tablename__ = "Product"

    symbol = Column(String(16), primary_key=True)
    price = Column(DECIMAL(15, 2))
    productType = Column(String(12))
    name = Column(String(128))
    lastUpdate = Column(DateTime)

# Order Model
class Order(Base):
    __tablename__ = 'Order'

    orderid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('User.userid'))
    symbol = Column(String(16), ForeignKey('Product.symbol'))
    side = Column(Integer)
    orderTime = Column(DateTime, server_default=func.now())
    shares = Column(Integer)
    price = Column(DECIMAL(15, 2))
    status = Column(String(24), server_default="pending")  # filled, partial_fill, or canceled
    # Fix back_populates to refer to 'orders' in User model
    user = relationship("User", back_populates="orders")
    # Relationship with Product, no need for back_populates
    product = relationship("Product")
    fill = relationship("Fill", foreign_keys="[Fill.orderid]", back_populates="order")
    # Add 'fills_as_matched' relationship for matched orders
    fills_as_matched = relationship("Fill", foreign_keys="[Fill.matchedorderid]", back_populates="matched_order")

# Fill Model
class Fill(Base):
    __tablename__ = "Fill"
    
    fillid = Column(Integer, primary_key=True)
    orderid = Column(Integer, ForeignKey('Order.orderid'))
    userid = Column(Integer, ForeignKey('User.userid'))
    matchedorderid = Column(Integer, ForeignKey('Order.orderid'))
    share = Column(Integer)
    # Relationship to the 'Order' that owns the fill
    order = relationship("Order", foreign_keys=[orderid], back_populates="fill")
    # Relationship to the matched 'Order'
    matched_order = relationship("Order", foreign_keys=[matchedorderid], back_populates="fills_as_matched")
    price = Column(DECIMAL(15, 2))
    symbol = Column(String(16), ForeignKey('Product.symbol'))

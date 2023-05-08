from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint)
from sqlalchemy.sql import func
from .database import Base


class Customer(Base):
    """
    Таблица с информацией о покупателях
    """
    __tablename__ = 'Customer'
    customer_id = Column(
        Integer, 
        primary_key=True)
    name = Column(
        String(200),
        comment="ФИО покупателя")
    email = Column(
        String(200),
        comment="email покупателя")
    phone_number = Column(
        String(50),
        comment="Номер телефона покупателя в формате +70001234567")

class Purchase(Base):
    """
    Таблица с информацией обо всех покупках по акции
    """
    __tablename__ = 'Purchase'
    purchase_id = Column(
        Integer, 
        primary_key=True)
    customer_id = Column('customer_id', Integer, ForeignKey(
        "Customer.customer_id", ondelete="cascade"))
    purchase_date = Column(
        DateTime,
        server_default=func.now(),
        comment="Время покупки")


class Item(Base):
    """
    Таблица с информацией о товарах партнера
    """
    __tablename__ = 'Item'
    item_id = Column(Integer, primary_key=True)
    name = Column(
        String(200),
        comment="Название товара")


class PurchaseToItem(Base):
    """
    Таблица связей покупка-товар
    """
    __tablename__ = 'PurchaseToItem'
    __table_args__ = (PrimaryKeyConstraint('purchase_id', 'item_id'),)

    purchase_id = Column('purchase_id', ForeignKey(
        'Purchase.purchase_id', ondelete="cascade"), primary_key=True)
    item_id = Column('item_id', ForeignKey(
        'Item.item_id', ondelete="cascade"), primary_key=True)
    price = Column(
        Integer,
        comment="Цена товара в чеке")
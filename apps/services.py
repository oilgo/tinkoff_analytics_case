import re
from string import punctuation
from core import SessionLocal
from typing import Dict
from .schemas import PurcaseRequest
from sqlalchemy import (
    select, 
    update
)
from core import (
    Customer,
    Item,
    Purchase,
    PurchaseToItem
)


async def _purchase_info(request: PurcaseRequest):
    """ Метод для получения и записи в БД информации о покупках по партнерской акции
    """
    customer_id = await _add_user(name=request.customer_name,
                                  email=request.email,
                                  phone_number=request.phone_number)
    purchase_id = await _add_purchase(customer_id=customer_id)
    await _add_items(receipt=request.receipt, purchase_id=purchase_id)


def _clean_phone(phone_number: str) -> str:
    """ Метод для 'очищения' номера телефона
        input params: phone - полученный номер телефона
        output params: очищенный номер телефона
    """
    # Удаляем пунктуацию
    clean_phone = re.sub(f'[{punctuation}]', '', phone_number)
    # Если длина номера не равна 11 -> нет кода страны -> добавляем его
    if len(clean_phone) != 11:
        clean_phone = '+7' + clean_phone
    # Если код страны - 8, меняем его на +7
    elif clean_phone.startswith('8'):
        clean_phone = '+7' + clean_phone[1:]
    # Если код страны - 7, добавляем плюс
    else:
        clean_phone = '+' + clean_phone
    return clean_phone


async def _add_user(name: str, email: str, phone_number: str) -> int:
    """ Метод, который проверяет, есть ли покупатель в БД, 
        и при необходимости добавляет или изменяет информацию о нем
        input_params: name - ФИО покупателя, email - почта покупателя, phone_number - номер телефона покупателя
        output_params: id пользователя в БД
    """
    # 'Очищаем' номер телефона
    phone_number = _clean_phone(phone_number)

    # Смотрим, есть ли уже покупатель в базе (есть ли запись с таким именем и email или именем и телефоном)
    query = select(Customer.customer_id, Customer.name, Customer.email, Customer.phone_number).where(
        Customer.name == name and (
            Customer.phone_number == phone_number or Customer.email == email))
    with SessionLocal() as session:
        new_customer = session.execute(query).fetchone()

    # Если покупателя в базе нет, добавляем
    if new_customer is None:
        new_customer = Customer(
            name=name, email=email, phone_number=phone_number)
        with SessionLocal.begin() as session:
            session.add(new_customer)

    # Если покупатель есть
    else:
        # Преобразуем спрева в словарь, потом в класс
        new_customer = new_customer._mapping
        new_customer = Customer(customer_id=new_customer['customer_id'],
                                name=new_customer['name'],
                                email=new_customer['email'],
                                phone_number=new_customer['phone_number'])

        # Если email или телефон не совпадает, меняем информацию в БД
        if new_customer.email != email or new_customer.phone_number != phone_number:
            with SessionLocal.begin() as session:
                session.execute(update(Customer).values(
                    email=email,
                    phone_number=phone_number).where(Customer.customer_id == new_customer.customer_id))

    return new_customer.customer_id


async def _add_purchase(customer_id: int) -> int:
    """ Метод, который добавляет информацию о покупке в БД
        input_params: customer_id - id покупателя в БД
        output_params: id покупки в БД
    """
    new_purchase = Purchase(customer_id=customer_id)
    with SessionLocal.begin() as session:
        session.add(new_purchase)
    return new_purchase.purchase_id


async def _add_items(receipt: Dict[str, int], purchase_id: int) -> None:
    """ Метод, который проверяет, есть ли информация о товарах в БД, 
        и при необходимости добавляет информацию о них и о связях товар-покупка
        input_params: receipt - чек покупки в формате словаря {название товара: цена}, purchase_id - id покупки в БД
    """
    # Ищем все существующие товары в БД
    with SessionLocal() as session:
        existing_items = session.execute(select(Item.item_id, Item.name)).all()

    # Заводим словарь {название товара: id в БД} и заполняем его
    item_to_id: Dict[str, int] = {}
    for item in existing_items:
        item = item._mapping
        item_to_id[item['name']] = item['item_id']

    # Проходимся по чеку
    for item, price in receipt.items():

        # Если товара нет в БД, добавляем
        if item not in item_to_id:
            new_item = Item(name=item)
            with SessionLocal.begin() as session:
                session.add(new_item)

        # Если есть, преобразуем информацию в класс
        else:
            new_item = Item(name=item, item_id=item_to_id[item])

        # Добавляем связь с инф-ей о цене в БД
        purchase_to_item = PurchaseToItem(purchase_id=purchase_id,
                                          item_id=new_item.item_id,
                                          price=price)
        with SessionLocal.begin() as session:
            session.add(purchase_to_item)

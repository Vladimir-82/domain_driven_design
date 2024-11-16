"""Тестирование взаимодействия с БД."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.models import Product
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository


@pytest.fixture
def create_products():
    """Создание продуктов."""
    product1 = Product(id=1, name='my_product1', quantity=2, price=999)
    product2 = Product(id=2, name='my_product2', quantity=3, price=9)
    product3 = Product(id=3, name='my_product3', quantity=4, price=45)
    product4 = Product(id=4, name='my_product4', quantity=44, price=7)
    return product1, product2, product3, product4


@pytest.fixture(scope='session', autouse=True)
def create_db():
    """Создание БД."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


@pytest.fixture
def session(create_db):
    """Создание сессии БД."""
    return create_db()


class TestInfrastructure:
    """Тестирование взаимодействия с БД."""

    def test_order(self, session, create_products):
        """Проверка количества продуктов в заказе."""
        products = SqlAlchemyProductRepository(session)

        for product in create_products:
            products.add(product)
        session.commit()

        products_list = products.list()
        assert len(products_list) == len(create_products)

    @pytest.mark.parametrize('products_list', [1, 2, 3, 4])
    def test_products(self, session, create_products, products_list):
        """Проверка добавления продуктов в заказ."""
        products = SqlAlchemyProductRepository(session)
        for product in create_products:
            products.add(product)
        session.commit()

        product = products.get(products_list)
        assert product.name == create_products[products_list - 1].name
        assert product.quantity == create_products[products_list - 1].quantity
        assert product.price == create_products[products_list - 1].price

"""Основной модуль."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.services import WarehouseService
from infrastructure.database import DATABASE_URL
from infrastructure.orm import Base
from infrastructure.repositories import (
    SqlAlchemyOrderRepository,
    SqlAlchemyProductRepository,
)
from infrastructure.unit_of_work import AlchemyClassOfWork


engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def main():
    """Основная функция.

    Создание продуктов.
    Получение списка продуктов.
    Создание заказа.
    Получение списка заказов.
    """
    session = SessionFactory()
    product_repo = SqlAlchemyProductRepository(session)
    order_repo = SqlAlchemyOrderRepository(session)

    uow = AlchemyClassOfWork(session)

    warehouse_service = WarehouseService(product_repo, order_repo)
    with uow:
        warehouse_service.create_product(name='product', quantity=2, price=40)
        uow.commit()
        new_product = warehouse_service.product_repo.list().pop()
        print(f'create product: {new_product}')

        warehouse_service.create_product(name='another_product', quantity=3, price=7)
        uow.commit()
        another_product = warehouse_service.product_repo.list().pop()
        print(f'create product: {another_product}')

        get_products_list(product_repo)

        order = warehouse_service.create_order(products=[new_product, another_product])
        uow.commit()
        print(f'Order created: {order}')

        get_orders_list(order_repo)


def get_products_list(product_repo):
    """Получение списка продуктов."""
    products = product_repo.list()
    print('Product list:')
    for product in products:
        print(product)


def get_orders_list(order_repo):
    """Получение списка заказов."""
    orders = order_repo.list()
    print('Order list:')
    for order in orders:
        print(order)


if __name__ == "__main__":
    main()

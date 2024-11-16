"""Тестирование создания продуктов и заказа."""

import pytest
from unittest.mock import MagicMock
from domain.models import Product
from domain.services import WarehouseService


@pytest.fixture
def create_products():
    """Создание продуктов."""
    product1 = Product(id=1, name='my_product1', quantity=2, price=999)
    product2 = Product(id=2, name='my_product2', quantity=3, price=9)
    product3 = Product(id=3, name='my_product3', quantity=4, price=45)
    return product1, product2, product3


@pytest.fixture
def store_service():
    """Сервис WarehouseService."""
    product_repo = MagicMock()
    order_repo = MagicMock()
    return WarehouseService(product_repo, order_repo)


class TestServices:
    """Тестирование создания продуктов и заказа."""

    @pytest.mark.parametrize(
        'products', [
            ({'name': 'my_product', 'quantity': 2, 'price': 99}),
            ({'name': 'another_product', 'quantity': 23, 'price': 1}),
            ({'name': 'another_product_2', 'quantity': 1000, 'price': 1}),
        ]
    )
    def test_create_product_ok(self, store_service, products):
        """Создание продукта. Валидное создание."""

        product = store_service.create_product(products.get('name'), products.get('quantity'), products.get('price'))

        assert isinstance(product, Product)
        assert product.name == products.get('name')
        assert product.quantity == products.get('quantity')
        assert product.price == products.get('price')

    @pytest.mark.parametrize(
        'products', [
            ({'name': 12345, 'quantity': 2, 'price': 99}),
            ({'name': 'another_product', 'quantity': [], 'price': 1}),
            ({'name': 'another_product_2', 'quantity': 1000, 'price': 'price'}),
        ]
    )
    def test_create_product_error(self, store_service, products):
        """Создание продукта. Невалидное создание."""
        with pytest.raises(ValueError):
            store_service.create_product(products.get('name'), products.get('quantity'), products.get('price'))

    def test_create_order(self, store_service, create_products):
        """Создание заказа."""
        product1, product2, product3 = create_products
        order = store_service.create_order(products=[product1, product2, product3])

        assert len(order.products) == len(create_products)
        assert product1 in order.products
        assert product2 in order.products
        assert product3 in order.products

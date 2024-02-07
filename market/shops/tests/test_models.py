from django.test import TestCase
from shops.models import Shop, Offer
from products.models import Product, Detail


class ShopFixturesTest(TestCase):
    """Класс тестов фикстур модели Магазин"""

    fixtures = ["fixtures/04-shops.json"]

    def test_fixtures_len(self):
        self.assertEqual(Shop.objects.count(), 10)


class ShopModelTest(TestCase):
    """Класс тестов модели Магазин"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.detail = Detail.objects.create(name="тестовая характеристика")
        cls.product = Product.objects.create(
            name="тестовый продукт",
        )
        cls.product.details.set([cls.detail])
        cls.shop = Shop.objects.create(name="тестовый магазин")
        cls.offer = Offer.objects.create(shop=cls.shop, product=cls.product, price=25)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        ShopModelTest.detail.delete()
        ShopModelTest.product.delete()
        ShopModelTest.shop.delete()
        ShopModelTest.offer.delete()

    def test_verbose_name(self):
        shop = ShopModelTest.shop
        field_verboses = {
            "name": "название",
            "products": "товары в магазине",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(shop._meta.get_field(field).verbose_name, expected_value)

    def test_name_max_length(self):
        shop = ShopModelTest.shop
        max_length = shop._meta.get_field("name").max_length
        self.assertEqual(max_length, 512)


class OfferModelTest(TestCase):
    """Класс тестов модели Предложение магазина"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = Product.objects.create(
            name="тестовый продукт",
        )
        cls.shop = Shop.objects.create(name="тестовый магазин")
        cls.offer = Offer.objects.create(shop=cls.shop, product=cls.product, price=35)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        OfferModelTest.product.delete()
        OfferModelTest.shop.delete()
        OfferModelTest.offer.delete()

    def test_verbose_name(self):
        offer = OfferModelTest.offer
        field_verboses = {
            "price": "цена",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(offer._meta.get_field(field).verbose_name, expected_value)

    def test_price_max_digits(self):
        offer = OfferModelTest.offer
        max_digits = offer._meta.get_field("price").max_digits
        self.assertEqual(max_digits, 10)

    def test_price_decimal_places(self):
        offer = OfferModelTest.offer
        decimal_places = offer._meta.get_field("price").decimal_places
        self.assertEqual(decimal_places, 2)

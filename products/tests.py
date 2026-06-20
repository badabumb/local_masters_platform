from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from hypothesis import given, settings as hyp_settings, strategies as st
from hypothesis.extra.django import TestCase as HypothesisTestCase

from orders.models import CartItem
from profiles.models import Profile
from .forms import ProductForm
from .models import Product

User = get_user_model()


def make_user(username, is_master=False):
    user = User.objects.create_user(username=username, password='pass12345')
    Profile.objects.create(user=user, is_master=is_master)
    return user


def base_data(price='100.00'):
    return {
        'title': 'Чашка',
        'description': 'Описание товара',
        'price': price,
        'category': 'ceramics',
    }


class ProductFormFuzzTests(HypothesisTestCase):
    """Property-based (fuzz) тесты формы товара."""

    @hyp_settings(max_examples=50, deadline=None)
    @given(
        title=st.text(max_size=200),
        description=st.text(max_size=2000),
        category=st.text(max_size=30),
    )
    def test_form_does_not_crash_on_random_text(self, title, description, category):
        # ProductForm не должен падать на случайных строках —
        # допустимо быть невалидной, но не должно быть исключений.
        data = {'title': title, 'description': description, 'price': '10.00', 'category': category}
        form = ProductForm(data=data)
        form.is_valid()  # не должно бросать исключение

    @hyp_settings(max_examples=50, deadline=None)
    @given(price=st.decimals(min_value=0, max_value=Decimal('99999999.99'), places=2))
    def test_positive_price_is_accepted(self, price):
        form = ProductForm(data=base_data(price=str(price)))
        self.assertTrue(form.is_valid(), form.errors)

    @hyp_settings(max_examples=50, deadline=None)
    @given(price=st.decimals(min_value=Decimal('-99999999.99'), max_value=Decimal('-0.01'), places=2))
    def test_negative_price_is_rejected(self, price):
        form = ProductForm(data=base_data(price=str(price)))
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)


class ProductRoleTests(TestCase):
    """RBAC: только мастер может создавать товары."""

    def test_non_master_cannot_create_product(self):
        make_user('user1', is_master=False)
        self.client.login(username='user1', password='pass12345')
        response = self.client.post(reverse('product_create'), data=base_data())
        self.assertEqual(Product.objects.count(), 0)
        self.assertRedirects(response, reverse('profile_detail'))

    def test_master_can_create_product(self):
        make_user('master1', is_master=True)
        self.client.login(username='master1', password='pass12345')
        response = self.client.post(reverse('product_create'), data=base_data())
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.get()
        self.assertRedirects(response, reverse('product_detail', args=[product.pk]))

    def test_user_without_profile_cannot_create_product(self):
        # Profile отсутствует — код не должен падать.
        User.objects.create_user(username='noprofile', password='pass12345')
        self.client.login(username='noprofile', password='pass12345')
        response = self.client.post(reverse('product_create'), data=base_data())
        self.assertEqual(Product.objects.count(), 0)
        self.assertRedirects(response, reverse('profile_detail'))


class ProductOwnershipTests(TestCase):
    """Редактировать/удалять товар может только владелец или staff."""

    def setUp(self):
        self.owner = make_user('owner', is_master=True)
        self.other = make_user('other', is_master=True)
        self.product = Product.objects.create(
            title='Чашка', description='Опис', price=Decimal('100.00'),
            category='ceramics', author=self.owner,
        )

    def test_other_user_cannot_update_product(self):
        self.client.login(username='other', password='pass12345')
        response = self.client.post(
            reverse('product_update', args=[self.product.pk]),
            data=base_data(price='999.00'),
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal('100.00'))
        self.assertRedirects(response, reverse('product_detail', args=[self.product.pk]))

    def test_other_user_cannot_delete_product(self):
        self.client.login(username='other', password='pass12345')
        response = self.client.post(reverse('product_delete', args=[self.product.pk]))
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        self.assertRedirects(response, reverse('product_detail', args=[self.product.pk]))

    def test_owner_can_update_product(self):
        self.client.login(username='owner', password='pass12345')
        self.client.post(
            reverse('product_update', args=[self.product.pk]),
            data=base_data(price='250.00'),
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal('250.00'))

    def test_owner_can_delete_product(self):
        self.client.login(username='owner', password='pass12345')
        self.client.post(reverse('product_delete', args=[self.product.pk]))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())


class CartOwnProductTests(TestCase):
    """Пользователь не может добавить свой товар в корзину."""

    def test_user_cannot_add_own_product_to_cart(self):
        owner = make_user('owner', is_master=True)
        product = Product.objects.create(
            title='Чашка', description='Опис', price=Decimal('100.00'),
            category='ceramics', author=owner,
        )
        self.client.login(username='owner', password='pass12345')
        self.client.post(reverse('add_to_cart', args=[product.pk]))
        self.assertEqual(CartItem.objects.filter(user=owner, product=product).count(), 0)

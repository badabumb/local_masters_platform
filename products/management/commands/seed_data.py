from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from products.models import Product
from profiles.models import Profile


class Command(BaseCommand):
    help = 'Creates demo masters and handmade products for the catalog.'

    def handle(self, *args, **options):
        products = [
            {
                'username': 'anna_ceramics',
                'master': 'Анна Кузнецова',
                'city': 'Москва',
                'title': 'Керамическая ваза ручной работы',
                'description': 'Матовая керамическая ваза спокойной формы для сухоцветов и небольших букетов.',
                'price': Decimal('3200.00'),
                'category': 'ceramics',
            },
            {
                'username': 'vera_wax',
                'master': 'Вера Соколова',
                'city': 'Тула',
                'title': 'Свеча из натурального воска',
                'description': 'Свеча из пчелиного воска с мягким медовым ароматом и хлопковым фитилем.',
                'price': Decimal('850.00'),
                'category': 'candles',
            },
            {
                'username': 'olga_knit',
                'master': 'Ольга Миронова',
                'city': 'Казань',
                'title': 'Вязаный шарф',
                'description': 'Теплый шарф крупной вязки из мягкой полушерстяной пряжи для прохладной погоды.',
                'price': Decimal('2400.00'),
                'category': 'textile',
            },
            {
                'username': 'maria_beads',
                'master': 'Мария Орлова',
                'city': 'Санкт-Петербург',
                'title': 'Серьги из бисера',
                'description': 'Легкие серьги из японского бисера в пудрово-малиновой гамме.',
                'price': Decimal('1300.00'),
                'category': 'jewelry',
            },
            {
                'username': 'ivan_wood',
                'master': 'Иван Беляев',
                'city': 'Ярославль',
                'title': 'Деревянная шкатулка',
                'description': 'Небольшая шкатулка из массива дерева с аккуратной ручной шлифовкой.',
                'price': Decimal('2800.00'),
                'category': 'wood',
            },
            {
                'username': 'nina_soap',
                'master': 'Нина Волкова',
                'city': 'Нижний Новгород',
                'title': 'Мыло ручной работы',
                'description': 'Натуральное мыло с маслами ши и миндаля, подходит для ежедневного ухода.',
                'price': Decimal('520.00'),
                'category': 'cosmetics',
            },
        ]

        created_count = 0

        for item in products:
            user, _ = User.objects.get_or_create(
                username=item['username'],
                defaults={
                    'first_name': item['master'],
                    'email': f"{item['username']}@example.com",
                },
            )
            if not user.first_name:
                user.first_name = item['master']
                user.save(update_fields=['first_name'])

            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'name': item['master'],
                    'city': item['city'],
                    'about': f"Локальный мастер. Создает изделия в категории «{dict(Product.CATEGORY_CHOICES)[item['category']]}».",
                    'is_master': True,
                },
            )

            _, created = Product.objects.update_or_create(
                title=item['title'],
                defaults={
                    'description': item['description'],
                    'price': item['price'],
                    'category': item['category'],
                    'author': user,
                },
            )
            created_count += int(created)

        self.stdout.write(self.style.SUCCESS(f'Готово: демо-товары созданы или обновлены. Новых товаров: {created_count}.'))

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Create moderator group with permissions'

    def handle(self, *args, **options):
        # Создаём или получаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем контент-тип модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем кастомное право can_unpublish_product
        can_unpublish = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type,
        )

        # Получаем право на удаление продукта
        can_delete = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        # Добавляем права группе
        moderator_group.permissions.add(can_unpublish, can_delete)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана и права назначены'))
        else:
            self.stdout.write(self.style.SUCCESS('Права для группы "Модератор продуктов" обновлены'))

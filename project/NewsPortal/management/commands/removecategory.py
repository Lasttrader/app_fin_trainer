from django.core.management.base import BaseCommand, CommandError
from NewsPortal.models import Category, Post, Author
 
 
class Command(BaseCommand):
    help = 'Эта команда удаляетвсе новости из какой-либо категории, но только при подтверждении действия в консоли при выполнении команды '
 
    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
 
    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        try:
            category = Category.objects.get(name=options['category'])

            Post.objects.filter(postCategory=category).delete()

            self.stdout.write(self.style.SUCCESS(f'Все новости в категории {category.name} успешно удалены')) # в случае неправильного подтверждения говорим, что в доступе отказано
        
        except category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {category.name}'))
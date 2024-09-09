import json
from upload.models import Category
from django.core.management.base import BaseCommand


categories = []
with open('categories.json', 'r') as f:
    categories = json.loads(f.read())


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in categories:
            category = Category.objects.create(
                title=i['title'], photo=i['image'], url=i['url'])
            for sub in i['sub']:
                sub = Category.objects.create(
                    title=sub['title'], photo=sub['image'], url=sub['url'], parent=category)
                for sub2 in sub['sub']:
                    Category.objects.create(
                        title=sub2['title'], photo=sub2['image'], url=sub2['url'], parent=sub)

        print('Categories created successfully')

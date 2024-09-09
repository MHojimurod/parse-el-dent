from upload.models import Category
from dump.utils import parse_products_link
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    '''Save the links of the products belonging to each category to the Urls model'''

    def handle(self, *args, **options):
        categories = Category.objects.filter(parent=None)
        for cateogry in categories:
            subs = Category.objects.filter(parent=cateogry)
            for sub in subs:
                if sub.parent:
                    subs2 = Category.objects.filter(parent=sub)
                    for sub2 in subs2:
                        # parse all products links belonging to this sub2
                        parse_products_link(sub2.pk, sub2.url)
                else:
                    # parse all products links belonging to this sub
                    parse_products_link(sub.pk, sub.url)

        print('Successfully parsed product links')

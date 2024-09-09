from upload.models import Urls
from dump.utils import parse_product_detail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    '''Each product detail is parsed and saved to the Product model, this takes more time, because it is send  request each detail page'''

    def handle(self, *args, **options):

        urls = Urls.objects.filter(done=False).order_by('id')
        for url in urls:

            # This function parse product details and save to Product model
            res = parse_product_detail(url.url, url.category.pk)

            if res:
                # To avoid re-parsing
                url.done = True
                url.save()

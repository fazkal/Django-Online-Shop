from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import BaseProvider
from django.utils.text import slugify
from shop.models import ProductCategoryModel


class FashionProvider(BaseProvider):

    fashion_items = ['کیف','کلاه','لباس','کفش',
                     'جوراب','تجهیزات جانبی','لباس زیر','کفش ورزشی'
                     ,'ساعت مچی','عینک آفتابی','شلوار','زیورآلات'
                     ,'کوله پشتی','اکسسوری مو','تاپ','شلوارک']
    
    def fashion_item(self):
        return self.random_element(self.fashion_items)


class Command(BaseCommand):
    help = 'Generate fake categories'
    

    def handle(self, *args, **options):
        fake = Faker(['fa_IR'])
        fake.add_provider(FashionProvider) 

        for _ in range(10):
            title = fake.fashion_item()
            slug = slugify(title,allow_unicode=True)
            ProductCategoryModel.objects.get_or_create(title=title,slug=slug)

        self.stdout.write(self.style.SUCCESS(
            'Successfuly generated 10 fake categories'
        ))

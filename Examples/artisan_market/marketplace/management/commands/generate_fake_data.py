from django.core.management.base import BaseCommand
from marketplace.models import Product
from django.contrib.auth.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake products for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()
        user, _ = User.objects.get_or_create(username='testuser')
        user.set_password('password123')
        user.save()

        # Sample tags to use
        sample_tags = ['handmade', 'vintage', 'art', 'fashion', 'home', 'gift', 'eco-friendly', 'leather', 'wood', 'knit']

        for _ in range(20):
            product = Product.objects.create(
                seller=user,
                title=fake.sentence(nb_words=3),
                description=fake.text(),
                price=round(random.uniform(10.0, 100.0), 2),
                image='product_images/default.jpg'
            )

            # Assign 1 to 3 random tags from the sample list
            chosen_tags = random.sample(sample_tags, k=random.randint(1, 3))
            product.tags.add(*chosen_tags)

        self.stdout.write(self.style.SUCCESS("✅ 20 fake products with tags created."))

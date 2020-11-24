from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from api.models import Profile

class Command(BaseCommand):
    help = "simple command for creation of super user"

    def handle(self, *args, **options):
        user_model = get_user_model()
        asin, created = user_model.objects.get_or_create(
            username="asin", 
        )

        asin.email="w200kr@gmail.com"
        asin.is_staff=True
        asin.is_superuser=True

        asin_profile, created = Profile.objects.get_or_create(
            user=asin
        )
        asin_profile.category='S'
        asin_profile.name='신석은'
        asin_profile.tel='92874497'
        asin_profile.address='서울특별시 동대문구 망우로12길 49-1'
        asin_profile.address_detail='지하 B102호'
        asin_profile.kakao_id='1520435556'

        asin.set_password('hawks2012')

        asin.save()
        asin_profile.save()
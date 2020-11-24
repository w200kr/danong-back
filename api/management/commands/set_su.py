from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from api.models import Profile

class Command(BaseCommand):
    help = "simple command for creation of super user"

    def handle(self, *args, **options):
        user_model = get_user_model()
        asin, created = user_model.objects.get_or_create(
            username="asin", 
            email="w200kr@gmail.com", 
            is_staff=True,
            is_superuser=True,
            # category='Player',
            # student_id='2012920031',
            # tel='01092874497',
            # name='신석은',
        )
        asin_profile, created = Profile.objects.get_or_create(
            user=asin,
            category='S',
            name='신석은',
            tel='92874497',
            address='서울특별시 동대문구 망우로12길 49-1',
            address_detail='지하 B102호',
            kakao_id='1520435556'   
        )

        asin.set_password('hawks2012')
        asin.save()
        asin_profile.save()
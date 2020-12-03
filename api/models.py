from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

from datetime import datetime

"""

유즈케이스

1. 회원가입
    판매자회원
    구매자회원

2. 로그인

3. 소셜 회원가입

4. 소셜 로그인

5. 상품 등록

6. 상품 검색
    지도
    필터
    지도+필터

7. 상품 상세 확인

8. 상품 구매

9. 관심목록 등록

"""



"""
User
    user_id : 이용자 번호, integer, primary key, NOT NULL, 
    category : 유저 종류(판매자, 구매자), varchar(10), NOT NULL,
    email :  이메일, varchar(100), NOT NULL
    password : 비밀번호, varchar(255), NOT NULL
    name : 실명, varchar(20), NULL
    zip : 우편번호, varchar(20) NULL
    address : 주소, varchar(255), NULL
    address_detail : 주소상세, varchar(255), NULL
    phone : 전화번호, varchar(255), NULL
    gender : 성별, varchar(255), NULL
    career: 농사경력, varchar(255), NULL
"""
"""
Wish
    wish_id : 관심목록 번호, integer, primary key, NOT NULL, 
    user_id : 이용자 번호, integer, Foreign key, NOT NULL, 
    product_ id: 상품 번호, integer, Foreign key, NOT NULL, 
"""
def user_directory_path(instance, filename):
    dt = datetime.now()
    dt_string = dt.isoformat().split(".")[0]
    return f'{instance.user.username}/{dt_string}/{filename}'

class Profile(models.Model):
    SELLER = 'S'
    BUYER = 'B'
    CATEGORY_CHOICES = (
        (SELLER, '판매자'),
        (BUYER, '구매자'),
    )

    # JOB_POSITION_CHOICES = (
    # )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES, null=False, blank=False, default='B')
    # image_url = models.CharField(max_length=1024, null=True, blank=True)
    name = models.CharField(max_length=20, null=False, blank=False)

    # zipcode = models.CharField(max_length=10, null=True, blank=True, default='')
    address = models.CharField(max_length=100, null=True, blank=True, default='')
    address_detail = models.CharField(max_length=100, null=True, blank=True, default='')

    tel = models.CharField(max_length=20, null=False, blank=False, default='')
    career = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    thumbnail = ProcessedImageField(
        upload_to=user_directory_path,
        processors=[Thumbnail(230, 230)], # 처리할 작업 목룍
        format='JPEG',                    # 최종 저장 포맷
        options={'quality': 70},
        null=True,
        blank=True,
    )
    seller_name = models.CharField(max_length=20, null=True, blank=True)
    job_position = models.CharField(max_length=20, null=True, blank=True)
    main_crops = models.ForeignKey('SmallCategory', on_delete=models.SET_NULL, null=True, blank=True)

    kakao_id = models.CharField(max_length=20, null=True, blank=True, unique=True)

    wishlist = models.ManyToManyField('Product', blank=True)

    @property
    def email(self):
        return self.user.email

    @email.setter
    def email(self, value):
        self.user.email = value

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = '프로필 목록'


class SmallCategory(models.Model):
    CATEGORY_CHOICES = (
        ('garden', '야채류'),
        ('green', '청과류'),
        ('grain', '곡류'),
        ('nuts', '견과류'),
        ('mushrooms', '버섯류'),
        ('etc', '기타/가공품'),
    )

    large_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = '상품 분류'
        verbose_name_plural = '상품 분류 목록'

    def __str__(self):
        return f'[{self.get_large_category_display()}] {self.name}'

    def get_category_depth(self):
        all_categories = SmallCategory.objects.all()
        category_depth = {value:[] for (value, label) in SmallCategory.CATEGORY_CHOICES}

        for category in all_categories:
            category_depth[category.large_category].append(category)

        return category_depth

"""
Product
    product_id : 상품 번호, integer, Primary key, NOT NULL, 
    buyer_id : 판매자 번호, integer, Foreign key, NOT NULL, 
    product_type : 상품 종류', varchar(15), NOT NULL,
    name : 상품 이름, varchar(50), not null
    address : 농작지 주소, varchar(255), not null
    price : 가격, integer, not null
    view_count : 조회수, integer, not null, default=1
    description : 상품설명, text, not null
    image_url : 대표 이미지 url, varchar(500), NOT NULL
    created : 생성시점, DateTime, not null, default=datetime.now
    updated : 갱신시점, DateTime, not null, default=datetime.now
    is_hide : 공개 여부, boolean, not null, default=true

    lat : 위도, varchar(50), not null 
    lng : 경도, varchar(50), not null 
"""
def product_directory_path(instance, filename):
    return f'{instance.seller.username}/{instance.name}_{instance.updated}/{filename}'

class Product(models.Model):
    seller = models.ForeignKey(User, verbose_name='판매자', on_delete=models.CASCADE, null=False, blank=False)
    category = models.ForeignKey('SmallCategory', verbose_name='상품 분류', on_delete=models.SET_NULL, null=True, blank=False)
    # category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=False, blank=False)
    name = models.CharField('상품명', max_length=100, null=False, blank=False)
    address = models.CharField('농지 주소', max_length=200, null=False, blank=False)
    price = models.PositiveIntegerField('가격', null=False, blank=False)
    view_count = models.PositiveSmallIntegerField('조회수', null=False, blank=False, default=0)
    description = models.CharField('상품 설명', max_length=100, null=False, blank=False)
    CS_contact = models.CharField('1대1 상담 url', max_length=500, null=False, blank=False)
    thumbnail = ProcessedImageField(
        verbose_name='대표 섬네일',
        upload_to=product_directory_path,
        processors=[Thumbnail(230, 230)], # 처리할 작업 목룍
        format='JPEG',                    # 최종 저장 포맷
        options={'quality': 70},
        null=True,
        blank=True,
    )
    is_hide = models.BooleanField(null=False, blank=False, default=False)

    free_shipping = models.BooleanField('택배거래', null=False, blank=False, default=False)
    same_day_shipping = models.BooleanField('직거래', null=False, blank=False, default=False)

    natural = models.BooleanField('자연산', null=False, blank=False, default=False)
    low_cabon = models.BooleanField('저탄소', null=False, blank=False, default=False)
    organic = models.BooleanField('유기농', null=False, blank=False, default=False)
    low_pesticide = models.BooleanField('저농약', null=False, blank=False, default=False)
    pesticide_free = models.BooleanField('무농약', null=False, blank=False, default=False)

    lat = models.FloatField(null=False, blank=False)
    lng = models.FloatField(null=False, blank=False)

    aptitude_table = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='생성시간', null=False, blank=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='수정시간', null=False, blank=False)

    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품 목록'

    def __str__(self):
        return f'{self.name}'


def productimage_directory_path(instance, filename):
    return f'{instance.product.seller.username}/{instance.product.name}_{instance.product.updated}/{filename}'

class ProductImage(models.Model):
    IMAGE_TYPE_CHOICE = (
        ('top', '상단 대표 이미지'),
        ('content', '상품 설명 이미지'),
    )

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(verbose_name='순서', null=False, blank=False)
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPE_CHOICE, null=False, blank=False)
    image = models.ImageField(upload_to=productimage_directory_path)

    class Meta:
        verbose_name = '상품 이미지'
        verbose_name_plural = '상품 이미지 목록'
        unique_together = ['product', 'image_type', 'order']

    def __str__(self):
        return f'{self.product.name} 상품 이미지'

"""
ProductOption
    product_option_id = 상품 옵션 번호, integer, Primary key, NOT NULL, 
    product_id : 상품 번호, integer, Foreign key, NOT NULL, 
    order : 옵션 순서, 번호, integer, NOT NULL, default=0
    volumn : 용량, varchar(255), not null
    price : 가격, integer, not null

    unique index - product_id, order
"""
class ProductOption(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(verbose_name='순서', null=False, blank=False)
    volumn = models.CharField(verbose_name='용량', max_length=50, null=False, blank=False)
    price = models.PositiveIntegerField(verbose_name='가격', null=False, blank=False)

    class Meta:
        verbose_name = '상품 옵션'
        verbose_name_plural = '상품 옵션 목록'
        unique_together = ['product', 'order']

    def __str__(self):
        return f'{self.product.name} - {self.volumn}'

class ProductFaq(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(verbose_name='순서', null=False, blank=False)
    question = models.CharField(verbose_name='질문', max_length=100, null=False, blank=False)
    answer = models.CharField(verbose_name='대답', max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = '상품 문답'
        verbose_name_plural = '상품 문답 목록'
        unique_together = ['product', 'order']

    def __str__(self):
        return f'{self.product.name} - {self.question[:10]}'




"""
Purchase
    purchase_id = 구매내역 번호, integer, Primary key, NOT NULL, 
    seller_id = 구매자 번호, integer, Foreign key, NOT NULL, 
    product_option_id = 구매옵션 번호, integer, Foreign key, NOT NULL, 
    qty = 구매수량, integer, NOT NULL, 
    amount = 지불가격, integer, NOT NULL, 
    imp_id = 결제모듈의 해당 구매내역 id, varchar(255), null 
    merchant_uid = 결제번호, varchar(255), null
    type = 결제 수단, varchar(20), not null,
    status = 결제 상태, varchar(30), not null, default='UNPAYMENT'
    created = 결제일시, DateTime, not null, default=datetime.now
"""
class Purchase(models.Model):
    PENDING = 10
    COMPLETE = 20
    PROCEEDING = 30
    DONE = 40
    CANCEL = 50

    STATUS_CHOICE = (
        (PENDING, '결제 대기'),
        (COMPLETE, '결제 완료'),
        (PROCEEDING, '배송 중 '),
        (DONE, '배송 완료 '),
        (CANCEL, '취소'),
    )

    CARD = 'card'
    CASH = 'cash'
    PAYMENT_TYPE_CHOICE = (
        (CARD, '카드 결제'),
        (CASH, '무통장 입금'),
    )

    buyer = models.ForeignKey(User, verbose_name='구매자', on_delete=models.CASCADE, null=False, blank=False)
    product_option = models.ForeignKey('ProductOption', verbose_name='구매 옵션', on_delete=models.CASCADE, null=False, blank=False)
    qty = models.PositiveSmallIntegerField(verbose_name='수량', null=False, blank=False)
    amount = models.PositiveIntegerField(verbose_name='결제 총액', null=False, blank=False)

    payment_type = models.CharField(verbose_name='결제수단', max_length=10, choices=PAYMENT_TYPE_CHOICE, null=False, blank=False)
    status = models.IntegerField(verbose_name='상태',choices=STATUS_CHOICE, null=False, blank=False, default=PENDING)
    imp_id = models.CharField(max_length=120, null=True, blank=True)
    merchant_uid = models.CharField(max_length=120, unique=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name='생성시간', null=False, blank=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='수정시간', null=False, blank=False)

    class Meta:
        verbose_name = '구매내역'
        verbose_name_plural = '구매내역 목록'

    def __str__(self):
        return f'{self.buyer.profile.name} {self.amount}'

"""
Review
    review_id : 리뷰 번호, integer, Primary key, NOT NULL, 
    product_id : 상품 번호, integer, Foreign key, NOT NULL, 
    seller_id : 구매자 번호, integer, Foreign key, NOT NULL, 
    rating : 별점, integer, not null,
    text : 내용, varchar(500), not null
    created : 작성일시, DateTime, not null, default=datetime.now
"""
class Review(models.Model):
    product = models.ForeignKey('Product', verbose_name='상품', on_delete=models.CASCADE, null=False, blank=False)
    buyer = models.ForeignKey(User, verbose_name='구매자', on_delete=models.CASCADE, null=False, blank=False)
    rating = models.FloatField(verbose_name='평가점수')
    text = models.CharField(verbose_name='리뷰 내용', max_length=300, null=False, blank=False)
    created = models.DateTimeField(verbose_name='생성시간', auto_now_add=True, null=False, blank=False)

    class Meta:
        verbose_name = '상품 리뷰'
        verbose_name_plural = '상품 리뷰 목록'

    def __str__(self):
        return f'{self.buyer.profile.name} {self.text}'
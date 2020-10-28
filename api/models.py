from django.db import models

# Create your models here.
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
# class Profile(models.Model):
#     pass


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
# class Product(models.Model):
#     pass


"""
ProductOption
    product_option_id = 상품 옵션 번호, integer, Primary key, NOT NULL, 
    product_id : 상품 번호, integer, Foreign key, NOT NULL, 
    order : 옵션 순서, 번호, integer, NOT NULL, default=0
    volumn : 용량, varchar(255), not null
    price : 가격, integer, not null

    unique index - product_id, order
"""
# class ProductOption(models.Model):
#     pass


"""
Wish
    wish_id : 관심목록 번호, integer, primary key, NOT NULL, 
    user_id : 이용자 번호, integer, Foreign key, NOT NULL, 
    product_ id: 상품 번호, integer, Foreign key, NOT NULL, 
"""
# class Wish(models.Model):
#     pass


"""
Purchase
    purchase_id = 구매내역 번호, integer, Primary key, NOT NULL, 
    seller_id = 구매자 번호, integer, Foreign key, NOT NULL, 
    product_option_id = 구매옵션 번호, integer, Foreign key, NOT NULL, 
    qty = 구매수량, integer, NOT NULL, 
    amount = 지불가격, integer, NOT NULL, 
    imp_id = 결제모듈의 해당 구매내역 id, varchar(255), null 
    merchant_id = 결제번호, varchar(255), null
    type = 결제 수단, varchar(20), not null,
    status = 결제 상태, varchar(30), not null, default='UNPAYMENT'
    created = 결제일시, DateTime, not null, default=datetime.now
"""
# class Purchase(models.Model):
#     pass


"""
Review
    review_id : 리뷰 번호, integer, Primary key, NOT NULL, 
    product_id : 상품 번호, integer, Foreign key, NOT NULL, 
    seller_id : 구매자 번호, integer, Foreign key, NOT NULL, 
    rating : 별점, integer, not null,
    text : 내용, varchar(500), not null
    created : 작성일시, DateTime, not null, default=datetime.now
"""
# class Review(models.Model):
#     pass
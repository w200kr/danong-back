# from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Avg


from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from api.models import SmallCategory, Profile, Product, ProductImage, ProductOption, ProductFaq, Purchase, Review

from IPython import embed

import json
# import datetime, copy

class BaseSerializer(serializers.Serializer):
    def get_request_user(self):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        # if settings.DEBUG and user.is_anonymous:
        #     user = User.objects.get(username='asin')
        return user

class ProfileSerializer(serializers.ModelSerializer, BaseSerializer):
    # user_id = serializers.IntegerField(source='user.id', read_only=True)
    # profile_id = serializers.IntegerField(source='user.profile.id', read_only=True)
    # username = serializers.CharField(source='user.username', read_only=True)
    # password = serializers.CharField(source='user.password', required=False, write_only=True)
    thumbnail = serializers.ImageField(required=False, allow_empty_file=True, use_url=False, write_only=True)
    thumbnail_url = serializers.SerializerMethodField(required=False, read_only=True)
    large_category = serializers.CharField(source='main_crops.large_category', required=False, read_only=True)

    class Meta:
        model = Profile
        exclude = ['user', 'wishlist', 'id']

    def get_thumbnail_url(self, profile):
        try:
            url = self.context['request'].build_absolute_uri(profile.thumbnail.url)
        except Exception as e:
            url = ''
        return url


class SignUpSerializer(serializers.ModelSerializer, BaseSerializer):
    category = serializers.CharField(source='profile.category')
    name = serializers.CharField(source='profile.name')
    tel = serializers.CharField(source='profile.tel')

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create({
            'username': validated_data['username'],
            'email': validated_data['email']
        })
        user_profile = Profile.objects.create(
            user=user,
            category=validated_data.get('profile',{}).get('category', Profile.BUYER),
            name=validated_data.get('profile',{}).get('name', ''),
            tel=validated_data.get('profile',{}).get('tel', ''),
        )

        user.set_password(validated_data['password'])
        user.save()
        user_profile.save()
        return user

class KakaoSignUpSerializer(SignUpSerializer):
    kakao_id = serializers.CharField(source='profile.kakao_id')
    def create(self, validated_data):
        # kakao_id, nickname, tel
        user = super().create({
            'username': 'kakao_'+validated_data.get['kakao_id'],
            'password': User.objects.make_random_password(30),
            'email': validated_data['email'],
            'profile': {
                'category': 'B',
                'name': validated_data.get('nickname', ''),
                'tel': validated_data.get('tel', ''),
            }
        })
        return user

class LoginSerializer(AuthTokenSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    # profile = ProfileSerializer(source='user.proifle', required=False)
    profile_id = serializers.IntegerField(source='user.profile.id', read_only=True)
    category = serializers.CharField(source='user.profile.category', read_only=True)
    name = serializers.CharField(source='user.profile.name', read_only=True)
    # address = serializers.CharField(source='user.profile.address', read_only=True)
    # address_detail = serializers.CharField(source='user.profile.address_detail', read_only=True)
    # tel = serializers.CharField(source='user.profile.tel', read_only=True)
    # career = serializers.CharField(source='user.profile.career', read_only=True)
    # comment = serializers.CharField(source='user.profile.comment', read_only=True)
    # # thumbnail = serializers.CharField(source='user.profile.thumbnail.url', read_only=True)
    # thumbnail_url = serializers.SerializerMethodField()
    # seller_name = serializers.CharField(source='user.profile.seller_name', read_only=True)
    # job_position = serializers.CharField(source='user.profile.job_position', read_only=True)
    # large_category = serializers.CharField(source='user.profile.main_crops.large_category', read_only=True)
    # main_crops = serializers.IntegerField(source='user.profile.main_crops.id', read_only=True)

    # def get_thumbnail_url(self, token):
    #     try:
    #         url = self.context['request'].build_absolute_uri(token['user'].profile.thumbnail.url)
    #     except Exception as e:
    #         url = ''
    #     return url

class KakaoLoginSerializer(LoginSerializer):
    username = None
    password = None
    kakao_id = serializers.CharField(source='user.profile.kakao_id', write_only=True)
    name = serializers.CharField(source='user.profile.name', required=False)
    email = serializers.CharField(source='user.email', required=False)
    # tel = serializers.CharField(source='user.profile.tel', write_only=True)

    def validate(self, attrs):
        profile_obj = attrs.get('user', {}).get('profile', {})
        kakao_id = profile_obj.get('kakao_id', None)
        if not kakao_id:
            msg = _('Must include "kakao_id".')
            raise serializers.ValidationError(msg, code='authorization')

        matched_profile = Profile.objects.filter(kakao_id=kakao_id).first()
        if matched_profile:
            user = matched_profile.user
            attrs['user'] = user
        else:
            name = profile_obj.get('name', '')
            email = profile_obj.get('email', '')
            tel = profile_obj.get('tel', '')

            user = User.objects.create(
                username='kakao_'+kakao_id,
                email=email,
            )
            user_profile = Profile.objects.create(
                user=user,
                category=Profile.BUYER,
                name=name,
                tel=tel,
                kakao_id=kakao_id,
            )

            user.set_password( User.objects.make_random_password(30) )
            user.save()
            user_profile.save()

            attrs['user'] = user

        # attrs['user'] = user
        return attrs


class UserProfileDetailSerializer(serializers.ModelSerializer, BaseSerializer):
    password = serializers.CharField(write_only=True,)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'date_joined']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user

class CategoryListSerializer(serializers.ModelSerializer, BaseSerializer):
    class Meta:
        model = SmallCategory
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer, BaseSerializer):
    image = serializers.ImageField(required=True, use_url=False, write_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = '__all__'

    def get_image_url(self, productimag):
        try:
            url = self.context['request'].build_absolute_uri(productimag.image.url)
        except Exception as e:
            url = ''
        return url

class ProductOptionSerializer(serializers.ModelSerializer, BaseSerializer):
    class Meta:
        model = ProductOption
        fields = '__all__'

class ProductFaqSerializer(serializers.ModelSerializer, BaseSerializer):
    class Meta:
        model = ProductFaq
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer, BaseSerializer):
    buyer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, default=serializers.CurrentUserDefault())
    buyer_name = serializers.CharField(source='buyer.profile.name', read_only=True)
    buyer_thumbnail_url = serializers.SerializerMethodField(read_only=True)
    is_mine = serializers.SerializerMethodField(read_only=True)
    created = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def get_buyer_thumbnail_url(self, review):
        try:
            url = self.context['request'].build_absolute_uri(review.buyer.profile.thumbnail.url)
        except Exception as e:
            print(e)
            url = ''
        return url

    def get_is_mine(self, review):
        user = self.get_request_user()
        if user:
            return user == review.buyer
        else:
            return None
    def get_created(self, review):
        return review.created.strftime('%Y.%m.%d')

class ProductListSerializer(serializers.ModelSerializer, BaseSerializer):
    seller = UserProfileDetailSerializer(default=serializers.CurrentUserDefault())
    images = ProductImageSerializer(source='productimage_set', many=True, required=False)
    options = ProductOptionSerializer(source='productoption_set', many=True, required=False)
    faqs = ProductFaqSerializer(source='productfaq_set', many=True, required=False)

    is_dibbed = serializers.SerializerMethodField()
    rating_avg = serializers.SerializerMethodField()
    review_num = serializers.IntegerField(source='review_set.count', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        obj = {**validated_data, 'seller': self.get_request_user()}  
        product = Product.objects.create(**obj)
        images_data = self.initial_data.getlist('images[]')
        images_rest_data = json.loads( self.initial_data.get('images_rest', '[]') )
        options_data = json.loads( self.initial_data.get('options', '[]') )
        faqs_data = json.loads( self.initial_data.get('faqs', '[]') )
        # 
        for index, image_data in enumerate(images_data):
            ProductImage.objects.create(product=product, image=image_data, order=index, **images_rest_data[index])

        for index, option_data in enumerate(options_data):
            ProductOption.objects.create(product=product, **option_data, order=index)

        for index, faq_data in enumerate(faqs_data):
            ProductFaq.objects.create(product=product, **faq_data, order=index)
        return product

    def get_is_dibbed(self, product):
        user = self.get_request_user()
        if user.is_anonymous:
            return None
        else:
            return user.profile.wishlist.filter(id=product.id).exists()

    def get_rating_avg(self, product):
        rating_avg = product.review_set.all().aggregate(Avg('rating')).get('rating__avg', 0)
        if rating_avg:
            return round(rating_avg, 2)
        return 0

class ProductSearchSerializer(serializers.ModelSerializer, BaseSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SellerProfileSerializer(serializers.ModelSerializer, BaseSerializer):
    tel = serializers.SerializerMethodField(read_only=True)
    career = serializers.CharField(read_only=True)
    comment = serializers.CharField(read_only=True)
    seller_name = serializers.CharField(read_only=True)
    job_position = serializers.CharField(read_only=True)
    main_crops = serializers.CharField(read_only=True)
    # thumbnail_url =
    thumbnail_url = serializers.SerializerMethodField(read_only=True)
    rating_avg = serializers.SerializerMethodField()
    review_num = serializers.SerializerMethodField()
    product_num = serializers.IntegerField(source='user.product_set.count', read_only=True)

    class Meta:
        model = Profile
        exclude = ('wishlist', 'user', 'kakao_id')

    def get_tel(self, profile):
        return f'{profile.tel[:3]}-{profile.tel[3:7]}-{profile.tel[7:11]}'

    def get_thumbnail_url(self, profile):
        try:
            url = self.context['request'].build_absolute_uri(profile.thumbnail.url)
        except Exception as e:
            url = ''
        return url

    def get_rating_avg(self, profile):
        rating_avg = Review.objects.filter(product__seller=profile.user).aggregate(Avg('rating')).get('rating__avg', 0) or 0
        if rating_avg:
            return round(rating_avg, 2)
        return 0
    def get_review_num(self, profile):
        return Review.objects.filter(product__seller=profile.user).count()


class ProductDetailSerializer(serializers.ModelSerializer, BaseSerializer):
    seller_profile = SellerProfileSerializer(source='seller.profile')
    images = ProductImageSerializer(source='productimage_set', many=True, required=False)
    options = ProductOptionSerializer(source='productoption_set', many=True, required=False)
    faqs = ProductFaqSerializer(source='productfaq_set', many=True, required=False)
    reviews = ProductReviewSerializer(source='review_set', many=True, required=False)
    is_dibbed = serializers.SerializerMethodField()
    rating_avg = serializers.SerializerMethodField()
    review_num = serializers.IntegerField(source='review_set.count', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_is_dibbed(self, product):
        user = self.get_request_user()
        if user.is_anonymous:
            return None
        else:
            return user.profile.wishlist.filter(id=product.id).exists()

    def get_rating_avg(self, product):
        rating_avg = product.review_set.all().aggregate(Avg('rating')).get('rating__avg', 0)
        if rating_avg:
            return round(rating_avg, 2)
        return 0


class PurchaseListSerializer(serializers.ModelSerializer, BaseSerializer):
    buyer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Purchase
        fields = '__all__'
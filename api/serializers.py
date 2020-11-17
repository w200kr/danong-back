# from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth.models import User
from api.models import SmallCategory, Profile, Product, ProductImage, ProductOption, Purchase, Review

from IPython import embed

# import datetime, copy


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class SignUpSerializer(serializers.ModelSerializer):
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
        # user = User.objects.create(
        #     username=validated_data['username'],
        #     email=validated_data['email']
        # )
        user_profile = Profile.objects.create(
            user=user,
            category=validated_data['profile']['category'],
            name=validated_data['profile']['name'],
            tel=validated_data['profile']['tel'],
        )

        user.set_password(validated_data['password'])
        user.save()
        user_profile.save()
        return user

class LoginSerializer(AuthTokenSerializer):
    category = serializers.CharField(source='user.profile.category', read_only=True)
    name = serializers.CharField(source='user.profile.name', read_only=True)
    zipcode = serializers.CharField(source='user.profile.zipcode', read_only=True)
    address = serializers.CharField(source='user.profile.address', read_only=True)
    address_detail = serializers.CharField(source='user.profile.address_detail', read_only=True)
    tel = serializers.CharField(source='user.profile.tel', read_only=True)
    career = serializers.CharField(source='user.profile.career', read_only=True)
    thumbnail = serializers.CharField(source='user.profile.thumbnail', read_only=True)
    seller_name = serializers.CharField(source='user.profile.seller_name', read_only=True)
    job_position = serializers.CharField(source='user.profile.job_position', read_only=True)
    main_crops = serializers.CharField(source='user.profile.main_crops', read_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmallCategory
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    seller = UserProfileSerializer(default=serializers.CurrentUserDefault())

    # seller = UserProfileSerializer()
    # seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=User.objects.first())
    images = ProductImageSerializer(source='productimage_set', many=True, required=False)
    options = ProductOptionSerializer(source='productoption_set', many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

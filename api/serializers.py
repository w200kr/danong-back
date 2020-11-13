# from django.contrib.auth import authenticate

from rest_framework import serializers
# from rest_framework.authtoken.serializers import AuthTokenSerializer

# from django.contrib.auth.models import User
from api.models import SmallCategory, Profile, Product, ProductImage, ProductOption, Purchase, Review

# from IPython import embed

# import datetime, copy


# class SignUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Member
#         fields = '__all__'
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         member = super().create(validated_data)

#         member.set_password(validated_data['password'])
#         member.save()
#         return member

# class LoginSerializer(AuthTokenSerializer):
#     positions = PositionSerializer(source='user.positions', many=True, read_only=True)
#     team = TeamDetailSerializer(source='user.team', read_only=True)
#     is_graduated = serializers.BooleanField(source='user.is_graduated', read_only=True)
#     student_id = serializers.CharField(source='user.student_id', read_only=True)
#     name = serializers.CharField(source='user.name', read_only=True)
#     tel = serializers.CharField(source='user.tel', read_only=True)
#     comment = serializers.CharField(source='user.comment', read_only=True)


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmallCategory
        fields = '__all__'

class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

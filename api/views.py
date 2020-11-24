# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.generic import TemplateView
# from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import redirect

from rest_framework import mixins, generics, status, filters
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
# from rest_framework import mixins, generics, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
# from rest_framework.exceptions import APIException
from rest_framework.reverse import reverse
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django_filters.rest_framework import DjangoFilterBackend
# import django_filters.rest_framework

from api.serializers import CategoryListSerializer, ProductListSerializer, SignUpSerializer, LoginSerializer, KakaoSignUpSerializer, KakaoLoginSerializer, UserProfileDetailSerializer, ProfileSerializer, ProductDetailSerializer, ProductReviewSerializer, PurchaseListSerializer

from api.models import SmallCategory, Profile, Product, ProductImage, ProductOption, Purchase, Review


from api.filters import ProductFilter
from api.crawls import Crawler

from IPython import embed

import requests
import json


def get_user(request):
    user = None
    if request and hasattr(request, "user"):
        user = request.user
    if settings.DEBUG and user.is_anonymous:
        user = User.objects.get(username='asin')
    return user

class Login(ObtainAuthToken):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)

        obj = {
            **serializer.data,
            'token': token.key,
        }
        obj.pop('password')

        return Response(obj)

class KakaoLogin(generics.GenericAPIView):
    serializer_class = KakaoLoginSerializer
    def post(self, request, *args, **kwargs):
        response_data = {}
        kakao_id = str(request.data.get('kakao_id',''))
        name = str(request.data.get('name',''))
        email = str(request.data.get('email',''))

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        matched_profile = Profile.objects.filter(kakao_id=kakao_id).first()
        if matched_profile:
            user = matched_profile.user
            # response_data['status'] = 'ok'
            # response_data['next_url'] = '/'
            response_data['token'] = user.auth_token.key
        else:
            user = User.objects.create(
                username='kakao_'+kakao_id,
                email=email,
            )
            user_profile = Profile.objects.create(
                user=user,
                category=Profile.BUYER,
                name=name,
                tel='',
                kakao_id=kakao_id,
            )

            user.set_password( User.objects.make_random_password(30) )
            user.save()
            user_profile.save()

            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)

            # response_data['status'] = 'fail'
            # response_data['next_url'] = reverse('kakao-signup')

        data = {
            **serializer.data,
            **response_data,
        }

        return Response(data)

class SignUp(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# class KakaoSignUp(generics.GenericAPIView):
#     serializer_class = KakaoSignUpSerializer
#     def post(self, request, *args, **kwargs):

#         return 

class BaseAPIView(generics.GenericAPIView):
    if not settings.DEBUG:
        authentication_classes = [TokenAuthentication]
        # permission_classes = (IsAuthenticated,)

    def get_request_user(self):
        user = None
        request = self.request
        if request and hasattr(request, "user"):
            user = request.user
        if settings.DEBUG and user.is_anonymous:
            user = User.objects.get(username='asin')
        return user

class CategoryDetph(mixins.ListModelMixin, BaseAPIView):
    queryset = SmallCategory.objects.all()
    serializer_class = CategoryListSerializer

    def get(self, request, *args, **kwargs):
        all_categories = self.list(request, *args, **kwargs).data

        category_depth = [
            {
                'value': value, 
                'label': label, 
                'sub_categories': list(filter(lambda category: category['large_category']==value, all_categories))
            } for index, (value, label) in enumerate(SmallCategory.CATEGORY_CHOICES)
        ]

        return Response(category_depth)


@api_view(['GET'])
def navermap_geocode(request, *args, **kwargs):
    headers = {
        'X-NCP-APIGW-API-KEY-ID': 'm11ogby6ag',
        'X-NCP-APIGW-API-KEY': 'G8nc8zH5sP4pg8ZVMYETnLoReXCfx04vgNKvwsPE',
    }
    if not 'address' in kwargs:
        return Response(status=status.HTTP_404_NOT_FOUND)

    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="+kwargs.get('address', '')
    # url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=망우로12길 49-1"
    response = requests.get(url, headers=headers)

    return Response(response.json())


@api_view(['GET'])
def nongsaro_addresses(request, *args, **kwargs):
    crawler = Crawler()

    try:
        response = crawler.lookup_nongsaro(kwargs.get('address', ''))
    except Exception as e:
        # raise e
        return Response(status=status.HTTP_404_NOT_FOUND)
    finally:
        crawler.driver.close()

    return Response(response)

class ProductList(mixins.ListModelMixin,
                    mixins.CreateModelMixin, 
                    BaseAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['name', 'category__name', 'price']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    # filterset_fields = ['category', 'price']
    parser_class = (MultiPartParser,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    parser_class = (MultiPartParser,)

    def update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

@api_view(['POST'])
def product_dib(request):
    product_id = request.data.get('product_id', None)
    if product_id:
        profile = get_user(request).profile
        if product_id in list(profile.wishlist.values_list('id', flat=True)):
            profile.wishlist.remove(product_id)
        else:
            profile.wishlist.add(product_id)
        profile.save()

        return Response({'status':'ok'}, status=status.HTTP_201_CREATED)
    return Response({'status':'fail'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_class = (MultiPartParser,)


class ReviewList(mixins.ListModelMixin,
                    mixins.CreateModelMixin, 
                    BaseAPIView):
    queryset = Review.objects.all()
    serializer_class = ProductReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ProductReviewSerializer



class PurchaseList(mixins.ListModelMixin,
                    mixins.CreateModelMixin, 
                    BaseAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


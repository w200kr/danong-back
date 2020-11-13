# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.generic import TemplateView
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from django.utils import timezone

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import mixins, generics, viewsets
from rest_framework import mixins, generics
from rest_framework.response import Response


from api.serializers import CategoryListSerializer

# from rest_framework.authentication import TokenAuthentication

from api.models import SmallCategory, Profile, Product, ProductImage, ProductOption, Purchase, Review
# from api.v1.serializers import SignUpSerializer, LoginSerializer, MemberListSerializer, MemberDetailSerializer, ScheduleSerializer, ScheduleListSerializer, PracticeSerializer, PracticeListSerializer, MatchSerializer, MatchListSerializer, DrillListSerializer, PositionSerializer, WorkoutListSerializer, WorkoutDetailSerializer, QuizListSerializer, QuizDetailSerializer
# from api.constants import get_main_positions_by_situation, OFFENSE, DEFENSE, FLAT_POSITION_SET, get_main_positions

# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token

from IPython import embed

import requests
import json



# class Login(ObtainAuthToken):
#     serializer_class = LoginSerializer
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token = Token.objects.get(user=user)

#         obj = {
#             **serializer.data,
#             'token': token.key,
#         }
#         obj.pop('password')

#         return Response(obj)

# class SignUp(mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Member.objects.all()
#     serializer_class = SignUpSerializer

#     def get(self, request, *args, **kwargs):
#         response_data = {
#             'offense_positions': get_main_positions_by_situation(OFFENSE),
#             'defense_positions': get_main_positions_by_situation(DEFENSE),
#         }
#         return Response(response_data)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class BaseAPIView(generics.GenericAPIView):
    pass
    # if not settings.DEBUG:
    #     authentication_classes = [TokenAuthentication]
    #     permission_classes = (IsAuthenticated,)

class CategoryDetph(mixins.ListModelMixin, BaseAPIView):
    queryset = SmallCategory.objects.all()
    serializer_class = CategoryListSerializer

    def get(self, request, *args, **kwargs):
        all_categories = self.list(request, *args, **kwargs).data

        category_depth = [
            {
                'value': value, 
                'label': label, 
                'sub_categories':list(filter(lambda category: category['large_category']==value, all_categories))
            } for index, (value, label) in enumerate(SmallCategory.CATEGORY_CHOICES)
        ]

        return Response(category_depth)


class NaverMapGeocode(BaseAPIView):
    def get(self, request, *args, **kwargs):
        headers = {
            'X-NCP-APIGW-API-KEY-ID': 'm11ogby6ag',
            'X-NCP-APIGW-API-KEY': 'G8nc8zH5sP4pg8ZVMYETnLoReXCfx04vgNKvwsPE',
        }
        if not 'address' in kwargs:
            return Response(status_code=404)

        url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query="+kwargs['address']
        # url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=망우로12길 49-1"
        response = requests.get(url, headers=headers)

        return Response(response.json())


class NongsaroAddresses(BaseAPIView):
    def get(self, request, *args, **kwargs):





        return Response()


from django.urls import path

from api import views

# naming

# list : create list
# detail : Retrieve Update Delete

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    # path('signup/kakao/', views.KakaoSignUp.as_view(), name='kakao-signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('login/kakao/', views.KakaoLogin.as_view(), name='kakao-login'),


    # path('v1/members/<int:pk>', views.MemberList.as_view(), name='member-list'),
    path('categories/depth/', views.CategoryDetph.as_view(), name='category-list'),
    path('navermap/geocode/<str:address>/', views.NaverMapGeocode.as_view(), name='navermap-geocode'),
    path('nongsaro/<str:address>/', views.NongsaroAddresses.as_view(), name='nongsaro-addresses'),


    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/dib/', views.product_dib, name='product-dib'),

    path('profiles/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
]

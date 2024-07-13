from django.urls import path

from users import views


app_name= 'users'

urlpatterns = [
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('registration/',views.registration,name='registration'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('user-cart/',views.user_cart,name='user_cart'),
    ]
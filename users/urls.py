from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import UserCreateView, UserProfileUpdateView, UserProfileView
# from .views import

app_name = 'users'

urlpatterns = [
    # path('', animals.index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name ='logout'),
    path('user/create/', UserCreateView.as_view(), name ='user_create'),
    path('user/<int:pk>/update/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('user/<int:pk>/', UserProfileView.as_view(), name='detail_profile'),

]


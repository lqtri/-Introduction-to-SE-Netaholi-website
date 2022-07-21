from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('register', views.choose_acc_register_view, name='register'),
    path('register/<str:account_type>', views.account_register_view, name='register'),
    path('login', views.login_page_view, name='login'),
    path('logout', views.logout_page_view, name='logout'),
    path('changepwd', views.change_password_view, name='changepwd'),
    path('activate/<str:uidb64>/<str:token>', views.activate_view, name='activate')
]

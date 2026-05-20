from django.urls import include, path

from shop import views
urlpatterns = [
    path('', views.cars_view, name='cars'),
    path('ads/<int:id>/', views.ad_detail, name='ad_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('create-ad/', views.create_ad_view, name='create_ad'),
    path('delete-ad/<int:id>/', views.delete_ad_view, name='delete_ad'),
    path('change-status/', views.change_status_view, name='change_status'),
]


from django.urls import path
from .views import *

app_name = 'customadmin'
urlpatterns = [
    path('', admin_login, name="admin_login"),
    path('dashboard/', dashboard, name="dashboard"),

    path('tweet/<int:tweet_id>/', tweet_detail, name="tweet_detail"),
    path('tweet/create/', tweet_create_now, name="tweet_create_now"),
    path('tweet/<int:tweet_id>/update/', tweet_update, name="tweet_update"),
    path('tweet/<int:tweet_id>/delete/', tweet_delete, name="tweet_delete"),
    path('logout/', admin_logout, name='admin_logout'),
]

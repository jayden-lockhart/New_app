from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path(
        'register_reader/',
        views.register_reader,
        name='register_reader',
    ),
    path(
        'register_editor/',
        views.register_editor,
        name='register_editor',
    ),
    path(
        'register_journalist/',
        views.register_journalist,
        name='register_journalist',
    ),
    path('logout/', views.logout_user, name='logout'),
    path('home', views.home, name='home'),
    path(
        'view_reader/',
        views.view_reader,
        name='view_reader',
    ),
    path(
        'view_editor/',
        views.view_editor,
        name='view_editor',
    ),
    path(
        'view_journalist/',
        views.view_journalist,
        name='view_journalist',
    ),
]

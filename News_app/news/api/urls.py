from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path(
        'GET/articles/',
        views.view_approved_articles,
        name='get_articles',
    ),
    path(
        'GET/articles/subscribed/',
        views.view_subscribed_articles,
        name='get_subscribed_articles',
    ), 
    path(
        'GET/article/<id>/',
        views.view_single_article,
        name='get_article',
    ),
    path(
        'POST/article/',
        views.create_article,
        name='create_article',
    ),
    path(
        'PUT/articles/<id>/',
        views.update_article,
        name='update_article',
    ),
    path(
        'DELETE/article/<id>/',
        views.delete_article,
        name='delete_articles',
    ),
    path(
        'api-token-auth/',
        obtain_auth_token,
        name='api-token-auth'),
    path(
        "protected_view",
        views.protected_view,
        name="protected_view"
        ),


]

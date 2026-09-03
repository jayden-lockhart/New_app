from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import Article, User
from .serializers import ArticleSerializer, subscribeArticleSerializer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication



# Create your views here.


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": f"Hello, {request.user.username}!"})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@api_view(['GET'])
@login_required(login_url='login')
def view_approved_articles(request):
    '''GET /api/articles/: Return a list of all approved articles.'''
    articles = Article.objects.filter(approved=True)
    serializer = ArticleSerializer(articles, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@login_required(login_url='login')
def view_subscribed_articles(request):
    '''GET /api/articles/subscribed/: Return articles only from the reader’s
    subscribed publishers/journalists.'''
    user = request.user
    reader_profile = user.readerprofile
    subscribed_publishers = reader_profile.publishers.all()
    subscribed_journalists = reader_profile.journalists.all()

    articles = Article.objects.filter(
        approved=True,
        publisher__in=subscribed_publishers
    ) | Article.objects.filter(
        approved=True,
        author__in=subscribed_journalists
    )

    serializer = ArticleSerializer(articles, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@login_required(login_url='login')
def view_single_article(request, id):
    '''GET /api/articles/<id>/: Retrieve a single article.'''
    try:
        article = Article.objects.get(id=id, approved=True)
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data, safe=False)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)


@api_view(['POST'])
@login_required(login_url='login')
@allowed_users(allowed_roles=['JOURNALIST'])
def create_article(request):
    '''POST /api/articles/: Create article (journalists only).'''

    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['PUT'])
@login_required(login_url='login')
@allowed_users(allowed_roles=['JOURNALIST', 'EDITOR'])
def update_article(request, id):
    '''PUT /api/articles/<id>/: Update article (editors/journalists).'''

    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)

    if request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@api_view(['DELETE'])
@login_required(login_url='login')
@allowed_users(allowed_roles=['JOURNALIST', 'EDITOR'])
def delete_article(request, id):
    '''DELETE /api/articles/<id>/: Delete article (editors/journalists).'''
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article not found'}, status=404)

    if request.method == 'DELETE':
        article.delete()
        return JsonResponse(
            {'message': 'Article deleted successfully'}, status=204)

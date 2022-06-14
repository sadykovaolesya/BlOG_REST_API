from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.models import User
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Subscribe
from .serializers import (AuthorSerializer, PostSerializer,
                          PostSubscribeSerializer, SubscribeSerializer)
from .service import AuthorFilter, PostIsReadFilter, PostSubscribePagination

 
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class PostAPIViews(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.auth:     
            cache_key = "post_users_%s" % self.request.user.id
            post = cache.get(cache_key)
            if not post:
                post = Post.objects.exclude(author=self.request.user)
                cache.set(
                cache_key, post,
                timeout=CACHE_TTL 
            )
        else:
            cache_key = "post_users"
            post = cache.get(cache_key)
            if not post:
                post = Post.objects.all()
                cache.set(
                cache_key, post,
                timeout=CACHE_TTL 
            )            
        return post


class PostSubscribeDetailViews(generics.RetrieveUpdateAPIView):
    serializer_class = PostSubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subscribe = Subscribe.objects.select_related().filter(subscriber=self.request.user)
        author = [subscribe.author for subscribe in subscribe]
        post = Post.objects.select_related().filter(author__username__in=author).prefetch_related('read_users')
        return post


class PostSubscribeListViews(generics.ListAPIView):
    serializer_class = PostSubscribeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostSubscribePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostIsReadFilter

    def get_queryset(self):
        user = self.request.user
        subscribe = Subscribe.objects.select_related().filter(subscriber=user)
        author = [subscribe.author for subscribe in subscribe]
        post = Post.objects.select_related().filter(author__username__in=author).prefetch_related('read_users')
        return post


class UserListViews(generics.ListCreateAPIView):

    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter

    def get_queryset(self):
        authors = cache.get('authors')
        if not authors:
            authors = User.objects.annotate(count_post=Count("post"))
            cache.set(
                'authors', authors, 
                 timeout=CACHE_TTL
            )
        return authors


class SubscribeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscribe = Subscribe.objects.filter(subscriber=request.user)
        serializer = SubscribeSerializer(subscribe, many=True)
        return Response(serializer.data)

    def delete(self, request):
        subscribe = Subscribe.objects.filter(
            subscriber=request.user, author=request.data.get("author")
        )
        if subscribe.exists():
            subscribe.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

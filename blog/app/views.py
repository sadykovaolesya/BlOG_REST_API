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


class PostAPIViews(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.auth:
            post = Post.objects.exclude(author=self.request.user)
        else:
            post = Post.objects.all()
        return post


class PostSubscribeDetailViews(generics.RetrieveUpdateAPIView):
    serializer_class = PostSubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subscribe = Subscribe.objects.filter(subscriber=self.request.user)
        author = [subscribe.author for subscribe in subscribe]
        post = Post.objects.filter(author__username__in=author)
        return post


class PostSubscribeListViews(generics.ListAPIView):
    serializer_class = PostSubscribeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostSubscribePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostIsReadFilter

    def get_queryset(self):
        user = self.request.user
        subscribe = Subscribe.objects.filter(subscriber=user)
        author = [subscribe.author for subscribe in subscribe]
        post = Post.objects.filter(author__username__in=author)
        return post


class UserListViews(generics.ListCreateAPIView):

    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter

    def get_queryset(self):
        authors = User.objects.annotate(count_post=Count("post"))
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

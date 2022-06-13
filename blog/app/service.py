from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

from .models import Post


class PostSubscribePagination(PageNumberPagination):
    page_size = 10


class AuthorFilter(filters.FilterSet):
    count_post = filters.NumberFilter(field_name="count_post")

    o = filters.OrderingFilter(
        fields=(("count_post", "count_post"),),
        field_labels={
            "count_post": "Number of posts",
        },
    )

    class Meta:
        model = User
        fields = ("count_post",)


class PostIsReadFilter(filters.FilterSet):
    is_read = filters.BooleanFilter(field_name="is_read", method="get_read_status")

    def get_read_status(self, queryset, field_name, value):
        if value:
            return queryset.filter(read_users=self.request.user)
        else:
            return queryset.exclude(read_users=self.request.user)

    class Meta:
        model = Post
        fields = ("is_read",)

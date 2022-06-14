from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Subscribe


class PostSerializer(serializers.ModelSerializer):
    """Serializes the post"""

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        exclude = ["read_users"]


class PostSubscribeSerializer(serializers.ModelSerializer):
    """Serializes the subscription post"""

    author = serializers.SlugRelatedField(slug_field="username", read_only="True")
    title = serializers.CharField(read_only="True")
    content = serializers.CharField(read_only="True")

    class Meta:
        model = Post
        exclude = ["read_users"]

    def to_representation(self, instance):
        """is_read field added"""
        representation = super().to_representation(instance)
        representation["is_read"] = (
            self.context["request"].user in instance.read_users.all()
        )
        return representation

    def to_internal_value(self, data):
        """Validate check is_read"""
        is_read = data.get("is_read").lower()
        if is_read == "true" or is_read == "false":
            return {"is_read": is_read}
        else:
            raise TypeError("is_read must be boolean")

    def update(self, instance, validated_data):
        post = instance
        if validated_data.get("is_read") == "true":
            post.read_users.add(self.context["request"].user)
        else:
            post.read_users.remove(self.context["request"].user)
        return post


class AuthorSerializer(serializers.Serializer):
    """Serializes user"""

    author = serializers.CharField(source="username")
    count_post = serializers.IntegerField(read_only=True)
    subscriber = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        if data["username"] == data["subscriber"].username:
            raise serializers.ValidationError("You cannot subscribe to yourself")
        elif Subscribe.objects.filter(
            author__username=data["username"], subscriber=data["subscriber"]
        ).exists():
            raise serializers.ValidationError("Subscription already exists")
        return data

    def create(self, validated_data):
        user = User.objects.get(username=validated_data.pop("username"))
        Subscribe.objects.create(author=user, **validated_data)
        return user


class SubscribeSerializer(serializers.ModelSerializer):
    """Serializes subscribe"""

    subscriber = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscribe
        fields = "__all__"

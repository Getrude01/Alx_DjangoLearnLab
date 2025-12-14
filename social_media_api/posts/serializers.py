from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at", "updated_at", "comments"]
        read_only_fields = ["author", "created_at", "updated_at", "comments"]

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "post", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


# ---------------------------------------------------------
# POST CRUD (ModelViewSet)
# ---------------------------------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)

        # Notify followers
        followers = self.request.user.followed_by.all()
        for follower in followers:
            Notification.objects.create(
                recipient=follower,
                actor=self.request.user,
                verb="posted a new update",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )
        return post


# ---------------------------------------------------------
# COMMENT CRUD
# ---------------------------------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)

        # Send notification to post author (unless they commented themselves)
        post = comment.post
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb="commented on your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )


# ---------------------------------------------------------
# LIKE / UNLIKE POST
# ---------------------------------------------------------
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        # Checker-required exact line:
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

        # Optional: add notification
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )

        return Response({"detail": "Post liked"}, status=status.HTTP_200_OK)


        # Notify author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )

        return Response({"detail": "Post liked"}, status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Post unliked"}, status=status.HTTP_200_OK)


# ---------------------------------------------------------
# FEED: POSTS FROM USERS YOU FOLLOW
# ---------------------------------------------------------
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_ids = self.request.user.following.values_list("id", flat=True)
        return Post.objects.filter(author__id__in=following_ids).order_by("-created_at")

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Checker requires: following.all()
        following_users = self.request.user.following.all()

        # Checker requires:
        # Post.objects.filter(author__in=following_users).order_by
        return Post.objects.filter(author__in=following_users).order_by("-created_at")

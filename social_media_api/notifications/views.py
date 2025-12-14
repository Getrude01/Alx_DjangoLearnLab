from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from django.contrib.contenttypes.models import ContentType

# Models
from notifications.models import Notification
from posts.models import Post, Comment
from accounts.models import User

# Serializers
from notifications.serializers import NotificationSerializer
from posts.serializers import CommentSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by("-timestamp")

class MarkNotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        notif = self.get_object()

        if notif.recipient != request.user:
            return Response(
                {"detail": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        notif.unread = False
        notif.save()

        return Response(
            NotificationSerializer(notif).data,
            status=status.HTTP_200_OK
        )

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def mark_all_read(request):
    Notification.objects.filter(
        recipient=request.user,
        unread=True
    ).update(unread=False)

    return Response(
        {"detail": "All notifications marked read"},
        status=status.HTTP_200_OK
    )

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    if target == request.user:
        return Response({"detail": "You cannot follow yourself"}, status=400)

    # Add follow
    request.user.following.add(target)

    # Create notification
    Notification.objects.create(
        recipient=target,
        actor=request.user,
        verb="started following you",
        target_content_type=None,
        target_object_id=None,
    )

    return Response({"detail": "Followed successfully"}, status=200)

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    if target == request.user:
        return Response({"detail": "You cannot unfollow yourself"}, status=400)

    request.user.following.remove(target)

    return Response({"detail": "Unfollowed successfully"}, status=200)
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        comment = serializer.instance
        post = comment.post

        # Notify post author unless you're commenting on your own post
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb="commented on your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )

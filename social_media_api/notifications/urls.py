from django.urls import path
from .views import NotificationListView, MarkNotificationReadView, mark_all_read

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications-list"),
    path("mark-read/<int:pk>/", MarkNotificationReadView.as_view(), name="notification-mark-read"),
    path("mark-all-read/", mark_all_read, name="notification-mark-all-read"),
]
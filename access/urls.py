from django.urls import path

from .views import (
    RolePermissionListView,
    RolePermissionCreateView,
    RolePermissionUpdateView,
    RolePermissionDeleteView,
)

urlpatterns = [
    path("access-rules/", RolePermissionListView.as_view()),
    path("access-rules/create/", RolePermissionCreateView.as_view()),
    path("access-rules/<int:pk>/", RolePermissionUpdateView.as_view()),
    path(
        "access-rules/<int:pk>/delete/",
        RolePermissionDeleteView.as_view(),
    ),
]

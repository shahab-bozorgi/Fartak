from django.urls import path

from .views import (
    DocumentCategoryListCreateAPIView,
    DocumentCategoryRetrieveUpdateDestroyAPIView,
    DocumentTypeListCreateAPIView,
    DocumentTypeRetrieveUpdateDestroyAPIView,
    DocumentListCreateAPIView,
    DocumentRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("document-categories/", DocumentCategoryListCreateAPIView.as_view(), name="document-category-list-create"),
    path("document-categories/<int:pk>/", DocumentCategoryRetrieveUpdateDestroyAPIView.as_view(),
         name="document-category-detail"),

    path("document-types/", DocumentTypeListCreateAPIView.as_view(), name="document-type-list-create"),
    path("document-types/<int:pk>/", DocumentTypeRetrieveUpdateDestroyAPIView.as_view(), name="document-type-detail"),

    path("documents/", DocumentListCreateAPIView.as_view(), name="document-list-create"),
    path("documents/<int:pk>/", DocumentRetrieveUpdateDestroyAPIView.as_view(), name="document-detail"),
]

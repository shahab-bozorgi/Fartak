from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import DocumentCategory, DocumentType, Document
from .serializers import DocumentCategorySerializer, DocumentTypeSerializer, DocumentSerializer


# DocumentCategory Views
class DocumentCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentCategory.objects.filter(is_deleted=False)
    serializer_class = DocumentCategorySerializer

    @extend_schema(
        summary="List all document categories",
        responses=DocumentCategorySerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new document category",
        request=DocumentCategorySerializer,
        responses=DocumentCategorySerializer,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DocumentCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentCategory.objects.filter(is_deleted=False)
    serializer_class = DocumentCategorySerializer

    @extend_schema(
        summary="Retrieve a document category",
        responses=DocumentCategorySerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Fully update a document category",
        request=DocumentCategorySerializer,
        responses=DocumentCategorySerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a document category",
        request=DocumentCategorySerializer,
        responses=DocumentCategorySerializer,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Soft delete a document category",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


# DocumentType Views
class DocumentTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentType.objects.filter(is_deleted=False)
    serializer_class = DocumentTypeSerializer

    @extend_schema(
        summary="List all document types",
        responses=DocumentTypeSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new document type",
        request=DocumentTypeSerializer,
        responses=DocumentTypeSerializer,
    )
    def post(self, request, *args, **kwargs):
        category_id = request.data.get("category_id")
        if not DocumentCategory.objects.filter(id=category_id, is_deleted=False).exists():
            return Response({"category_id": ["Invalid or deleted category"]}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class DocumentTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentType.objects.filter(is_deleted=False)
    serializer_class = DocumentTypeSerializer

    @extend_schema(
        summary="Retrieve a document type",
        responses=DocumentTypeSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Fully update a document type",
        request=DocumentTypeSerializer,
        responses=DocumentTypeSerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a document type",
        request=DocumentTypeSerializer,
        responses=DocumentTypeSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Soft delete a document type",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


# Document Views
class DocumentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer

    @extend_schema(
        summary="List all documents",
        responses=DocumentSerializer(many=True),
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new document",
        request=DocumentSerializer,
        responses=DocumentSerializer,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer

    @extend_schema(
        summary="Retrieve a document",
        responses=DocumentSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Fully update a document",
        request=DocumentSerializer,
        responses=DocumentSerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a document",
        request=DocumentSerializer,
        responses=DocumentSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Soft delete a document",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

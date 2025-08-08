from django.db.models import Count, Q, Prefetch
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from PyPDF2 import PdfReader
from .models import DocumentCategory, DocumentType, Document, UploadedTextFile
from .schemas.type import  (
    document_type_list_schema,
    document_type_list_schema,
    document_type_create_schema,
    document_type_retrieve_schema,
    document_type_update_schema,
    document_type_partial_update_schema,
    document_type_delete_schema,
)
from .serializers import DocumentCategorySerializer, DocumentTypeSerializer, DocumentSerializer, \
    CategoryWithDocTypeStatsSerializer
from .services.category import DocumentCategoryService
from .schemas.category import (
    category_list_create_schema,
    category_create_schema,
    category_retrieve_schema,
    category_update_schema,
    category_partial_update_schema,
    category_delete_schema,
    category_list_with_filters_schema, category_with_type_and_count_schema,
)
from .schemas.document import (
    document_list_schema,
    document_create_schema,
    document_retrieve_schema,
    document_update_schema,
    document_partial_update_schema,
    document_delete_schema,
)
from .services.document import DocumentService
from .services.type import DocumentTypeService


class DocumentCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentCategory.objects.filter(is_deleted=False)
    serializer_class = DocumentCategorySerializer

    @category_list_create_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @category_create_schema
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@category_list_with_filters_schema
class DocumentCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentCategory.objects.filter(is_deleted=False)
    serializer_class = DocumentCategorySerializer

    @category_retrieve_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @category_update_schema
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @category_partial_update_schema
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @category_delete_schema
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        DocumentCategoryService.soft_delete_category(instance)

class DocumentTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentType.objects.filter(is_deleted=False)
    serializer_class = DocumentTypeSerializer

    @document_type_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @document_type_create_schema
    def post(self, request, *args, **kwargs):
        category_id = request.data.get("category_id")
        if not DocumentTypeService.validate_category_exists(category_id):
            return Response({"category_id": ["Invalid or deleted category"]}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request, *args, **kwargs)


class DocumentTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentType.objects.filter(is_deleted=False)
    serializer_class = DocumentTypeSerializer

    @document_type_retrieve_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @document_type_update_schema
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @document_type_partial_update_schema
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @document_type_delete_schema
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        DocumentTypeService.soft_delete(instance)

    def perform_update(self, serializer):
        old_instance = self.get_object()
        new_instance = serializer.save()
        DocumentTypeService.cleanup_uploaded_text_if_visibility_removed(old_instance, new_instance)

class DocumentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer

    @document_list_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @document_create_schema
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        doc_type = serializer.validated_data['document_type']
        is_active = serializer.validated_data.get('is_active', False)

        if is_active:
            DocumentService.ensure_single_active(doc_type)

        document = serializer.save()
        DocumentService.save_uploaded_text(document)


class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer

    @document_retrieve_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @document_update_schema
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @document_partial_update_schema
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @document_delete_schema
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        DocumentService.soft_delete(instance)



class CategoryWithTypeAndDocCountAPIView(generics.ListAPIView):
    serializer_class = CategoryWithDocTypeStatsSerializer

    @category_with_type_and_count_schema
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        participant_id = self.request.query_params.get('participant_id')
        category_id = self.request.query_params.get('category_id')
        has_active_type = self.request.query_params.get('has_active_type')

        return CategoryService.get_filtered_categories_with_types(
            participant_id=participant_id,
            category_id=category_id,
            has_active_type=has_active_type
        )
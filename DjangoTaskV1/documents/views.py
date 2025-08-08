from django.db.models import Count, Q, Prefetch
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from PyPDF2 import PdfReader
from .models import DocumentCategory, DocumentType, Document, UploadedTextFile
from .serializers import DocumentCategorySerializer, DocumentTypeSerializer, DocumentSerializer, \
    CategoryWithDocTypeStatsSerializer


class DocumentCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentCategory.objects.filter(is_deleted=False)
    serializer_class = DocumentCategorySerializer

    @extend_schema(summary="List all document categories",responses=DocumentCategorySerializer(many=True),)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Create a new document category",request=DocumentCategorySerializer,responses=DocumentCategorySerializer,)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@extend_schema(
    summary="List categories with document type and document count",
    parameters=[
        OpenApiParameter("participant_id", OpenApiTypes.INT, OpenApiParameter.QUERY),
        OpenApiParameter("category_id", OpenApiTypes.INT, OpenApiParameter.QUERY),
        OpenApiParameter("has_active_type", OpenApiTypes.BOOL, OpenApiParameter.QUERY),
    ]
)
class CategoryWithTypeAndDocCountAPIView(generics.ListAPIView):
    serializer_class = CategoryWithDocTypeStatsSerializer

    def get_queryset(self):
        queryset = DocumentCategory.objects.filter(is_deleted=False)

        participant_id = self.request.query_params.get('participant_id')
        if participant_id:
            queryset = queryset.filter(participant_id=participant_id)

        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(id=category_id)

        has_active_type = self.request.query_params.get('has_active_type')
        if has_active_type == 'true':
            queryset = queryset.filter(
                documenttype__is_active=True,
                documenttype__is_deleted=False
            ).distinct()

        types = DocumentType.objects.filter(is_deleted=False).annotate(
            document_count=Count('document', filter=Q(document__is_deleted=False))
        )

        return queryset.prefetch_related(Prefetch('documenttype_set', queryset=types))


class DocumentCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentCategory.objects.filter(is_deleted=False)
    serializer_class = DocumentCategorySerializer

    @extend_schema(summary="Retrieve a document category",responses=DocumentCategorySerializer,)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Fully update a document category",request=DocumentCategorySerializer,responses=DocumentCategorySerializer,)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Partially update a document category",request=DocumentCategorySerializer,responses=DocumentCategorySerializer,)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Soft delete a document category",responses={204: None},)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class DocumentTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentType.objects.filter(is_deleted=False)
    serializer_class = DocumentTypeSerializer

    @extend_schema(summary="List all document types",responses=DocumentTypeSerializer(many=True),)
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

    def perform_update(self, serializer):
        old_instance = self.get_object()

        was_active = old_instance.is_active
        was_private_visible = old_instance.private_visible
        was_public_visible = old_instance.public_visible

        instance = serializer.save()

        if (
                was_active != instance.is_active or
                was_private_visible != instance.private_visible or
                was_public_visible != instance.public_visible
        ):
            if not (
                    instance.is_active and
                    (instance.private_visible or instance.public_visible)
            ):
                from .models import UploadedTextFile
                UploadedTextFile.objects.filter(document_type=instance).delete()


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

    def perform_create(self, serializer):
        doc_type = serializer.validated_data['document_type']
        is_active = serializer.validated_data.get('is_active', False)

        if is_active:
            old_active_doc = Document.objects.filter(
                document_type=doc_type,
                is_active=True,
                is_deleted=False
            ).first()

            if old_active_doc:
                old_active_doc.is_active = False
                old_active_doc.save()

                if old_active_doc.document_type.public_visible or old_active_doc.document_type.private_visible:
                    UploadedTextFile.objects.filter(document=old_active_doc).delete()

        document = serializer.save()
        file = document.file

        if (
                document.is_active and
                (doc_type.public_visible or doc_type.private_visible) and
                file.name.endswith(".pdf")
        ):
            try:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""

                UploadedTextFile.objects.create(
                    document=document,
                    document_type=doc_type,
                    text=text
                )
            except Exception as e:
                print(f"Error reading PDF: {e}")


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


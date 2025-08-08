from drf_spectacular.utils import extend_schema
from documents.serializers import DocumentTypeSerializer

document_type_list_schema = extend_schema(
    summary="List all document types",
    responses=DocumentTypeSerializer(many=True),
)

document_type_create_schema = extend_schema(
    summary="Create a new document type",
    request=DocumentTypeSerializer,
    responses=DocumentTypeSerializer,
)

document_type_retrieve_schema = extend_schema(
    summary="Retrieve a document type",
    responses=DocumentTypeSerializer,
)

document_type_update_schema = extend_schema(
    summary="Fully update a document type",
    request=DocumentTypeSerializer,
    responses=DocumentTypeSerializer,
)

document_type_partial_update_schema = extend_schema(
    summary="Partially update a document type",
    request=DocumentTypeSerializer,
    responses=DocumentTypeSerializer,
)

document_type_delete_schema = extend_schema(
    summary="Soft delete a document type",
    responses={204: None},
)

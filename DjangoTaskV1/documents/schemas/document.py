from drf_spectacular.utils import extend_schema

from documents.serializers import DocumentSerializer

document_list_schema = extend_schema(
    summary="List all documents",
    responses=DocumentSerializer(many=True)
)

document_create_schema = extend_schema(
    summary="Create a new document",
    request=DocumentSerializer,
    responses=DocumentSerializer
)

document_retrieve_schema = extend_schema(
    summary="Retrieve a document",
    responses=DocumentSerializer
)

document_update_schema = extend_schema(
    summary="Fully update a document",
    request=DocumentSerializer,
    responses=DocumentSerializer
)

document_partial_update_schema = extend_schema(
    summary="Partially update a document",
    request=DocumentSerializer,
    responses=DocumentSerializer
)

document_delete_schema = extend_schema(
    summary="Soft delete a document",
    responses={204: None}
)
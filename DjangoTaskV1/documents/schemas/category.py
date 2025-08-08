# documents/schemas/category_schemas.py

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from documents.serializers import DocumentCategorySerializer, CategoryWithDocTypeStatsSerializer

category_list_create_schema = extend_schema(
    summary="List all document categories",
    responses=DocumentCategorySerializer(many=True)
)

category_create_schema = extend_schema(
    summary="Create a new document category",
    request=DocumentCategorySerializer,
    responses=DocumentCategorySerializer
)

category_retrieve_schema = extend_schema(
    summary="Retrieve a document category",
    responses=DocumentCategorySerializer
)

category_update_schema = extend_schema(
    summary="Fully update a document category",
    request=DocumentCategorySerializer,
    responses=DocumentCategorySerializer
)

category_partial_update_schema = extend_schema(
    summary="Partially update a document category",
    request=DocumentCategorySerializer,
    responses=DocumentCategorySerializer
)

category_delete_schema = extend_schema(
    summary="Soft delete a document category",
    responses={204: None}
)

category_list_with_filters_schema = extend_schema(
    summary="List categories with document type and document count",
    parameters=[
        OpenApiParameter("participant_id", OpenApiTypes.INT, OpenApiParameter.QUERY),
        OpenApiParameter("category_id", OpenApiTypes.INT, OpenApiParameter.QUERY),
        OpenApiParameter("has_active_type", OpenApiTypes.BOOL, OpenApiParameter.QUERY),
    ]
)




category_with_type_and_count_schema = extend_schema(
    summary="List categories with document type and document count",
    parameters=[
        OpenApiParameter("participant_id", OpenApiTypes.INT, OpenApiParameter.QUERY),
        OpenApiParameter("category_id", OpenApiTypes.INT, OpenApiParameter.QUERY),
        OpenApiParameter("has_active_type", OpenApiTypes.BOOL, OpenApiParameter.QUERY),
    ],
    responses=CategoryWithDocTypeStatsSerializer(many=True)
)
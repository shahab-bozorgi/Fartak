from rest_framework import serializers

from documents.models import Document, DocumentCategory, DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentCategory.objects.filter(is_deleted=False),
        source='category',
        write_only=True
    )
    category = serializers.StringRelatedField(read_only=True)
    document_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = DocumentType
        fields = [
            'id',
            'category_id',
            'category',
            'title',
            'private_visible',
            'public_visible',
            'document_count',
            'is_active',
            'is_deleted',
        ]
        read_only_fields = ['id', 'is_deleted']

    def validate(self, attrs):
        # -------------------------------------
        return attrs

class DocumentCategorySerializer(serializers.ModelSerializer):
    types = DocumentTypeSerializer(many=True, write_only=True)
    document_types = DocumentTypeSerializer(source='types', many=True, read_only=True)

    class Meta:
        model = DocumentCategory
        fields = ['id', 'company', 'participant', 'title', 'is_deleted', 'types', 'document_types']
        read_only_fields = ['id', 'is_deleted']

    def create(self, validated_data):
        types_data = validated_data.pop('types', [])
        category = DocumentCategory.objects.create(**validated_data)
        for type_data in types_data:
            type_data.pop('category', None)
            DocumentType.objects.create(category=category, **type_data)
        return category

    def update(self, instance, validated_data):
        types_data = validated_data.pop('types', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if types_data is not None:
            sent_type_ids = [t.get('id') for t in types_data if t.get('id') is not None]

            instance.types.exclude(id__in=sent_type_ids).delete()

            for type_data in types_data:
                type_id = type_data.pop('id', None)
                type_data.pop('category', None)

                if type_id:
                    try:
                        doc_type = instance.types.get(id=type_id)
                        for attr, value in type_data.items():
                            setattr(doc_type, attr, value)
                        doc_type.save()
                    except DocumentType.DoesNotExist:
                        continue
                else:
                    DocumentType.objects.create(category=instance, **type_data)

        return instance


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'company',
            'participant',
            'document_type',
            'file',
            'is_active',
            'is_deleted',
        ]
        read_only_fields = ['id', 'is_deleted']

    def create(self, validated_data):
        document_type = validated_data['document_type']

        has_active_doc = Document.objects.filter(
            document_type=document_type,
            is_active=True,
            is_deleted=False
        ).exists()

        if not has_active_doc:
            validated_data['is_active'] = True
        else:
            validated_data['is_active'] = validated_data.get('is_active', False)

        return super().create(validated_data)

class DocumentTypeWithCountSerializer(serializers.ModelSerializer):
    document_count = serializers.IntegerField()

    class Meta:
        model = DocumentType
        fields = ['id', 'title', 'is_active', 'public_visible', 'private_visible', 'document_count']

class CategoryWithDocTypeStatsSerializer(serializers.ModelSerializer):
    types = serializers.SerializerMethodField()

    class Meta:
        model = DocumentCategory
        fields = ['id', 'title', 'participant', 'company', 'types']

    def get_types(self, obj):
        types = getattr(obj, 'documenttype_set', [])
        return DocumentTypeWithCountSerializer(types, many=True).data
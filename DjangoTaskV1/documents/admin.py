from django.contrib import admin

from documents.models import Document, Participant, DocumentType, DocumentCategory, UploadedTextFile

admin.site.register(Participant)
admin.site.register(Document)
admin.site.register(DocumentType)
admin.site.register(DocumentCategory)
admin.site.register(UploadedTextFile)





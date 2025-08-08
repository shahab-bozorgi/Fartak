from django.db import models

class Participant(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('not_active', 'Not Active'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class DocumentCategory (models.Model):
    company = models.IntegerField()
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company} {self.participant} {self.title}"

class DocumentType(models.Model):
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    private_visible = models.BooleanField()
    public_visible = models.BooleanField()
    is_active = models.BooleanField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category} {self.title}"


class Document(models.Model):
    company = models.IntegerField()
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/documents')
    is_active = models.BooleanField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company} {self.participant} {self.document_type}"

class UploadedTextFile (models.Model):
    text = models.TextField()
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.document_type} {self.document}"
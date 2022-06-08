import mimetypes

from django.conf import settings as django_settings
from django.db import transaction
from django.http import FileResponse
from django.utils.timezone import now
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from core import models


class DocumentUploadService:

    def __init__(self, user, path, file):
        self.user = user
        self.path = path if path.startswith('/') else '/' + path
        self.file = file

    def _find_document(self) -> 'models.Document':
        return models.Document.objects.find_by_path(
            user_id=self.user.id,
            path=self.path
        )

    @staticmethod
    def _create_revision(document: 'models.Document', revision: int):
        obj = models.DocumentRevision()
        obj.document = document
        obj.file = document.file
        obj.file_name = document.file_name
        obj.uploaded_at = document.uploaded_at
        obj.revision = revision
        return obj.save()

    def _update_or_create_document(self, document: 'models.Document', revision: int):
        document.user = self.user
        document.path = self.path
        document.file = self.file
        document.file_name = self.file.name
        document.uploaded_at = now()
        document.revision = revision
        return document.save()

    @transaction.atomic
    def upload(self):
        # check if document exists
        document = self._find_document()
        if document:
            # increasing revision
            revision = document.revision + 1

        else:
            # setting up first revision
            revision = 0

            # creating new instance
            document = models.Document()

        # updating or creating document to the last file and revision
        self._update_or_create_document(document=document, revision=revision)

        # creating revision for the document
        self._create_revision(document=document, revision=revision)

        data = {'id': document.id, 'revision': document.revision}
        return Response(data=data)


class DocumentDownloadService:

    def __init__(self, user, path, revision=None):
        self.user = user
        self.path = path if path.startswith('/') else '/' + path
        self.revision = revision

    @staticmethod
    def get_file_response(file):
        file_path = django_settings.MEDIA_ROOT / file.name
        if not file_path.exists():
            raise APIException('No files found')

        content_type, encoding = mimetypes.guess_type(str(file_path))
        content_type = content_type or 'application/octet-stream'
        response = FileResponse(file_path.open("rb"), content_type=content_type)
        if encoding:
            response.headers['Content-Encoding'] = encoding

        return response

    def download(self):
        # get document by path
        document = models.Document.objects.find_by_path(
            user_id=self.user.id,
            path=self.path
        )
        if not document:
            raise APIException('No documents found')

        # initializing file with last version
        file = document.file

        # looking for a specific revision
        if self.revision is not None:
            # searching for revision
            document_revision = models.DocumentRevision.objects.find_by_revision(
                document_id=document.id,
                revision=self.revision
            )
            if not document_revision:
                raise APIException('No revisions found')

            # change file to the revision specified
            file = document_revision.file

        # return file response
        return self.get_file_response(file=file)

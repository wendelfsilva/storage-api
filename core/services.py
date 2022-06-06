import mimetypes

from django.conf import settings as django_settings
from django.http import FileResponse
from rest_framework.exceptions import APIException

from core import models, helpers


class DocumentDownloadService:

    def __init__(self, request, path: str):
        self.request = request
        self.user = request.user
        self.path = path

    def get_real_revision(self, revision: int = None):
        if revision is None:
            current_revision = models.Document.objects.find_current_revision(
                user_id=self.user.id,
                path=self.path,
            )
            if not current_revision:
                raise APIException('No documents found')

            revision = current_revision.revision

        return revision

    def get_normalized_path(self, revision: int):
        return helpers.normalize_path(
            username=self.user.username,
            path=self.path,
            revision=revision
        )

    @staticmethod
    def get_file_response(path):
        file_path = django_settings.MEDIA_ROOT / path
        if not file_path.exists():
            raise APIException('No files found')

        content_type, encoding = mimetypes.guess_type(str(file_path))
        content_type = content_type or 'application/octet-stream'
        response = FileResponse(file_path.open("rb"), content_type=content_type)
        if encoding:
            response.headers['Content-Encoding'] = encoding

        return response

    def download(self, revision: int = None):
        # get real revision
        revision = self.get_real_revision(revision=revision)

        # normalize path
        path = self.get_normalized_path(revision=revision)

        # return file response
        return self.get_file_response(path=path)

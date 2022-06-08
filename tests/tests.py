import shutil
import tempfile
from pathlib import Path

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, override_settings

# Setting up temporary media root
MEDIA_ROOT = Path(tempfile.mkdtemp())


# Create your tests here.

class TestCaseBase(APITestCase):

    @staticmethod
    def create_admin_user():
        user = User.objects.filter(
            username='admin'
        ).first()
        if user:
            user.set_password('admin')
            user.save()
        else:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@storage.com',
                password='admin'
            )
        return user

    def get_token(self):
        payload = {
            'username': 'admin',
            'password': 'admin'
        }
        response = self.client.post(
            path=reverse('token'),
            data=payload
        ).json()
        return response.get('access')

    def set_admin_credentials(self):
        token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def setUp(self) -> None:
        self.create_admin_user()
        self.set_admin_credentials()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class DocumentTestCase(TestCaseBase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    @staticmethod
    def _get_file_path(extension: str):
        media_dir = Path(__file__).resolve().parent / 'files'
        return media_dir / f'file_example.{extension}'

    def _create_document_with_file_example(self, extension: str):
        file_path = self._get_file_path(extension=extension)
        with file_path.open(mode='rb') as file:
            # creating payload
            payload = {
                'path': f'/documents/reviews/example.{extension}',
                'file': file
            }

            # consuming endpoint
            path = '%s%s' % (reverse('document-list'), 'upload/')
            return self.client.post(
                path=path,
                data=payload,
            ).json()

    def test_uploading_JPG_file(self):
        response = self._create_document_with_file_example(extension='jpg')

        # check if one id was generated
        self.assertGreater(response['id'], 0)

    def test_uploading_DOCX_file(self):
        response = self._create_document_with_file_example(extension='docx')

        # check if one id was generated
        self.assertGreater(response['id'], 0)

    def test_uploading_XLXS_file(self):
        response = self._create_document_with_file_example(extension='xlsx')

        # check if one id was generated
        self.assertGreater(response['id'], 0)

    def test_uploading_PDF_file(self):
        response = self._create_document_with_file_example(extension='pdf')

        # check if one id was generated
        self.assertGreater(response['id'], 0)

    def test_uploading_ZIP_file(self):
        response = self._create_document_with_file_example(extension='zip')

        # check if one id was generated
        self.assertGreater(response['id'], 0)

    def test_uploading_ZIP_file_and_revision(self):
        fst_response = self._create_document_with_file_example(extension='zip')

        # check if one id was generated
        self.assertGreater(fst_response['id'], 0)
        self.assertEquals(fst_response['revision'], 0)

        sec_response = self._create_document_with_file_example(extension='zip')

        # check if one id was generated and revision is 1
        self.assertGreater(sec_response['id'], 0)
        self.assertEquals(sec_response['revision'], 1)

    def test_uploading_ZIP_file_with_path_extension_is_equal_file_extension(self):
        file_path = self._get_file_path(extension='zip')
        with file_path.open(mode='rb') as file:
            # creating payload
            payload = {
                'path': f'/documents/reviews/example.zip',
                'file': file
            }

            # consuming endpoint
            path = '%s%s' % (reverse('document-list'), 'upload/')
            response = self.client.post(
                path=path,
                data=payload,
            ).json()

            # check if an error was caught
            errors = response.get('non_field_errors')
            self.assertIsNone(errors, 'Specified URL should have the same file extension')

    def test_downloading_ZIP_file(self):
        self._create_document_with_file_example(extension='zip')

        # consuming endpoint
        path = '%s%s' % (reverse('document-download'), '/documents/reviews/example.zip')
        response = self.client.get(path)

        self.assertEquals(
            response.get('Content-Disposition'),
            'inline; filename="example_0.zip"'
        )

    def test_downloading_ZIP_file_with_revision(self):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)

        self._create_document_with_file_example(extension='zip')
        self._create_document_with_file_example(extension='zip')

        # consuming endpoint
        path = '%s%s' % (reverse('document-download'), '/documents/reviews/example.zip')
        response = self.client.get(path)

        self.assertEquals(
            response.get('Content-Disposition'),
            'inline; filename="example_1.zip"'
        )

        # consuming endpoint
        path = '%s%s' % (reverse('document-download'), '/documents/reviews/example.zip?revision=0')
        response = self.client.get(path)

        self.assertEquals(
            response.get('Content-Disposition'),
            'inline; filename="example_0.zip"'
        )

from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import helpers, managers


def get_upload_path(instance, filename):
    return helpers.normalize_path(
        username=instance.user.username,
        path=instance.path,
        revision=instance.revision
    )


# Create your models here.
class Document(models.Model):
    id = models.BigAutoField(
        db_column='id',
        primary_key=True,
        verbose_name=_('Id')
    )
    path = models.CharField(
        db_column='tx_path',
        max_length=256,
        null=False,
        verbose_name=_('Path')
    )
    revision = models.IntegerField(
        db_column='nb_revision',
        null=False,
        default=0,
        verbose_name=_('Revision')
    )
    file = models.FileField(
        upload_to=get_upload_path,
        null=False,
        verbose_name=_('File')
    )
    file_name = models.CharField(
        db_column='tx_file_name',
        max_length=256,
        blank=True,
        null=True,
        verbose_name=_('File name')
    )
    uploaded_at = models.DateTimeField(
        db_column='dt_uploaded',
        auto_now_add=True,
        null=True,
        verbose_name=_('Uploaded at')
    )
    user = models.ForeignKey(
        auth_models.User,
        db_column='id_user',
        on_delete=models.CASCADE,
        null=True,
        related_name='documents',
        verbose_name=_('User')
    )

    objects = managers.DocumentQuerySet.as_manager()

    class Meta:
        db_table = 'document'
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')


class DocumentRevision(models.Model):
    id = models.BigAutoField(
        db_column='id',
        primary_key=True,
        verbose_name=_('Id')
    )
    document = models.ForeignKey(
        Document,
        db_column='id_document',
        on_delete=models.CASCADE,
        null=False,
        related_name='document_revisions',
        verbose_name=_('Document')
    )
    revision = models.IntegerField(
        db_column='nb_revision',
        null=False,
        verbose_name=_('Revision')
    )
    file = models.FileField(
        null=False,
        verbose_name=_('File')
    )
    file_name = models.CharField(
        db_column='tx_file_name',
        max_length=256,
        blank=True,
        null=True,
        verbose_name=_('File name')
    )
    uploaded_at = models.DateTimeField(
        db_column='dt_uploaded',
        auto_now_add=True,
        null=True,
        verbose_name=_('Uploaded at')
    )

    objects = managers.DocumentRevisionQuerySet.as_manager()

    class Meta:
        db_table = 'document_revision'
        verbose_name = _('Document revision')
        verbose_name_plural = _('Document revisions')

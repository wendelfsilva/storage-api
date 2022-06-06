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
    revision = models.IntegerField(
        db_column='nb_revision',
        blank=True,
        null=True,
        verbose_name=_('Revision')
    )
    current_revision = models.BooleanField(
        db_column='cs_current_revision',
        blank=True,
        null=True,
        default=False,
        verbose_name=_('Current revision')
    )
    user = models.ForeignKey(
        auth_models.User,
        db_column='id_user',
        on_delete=models.CASCADE,
        null=True,
        related_name='documents',
        verbose_name=_('User')
    )
    uploaded_at = models.DateTimeField(
        db_column='dt_uploaded',
        auto_now_add=True,
        null=True,
        verbose_name=_('Uploaded at')
    )

    objects = managers.DocumentQuerySet.as_manager()

    class Meta:
        db_table = 'document'
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.file_name:
            self.file_name = self.file.name

        # new instance
        if not self.id:
            # define function parameters
            kwargs = {'user_id': self.user.id, 'path': self.path}

            # get revision by path
            self.revision = Document.objects.get_next_revision(**kwargs)

            # check if the current revision was changed
            cleaned = Document.objects.clean_revisions(**kwargs)
            if cleaned or self.revision == 0:
                self.current_revision = True

        super().save(force_insert, force_update, using, update_fields)

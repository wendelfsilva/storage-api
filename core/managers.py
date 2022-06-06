from django.db.models import Max
from django.db.models import QuerySet
from django.db.models.functions import Coalesce


class DocumentQuerySet(QuerySet):
    def find_current_revision(self, user_id: int, path: str):
        filters = {
            'user_id': user_id,
            'path': path if path.startswith('/') else '/' + path,
            'current_revision': True
        }

        return self.filter(**filters).first()

    def get_next_revision(self, user_id: int, path: str) -> int:
        response = self.filter(
            user_id=user_id,
            path=path if path.startswith('/') else '/' + path
        ).aggregate(
            max_revision=Coalesce(Max('revision'), -1)
        )
        return response['max_revision'] + 1

    def clean_revisions(self, user_id: int, path: str) -> bool:
        filters = {
            'user_id': user_id,
            'path': path if path.startswith('/') else '/' + path
        }
        path_exists = self.filter(**filters).exists()
        if path_exists:
            self.filter(**filters).update(current_revision=False)
            return True

        return False

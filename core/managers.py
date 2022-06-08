from django.db.models import QuerySet


class DocumentQuerySet(QuerySet):
    def find_by_path(self, user_id: int, path: str):
        return self.filter(
            user_id=user_id,
            path=path
        ).first()


class DocumentRevisionQuerySet(QuerySet):
    def find_by_revision(self, document_id: int, revision: int):
        return self.filter(
            document_id=document_id,
            revision=revision
        ).first()

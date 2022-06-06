from os.path import splitext

from rest_framework import serializers


class PathAndFileExtensionValidator:
    def __init__(self, path_field='path', file_field='file'):
        self.path_field = path_field
        self.file_field = file_field

    def __call__(self, attrs):
        path_extension = splitext(attrs['path'])[1]
        file_extension = splitext(attrs['file'].name)[1]
        if not (path_extension == file_extension):
            raise serializers.ValidationError('Specified URL should have the same file extension')

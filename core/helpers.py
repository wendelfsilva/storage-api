from os import sep
from os.path import normpath, splitext

from pathlib import Path


def normalize_path(username: str, path: str, revision: int):
    path = normpath(path)
    if path.startswith(sep):
        path = path.replace(sep, '', 1)

    path, extension = splitext(path)
    file_name = '%s_%s%s' % (path, revision, extension)
    return Path(username) / file_name

import os
import uuid

from django.utils.text import slugify

from airport.models import Airplane


def airplane_image_file_path(instance: Airplane, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "movies", filename)

import enum
import uuid
from pathlib import Path

from django.utils.deconstruct import deconstructible
from slugify import slugify


class UploadMode(enum.StrEnum):
    SAFE = "safe"
    RANDOM = "random"


@deconstructible
class UploadToFactory:
    def __init__(self, mode: str | UploadMode):
        self.field_name = "files"

        normalized_mode = UploadMode(mode) if isinstance(mode, str) else mode

        strategies = {
            UploadMode.RANDOM: lambda path: f"{uuid.uuid4().hex[:12]}{path.suffix}",
            UploadMode.SAFE: lambda path: f"{slugify(path.stem) or 'file'}_{uuid.uuid4().hex[:12]}{path.suffix}",
        }

        self.filename_generator = strategies.get(normalized_mode, lambda path: path.name)

    def __set_name__(self, owner, name):
        self.field_name = name

    def __call__(self, instance, filename):
        meta = instance._meta
        path = Path(filename)
        final_filename = self.filename_generator(path)

        return str(Path(meta.app_label) / meta.model_name / self.field_name / final_filename)


upload_safe = UploadToFactory(mode=UploadMode.SAFE)
upload_random = UploadToFactory(mode=UploadMode.RANDOM)

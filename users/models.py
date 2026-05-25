from django.contrib.auth.models import AbstractUser
from django.db import models

from shared.models import BaseModel


class User(AbstractUser, BaseModel):
    can_import = models.BooleanField(default=False)
    can_export = models.BooleanField(default=False)

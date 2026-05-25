from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class BaseModel(TimeStampedModel):
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

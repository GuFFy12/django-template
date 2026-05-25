from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin


class BaseAdmin(SimpleHistoryAdmin, ImportExportMixin):
    readonly_fields = ("created", "modified")
    list_filter = ("created", "modified")

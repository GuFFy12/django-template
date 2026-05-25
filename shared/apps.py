from django.apps import AppConfig


class SharedConfig(AppConfig):
    name = "shared"
    verbose_name = "Shared"

    def ready(self):
        from django.contrib import admin, messages
        from django.contrib.admin import action
        from django_tasks_db.admin import DBTaskResultAdmin
        from django_tasks_db.models import DBTaskResult

        if not admin.site.is_registered(DBTaskResult):
            return

        admin.site.unregister(DBTaskResult)

        class CustomDBTaskResultAdmin(DBTaskResultAdmin):
            @action(description="Run selected tasks again")
            def run_selected_again(self, request, queryset):
                count = 0
                for tr in queryset:
                    args = tr.args_kwargs.get("args", [])
                    kwargs = tr.args_kwargs.get("kwargs", {})
                    tr.task.enqueue(*args, **kwargs)
                    count += 1

                msg = f"Re-enqueued {count} task result{'s' if count != 1 else ''}."
                self.message_user(request, msg, level=messages.SUCCESS)

            def has_change_permission(self, request, obj=None):
                return request.user.has_perm(f"{self.opts.app_label}.change_{self.opts.model_name}")

        existing_actions = getattr(CustomDBTaskResultAdmin, "actions", None) or []
        CustomDBTaskResultAdmin.actions = [*list(existing_actions), "run_selected_again"]

        admin.site.register(DBTaskResult, CustomDBTaskResultAdmin)

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        from django.contrib import admin

        if getattr(admin.site, "_users_app_merged", False):
            return
        admin.site._users_app_merged = True

        original_get_app_list = admin.site.get_app_list

        def custom_get_app_list(request, app_label=None):
            app_list = original_get_app_list(request, app_label)

            if app_label:
                return app_list

            apps = {app["app_label"]: app for app in app_list}

            if "auth" in apps and "users" in apps:
                apps["auth"]["models"].extend(apps["users"]["models"])
                apps["auth"]["models"].sort(key=lambda m: m["name"].lower())

                return [app for app in app_list if app["app_label"] != "users"]

            return app_list

        admin.site.get_app_list = custom_get_app_list

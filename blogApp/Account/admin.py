from django.contrib import admin
from .models import CustomUser, Profile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)


class CustomAdminSite(admin.AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_header = 'RepoApp Admin Panel'  # Optional customization

    def head(self):
        head = super().head()
        head += '<link rel="shortcut icon" href="{% static \'admin/img/favicon.ico\' %}" type="image/x-icon" />'
        head += '<link rel="apple-touch-icon" sizes="180x180" href="{% static \'admin/img/apple-touch-icon.png\' %}">'
        head += '<link rel="icon" type="image/png" sizes="32x32" href="{% static \'admin/img/favicon-32x32.png\' %}">'
        head += '<link rel="icon" type="image/png" sizes="16x16" href="{% static \'admin/img/favicon-16x16.png\' %}">'
        head += '<link rel="manifest" href="{% static \'admin/img/site.webmanifest\' %}">'
        return head

# Register your custom admin site (optional)
admin.site = CustomAdminSite()

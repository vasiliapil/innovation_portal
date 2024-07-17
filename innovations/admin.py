from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Innovation

admin.site.register(Innovation, SimpleHistoryAdmin)

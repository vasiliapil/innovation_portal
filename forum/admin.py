from django.contrib import admin
from .models import *


admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)
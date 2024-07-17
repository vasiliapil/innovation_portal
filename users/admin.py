from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import Network_member, User

admin.site.register(Network_member)




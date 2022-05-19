from django.contrib import admin

# Register your models here.
from .models import Reply, Translatelog

admin.site.register(Translatelog)
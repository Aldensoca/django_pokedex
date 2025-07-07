from django.contrib import admin
from .models import pokemon
from .models import type

# Register your models here.
admin.site.register(pokemon)
admin.site.register(type)
from django.contrib import admin
from .models import Chain, Block

# Register your models here.

admin.site.register(Chain)
admin.site.register(Block)
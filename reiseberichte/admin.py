from django.contrib import admin
from .models import Reise, Reiseleiter, Termin, Tag

admin.site.register(Reise)
admin.site.register(Reiseleiter)
admin.site.register(Termin)
admin.site.register(Tag)

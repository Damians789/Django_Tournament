from django.contrib import admin

from .models import *
# Register your models here.


class Choice(admin.TabularInline):
    model = Adres
    max_num = 1


class Adresxd(admin.ModelAdmin):
    fieldsets = [
        ('Adres1: ', {'fields': ['Miasto']}),
        ('ZIP', {'fields': ['ZIP']}),
        ('Wojewodztwo', {'fields': ['Woj']}),
    ]
    inlines = [Choice]
    # list_display = ('Ulica', 'NrDomu')
    list_filter = ['Miasto', 'ZIP']


admin.site.register(Acode,  Adresxd)
admin.site.register(Wojewodztwo)
admin.site.register(Adres)
admin.site.register(Osoba)
admin.site.register(Stadion)
admin.site.register(Vote)
admin.site.register(Dyscyplina)

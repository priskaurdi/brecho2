from django.contrib import admin
from quadros import models


# Register your models here.
class QuadrosImagemInline(admin.TabularInline):
    model = models.QuadrosImagem
    extra = 0

class QuadrosAdmin(admin.ModelAdmin):
    inlines = [
        QuadrosImagemInline,
    ]
    readonly_fields = ['slug']
    

admin.site.register(models.Quadros, QuadrosAdmin)

admin.site.register(models.QuadrosComentario)
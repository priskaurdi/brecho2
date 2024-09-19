from django.contrib import admin
from catalogo import models


# Register your models here.
class CatalogoImagemInline(admin.TabularInline):
    model = models.CatalogoImagem
    extra = 0

class CatalogoAdmin(admin.ModelAdmin):
    inlines = [
        CatalogoImagemInline,
    ]
    readonly_fields = ['slug']
    

admin.site.register(models.Catalogo, CatalogoAdmin)

admin.site.register(models.CatalogoComentario)
from django.contrib import admin
from .models import Bicicleta, Aluguel


@admin.register(Bicicleta)
class BicicletaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'modelo', 'cor', 'valor_hora', 'disponivel', 'dono')
    search_fields = ('nome', 'modelo')


@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):
    list_display = ('bicicleta', 'usuario', 'data_inicio', 'data_fim', 'ativo')
    list_filter = ('ativo',)

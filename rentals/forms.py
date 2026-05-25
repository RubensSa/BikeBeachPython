from django import forms
from .models import Bicicleta


class BicicletaForm(forms.ModelForm):
    class Meta:
        model = Bicicleta
        fields = ['nome', 'modelo', 'cor', 'valor_hora', 'imagem']

    def clean_valor_hora(self):
        v = self.cleaned_data.get('valor_hora')
        if v is None or v <= 0:
            raise forms.ValidationError('O valor por hora deve ser maior que zero.')
        return v

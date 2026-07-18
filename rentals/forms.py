from django import forms
from .models import Bicicleta


class BicicletaForm(forms.ModelForm):
    class Meta:
        model = Bicicleta
        fields = ['nome', 'modelo', 'cor', 'valor_hora', 'imagem']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            # file inputs get form-control for Bootstrap 5
            field.widget.attrs['class'] = (existing + ' form-control').strip()

    def clean_valor_hora(self):
        v = self.cleaned_data.get('valor_hora')
        if v is None or v <= 0:
            raise forms.ValidationError('O valor por hora deve ser maior que zero.')
        return v

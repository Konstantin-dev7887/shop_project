from django import forms
from .models import Product

# Константа со списком запрещённых слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация всех полей Bootstrap-подобными классами
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        for word in FORBIDDEN_WORDS:
            if word.lower() in name.lower():
                raise forms.ValidationError(f'Название не может содержать слово "{word}".')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        for word in FORBIDDEN_WORDS:
            if word.lower() in description.lower():
                raise forms.ValidationError(f'Описание не может содержать слово "{word}".')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

    # Дополнительное задание: валидация загружаемого изображения
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5 MB
                raise forms.ValidationError('Размер изображения не должен превышать 5 МБ.')
            if image.content_type not in ['image/jpeg', 'image/png']:
                raise forms.ValidationError('Допустимые форматы: JPEG, PNG.')
        return image

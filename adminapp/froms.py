from django import forms

from mainapp.models import Product


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

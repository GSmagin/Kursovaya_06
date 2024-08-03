from django import forms

from blog.models import BlogMod


class PostForm(forms.ModelForm):
    ALLOWED_CHARS = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя- ')

    class Meta:
        model = BlogMod
        fields = ['title', 'content', 'preview_image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'preview_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not all(char in self.ALLOWED_CHARS for char in title):
            raise forms.ValidationError('Должны быть только: русские символы, дефис или пробел')
        return title

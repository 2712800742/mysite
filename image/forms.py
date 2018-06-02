from  django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import Image

class ImageForms(forms.ModelForm):
    class Meta:
        model = Image
        fields=("title","url","description")

    def clean_url(self):
        url= self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg','png']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("提供的URL不符合图片扩展名。")
        return url

    def save(self, force_insert=False, farce_update = False,commit=True):
        image = super(ImageForms,self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = "{}.{}".format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        response = request.urlopen(image_url)
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()

        return image
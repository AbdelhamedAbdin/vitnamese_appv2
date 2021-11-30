from django.db import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html


class Student(models.Model):
    student = models.IntegerField(blank=False)
    grade = models.CharField(max_length=25)
    gender = models.CharField(max_length=25)

    def __str__(self):
        return str(self.student)

    def get_absolute_url(self):
        return self.pk


class Character(models.Model):
    character = models.CharField(max_length=25)
    regularity = models.CharField(max_length=25)
    complexity = models.CharField(max_length=25)

    def __str__(self):
        return self.character

    def get_absolute_url(self):
        return self.pk


class Response(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    correct = models.IntegerField(blank=False)
    error_class = models.CharField(max_length=60, blank=True, null=True)
    error_number = models.CharField(max_length=60, blank=True, null=True)
    error_unit = models.CharField(max_length=60, blank=True, null=True)
    error_type = models.CharField(max_length=60, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return str(self.correct)

    def get_absolute_url(self):
        return self.pk

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def admin_image(self):
        return format_html('<image style="height: 75px;width: 75px" src="{}" />', self.image_url())
    admin_image.short_description = 'Mirror Image'
    admin_image.allow_tags = True


class History(models.Model):
    user_ip = models.CharField(max_length=15, default='127.0.0.1')
    action = models.CharField(max_length=15, default='visit')
    visit_date = models.DateField(auto_now_add=True)
    country_ip = models.CharField(max_length=30, default='Unknown')
    city_ip = models.CharField(max_length=30, default='Unknown')

    def __str__(self):
        return self.action


class MultipleImages(models.Model):
    images = models.ImageField(blank=True)

    def __str__(self):
        return str(self.id)

    def image_url(self):
        if self.images and hasattr(self.images, 'url'):
            return self.images.url

    def admin_image(self):
        return format_html(''
        '<a href="{}">'
        '<image style="height: 75px;width: 75px" src="{}" />'
        '</a>'
        , self.image_url(), self.image_url())
    admin_image.short_description = 'Images'
    admin_image.allow_tags = True

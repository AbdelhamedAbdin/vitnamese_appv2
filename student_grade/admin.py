from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export import resources, widgets
from .models import Student, Character, Response, History, MultipleImages
# from django import forms


# class ExtraImage(forms.Form):
#     image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#
#     class Meta:
#         model = Response


class ImportStudentModel(ImportExportModelAdmin):
    list_display = ('id', 'student', 'grade', 'gender')


class ImportCharacterModel(ImportExportModelAdmin):
    list_display = ('id', 'character', 'regularity', 'complexity')


class ImportResponseModel(resources.ModelResource):
    student = Field(attribute='student', column_name='student', widget=widgets.ForeignKeyWidget(Student, 'student'))
    character = Field(attribute='character', column_name='character', widget=widgets.ForeignKeyWidget(Character, 'character'))
    correct = Field(attribute='correct', column_name='correct')
    id = Field(attribute='id', column_name='id')
    image = Field(attribute='image', column_name='image')

    class Meta:
        model = Response
        export_order = ('id', 'student', 'character', 'correct', 'error_class', 'error_number', 'error_unit', 'error_type', 'remark')
        report_skipped = True


class ResponseModelAdmin(ImportExportModelAdmin):
    resource_class = ImportResponseModel
    list_display = ('id', 'student', 'character', 'correct', 'error_class', 'error_type', 'error_number', 'error_unit', 'remark', 'admin_image')
    search_fields = ('student', 'error_class', 'error_type', 'error_number', 'error_unit')
    list_filter = ('character', 'correct')


class AdminHistory(admin.ModelAdmin):
    list_display = ('user_ip', 'action', 'country_ip', 'city_ip', 'visit_date')
    list_filter = ('visit_date', 'action')
    search_fields = ('user_ip', 'city_ip', 'country_ip')


class MultipleImageManaged(admin.ModelAdmin):
    list_display = ('id', 'admin_image')

    def get_form(self, request, obj=None, **kwargs):
        form = super(MultipleImageManaged, self).get_form(request, obj=None, **kwargs)
        form.base_fields['admin_image'].widget.attrs = {
            'multiple': 'multiple'
        }
        return form

    def save_model(self, request, obj, form, change):
        for data in request.FILES.getlist('admin_image'):
            MultipleImages.objects.create(images=data)


admin.site.register(Student, ImportStudentModel)
admin.site.register(Character, ImportCharacterModel)
admin.site.register(Response, ResponseModelAdmin)
admin.site.register(History, AdminHistory)
admin.site.register(MultipleImages, MultipleImageManaged)

from django.contrib import admin

# Register your models here.
from parsers.models import File
from parsers.utils import go


@admin.action(description='Обновить ассортимент в соответствии с файлом')
def make_published(modeladmin, request, queryset):
    # queryset.update(status='p')
    # print(queryset.values())
    # print(queryset.values_list('name', flat=True).get())

    filename = queryset.values_list('name', flat=True).get()
    go(filename)


class APILogsAdmin(admin.ModelAdmin):
    change_list_template = 'admin/model_change_list.html'
    actions = [make_published]




admin.site.register(File, APILogsAdmin)


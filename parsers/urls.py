from django.urls import path

from parsers.views import ImportFilesView, ImportImagesView, EmailSendView

urlpatterns = [
    path('import/files/', ImportFilesView.as_view(), name='import-files'),
    path('import/images/', ImportImagesView.as_view(), name='import-images'),
    path('email/send/', EmailSendView.as_view())
]

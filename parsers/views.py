from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from parsers.email import send_email
from parsers.utils import go, update_files, update_images


class FirstView(View):
    def get(self, request):
        go()
        return HttpResponse('Done')


class ImportFilesView(View):
    def post(self, request):
        update_files()
        return redirect('/admin/parsers/file/')


        # return HttpResponse('Import Done')


class ImportImagesView(View):
    def post(self, request):
        update_images()
        return redirect('/admin/parsers/file/')


class EmailSendView(View):
    def get(self, request):
        send_email()
        return redirect('/')

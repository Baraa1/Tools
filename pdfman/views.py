# Python
#import string
#import random
import re
import os
from math import floor
# Django
from pathlib import Path
from django.shortcuts import render
#from django.urls import reverse
#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from django.views.generic.edit import FormView
#from django.contrib.sessions.models import Session
#from django.db.models import signals
#from django.core.files import File
from django.contrib import messages
# 3rd Party
from PyPDF2 import PdfWriter
from magic import from_file
# Custom
from .forms import FileFieldForm


# initializing size of string
N = 10

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PDF_PATH = f'{Path(__file__).resolve().parent.parent}/media/pdf/'

def pdf_messages(request):
    return render(request, 'includes/messages.html')

class PdfManFormView(FormView):
    form_class = FileFieldForm
    template_name = "pdfman/includes/pdf_form.html"  
    success_url = "/PDF/pdf_messages/"

    def get(self, request, *args, **kwargs):
        form = FileFieldForm()
        # Get the path and create a list of the files in it
        folder_path = self.get_or_create_dir(request.session.session_key)
        files = Path(folder_path).glob('*')
        # Create a list of file dicts
        files_list = []
        for fl in files:
            files_list.append(self.get_file_data(f'{folder_path}/{fl.name}'))
        context = {
            "form":form,
            "file_path":folder_path,
            "files_list":False if len(files_list) <= 0 else files_list,
        }
        return render(request, 'pdfman/pdf.html',context)
    # HTMX, triggered each time the user clicks upload file and selects a file
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.upload_pdf(request, form)
        else:
            messages.warning(request, "File/s not Uploaded")
            return self.form_invalid(form)

    def upload_pdf(self, request, form):
        files       = form.cleaned_data["file_field"]
        folder_path = self.get_or_create_dir(request.session.session_key)
        # removes anything that isn't a letter, number or a dot to make file operations easier
        pattern = re.compile(r"[^\w\.]")
        for f in files:
            try:
                file_name = pattern.sub("", str(f))
                pdf_handler = PdfWriter()
                pdf_handler.append(f)
                file_path = f'{folder_path}/{file_name}'
                pdf_handler.write(file_path)
                pdf_handler.close()
                #messages.add_message(request, messages.SUCCESS, f'<b>{f}</b> Uploaded <a href="my-file-view/{file_path}/" target="_blank">View</a>')
                context = self.get_file_data(file_path)
                context['file_path'] = folder_path
                return render(request, "pdfman/includes/file.html", context)
            except:            
                messages.add_message(request, messages.WARNING, f'<b>"{f}"</b> was not Uploaded - it is not a <b>PDF</b> file', extra_tags="rgb(220 38 38)")
                return render(request, "pdfman/includes/file.html")

    
    def get_or_create_dir(self, k):
        if Path(f'{PDF_PATH}{k}').exists():
            return f'{PDF_PATH}{k}'
        else:
            # Get or Create Directory
            Path(f'{PDF_PATH}{k}').mkdir(parents=True, exist_ok=True)
            # echo "<command>" | at now + <interval>
            os.system(f'echo rm -rf {PDF_PATH}{k} | at now + 1 hour')
            return f'{PDF_PATH}{k}'

    def get_file_data(self, file_path):
        pdf_file = Path(file_path)
        file_size = pdf_file.stat().st_size
        if file_size > 1024:
            if file_size > 1048576:
                file_size = f'{floor(file_size / 1048576)}mb'
            else:
                file_size = f'{floor(file_size / 1024)}kb'
        else:
            file_size = f'{file_size}b'

        context = {
            "file_name":str(pdf_file.name),
            "file_size":file_size,
            "file_type":from_file(file_path, mime=True)
        }
        return context
    
def delete_file(request):
    file_path = request.GET.get('file_path')
    file_name = request.GET.get('file_name')
    try:
        os.remove(f'{file_path}/{file_name}')
        messages.add_message(request, messages.SUCCESS, f'<b>"{file_name}"</b> was Deleted from server', extra_tags="rgb(34 197 94)")
        return render(request, "pdfman/includes/file.html")
    except:
        messages.add_message(request, messages.WARNING, f'<b>"{file_name}"</b> was NOT deleted from server', extra_tags="rgb(220 38 38)")
        context = PdfManFormView.get_file_data(f'{file_path}/{file_name}')
        return render(request, "pdfman/includes/file.html", context)

#    def merge_pdf(request, files):
#        merger = PdfWriter()
#        # using random.choices()
#        # generating random strings
#        res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
#        # merges the files in the order they were added to the html form by the end user
#        for f in files:
#            merger.append(f)
#        # Creates a merged file with a randomly generated string to prevent overwriting
#        merged_pdf = f'{PDF_PATH}{res}-merged-pdf.pdf'
#        merger.write(merged_pdf)
#        request.session['pdf_link'] = merged_pdf
#        request.session['filename'] = f'{res}-merged-pdf.pdf'
#        merger.close()
#        
#        return super().form_valid(files)
#
#
#class ViewPdfFile(TemplateView):
#    template_name = 'pdfman/view_pdf.html'
#    def get(self, request, *args, **kwargs):
#        pdf_link = request.session.get('pdf_link')
#        filename = request.session.get('filename')
#        return render(request, self.template_name, {"pdf_link": pdf_link,"filename":filename})
#
#class MyFileView(View):
#    def get(self, request, file_name):
#        #file_path = request.session.get('pdf_link')
#        response = HttpResponse(open(file_name, 'rb').read())
#        response['Content-Type'] = 'application/pdf'
#        return response
##def my_file_view(request):
#    pdf_link = request.session.get('pdf_link')
#    file_object = open(pdf_link, 'rb')
#    filename = request.session.get('filename')
#
#    return HttpResponse.send_file(file_object, filename=filename)

#def download_file(request):
#    # fill these variables with real values
#    fl_path = request.session.get('pdf_link')
#    filename = 'merged-pdf.pdf'
#
#    fl = open(fl_path, 'r')
#    django_file = File(some_file)
#    
#    mime_type, _ = mimetypes.guess_type(fl_path)
#    response = HttpResponse(fl, content_type=mime_type)
#    response['Content-Disposition'] = "attachment; filename=%s" % filename
#    return response
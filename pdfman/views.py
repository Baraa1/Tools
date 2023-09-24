# Python
import string
import random
import re
import os
from math import floor
import json
# Django
from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib import messages
#from django.views.generic import TemplateView
#from django.views import View
#from django.urls import reverse
#from django.contrib.sessions.models import Session
#from django.db.models import signals
#from django.core.files import File
# 3rd Party
from PyPDF2 import PdfWriter
from magic import from_file
# Custom
from .forms import FileFieldForm


# initializing size of string
N = 10

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PDF_PATH = f'{Path(__file__).resolve().parent.parent}/media/pdf/'


# Get or Create Directory
def get_or_create_dir(k):
    if Path(f'{PDF_PATH}{k}').exists():
        return f'{PDF_PATH}{k}'
    
    Path(f'{PDF_PATH}{k}').mkdir(parents=True, exist_ok=True)
    # Syntax: echo "<command>" | at now + <interval>
    os.system(f'echo rm -rf {PDF_PATH}{k} | at now + 1 hour')
    return f'{PDF_PATH}{k}'

def get_file_data(file_path):
    # Path has useful functions
    pdf_file  = Path(file_path)
    file_size = pdf_file.stat().st_size
    # convert the size into an easy to read number
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

# create a session if not created
def make_session(request):
    if not request.session.session_key:
        request.session.create()
    return

def upload_pdf(fh, file_path):
    pdf_handler = PdfWriter()
    pdf_handler.append(fh)
    pdf_handler.write(file_path)
    pdf_handler.close()

def merge_pdf(folder_path, ordered_list):
    merger             = PdfWriter()
    # generating random strings using random.choices()
    randomized_name    = ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))

    # merges the files in the order chosen by the user
    for file_obj in ordered_list:
        pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
        merger.append(pdf_file)

    # Where to save the file and what to name it
    merged_pdf = f'{folder_path}/{randomized_name}.pdf'
    merger.write(merged_pdf)
    merger.close()
    
    return merged_pdf

def pdf_messages(request):
    message = messages.get_messages(request)
    if message:
        return render(request, 'includes/messages.html')
    # Temporary duct tape solution
    else:
        return HttpResponse(status=204)#None#HttpResponse('')

class PdfManFormView(FormView):
    form_class    = FileFieldForm
    template_name = "pdfman/includes/pdf_form.html"  
    success_url   = "/PDF/pdf_messages/"

    def get(self, request, *args, **kwargs):
        make_session(request)
        form = FileFieldForm()
        folder_path = get_or_create_dir(request.session.session_key)
        # create a list of the files in this path
        files = Path(folder_path).glob('*')
        files_list = []
        # Create a list of file dicts
        for fl in files:
            files_list.append(get_file_data(f'{folder_path}/{fl.name}'))

        context = {
            "form":form,
            "file_path":folder_path,
            "files_list":False if len(files_list) <= 0 else files_list,
        }
        return render(request, 'pdfman/pdf.html',context)

    # HTMX, triggered each time the user clicks upload file and selects a file or uses drag and drop
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form       = self.get_form(form_class)

        if form.is_valid():
            return self.upload_file(request, form)
        else:
            messages.warning(request, "File/s were not Uploaded")
            return self.form_invalid(form)

    def upload_file(self, request, form):
        files       = form.cleaned_data["file_field"]
        folder_path = get_or_create_dir(request.session.session_key)
        # using re.compile with sub
        # removes anything that isn't a letter, number or a dot to make file operations easier
        # Some characters cause errors in later processes
        pattern = re.compile(r"[^\w\.]")
        for f in files:
            file_name = pattern.sub("", str(f))
            file_path = f'{folder_path}/{file_name}'
            
            if Path(f'{folder_path}/{file_name}').is_file():
                messages.add_message(request, messages.INFO, f'<b>"{f}"</b> is already uploaded', extra_tags="#38bdf8")
                return HttpResponse(status=204)
            
            try:
                # Saves the file on the server
                upload_pdf(f, file_path)
                messages.add_message(request, messages.SUCCESS, f'<b>{f}</b> Successfully Uploaded', extra_tags="#38bdf8")
                context              = get_file_data(file_path)
                context['file_path'] = folder_path
                return render(request, "pdfman/includes/file.html", context)
            
            except:            
                messages.add_message(request, messages.WARNING, f'<b>"{f}"</b> was not Uploaded - it is not a <b>PDF</b> file', extra_tags="rgb(220 38 38)")
                return HttpResponse(status=204)
    
def delete_file(request):
    file_path = request.GET.get('file_path')
    file_name = request.GET.get('file_name')

    try:
        os.remove(f'{file_path}/{file_name}')
        messages.add_message(request, messages.SUCCESS, f'<b>"{file_name}"</b> was Deleted from server', extra_tags="rgb(34 197 94)")
        return HttpResponse('')
    except:
        messages.add_message(request, messages.WARNING, f'<b>"{file_name}"</b> was NOT deleted from server', extra_tags="rgb(220 38 38)")
        context = get_file_data(f'{file_path}/{file_name}')
        return render(request, "pdfman/includes/file.html", context)

def merger(request):
    if request.method == 'POST':
        folder_path  = get_or_create_dir(request.session.session_key)
        ordered_list = json.loads(request.POST.get('item_order'))

        try:
            merged_pdf = merge_pdf(folder_path, ordered_list)
            context                    = get_file_data(merged_pdf)
            context['file_path']       = folder_path
            messages.add_message(request, messages.SUCCESS, f'Merged Successfully to <a href="/PDF/view_file/?file_path={merged_pdf}" target="_blank"><b>"{randomized_name}"</b></a>', extra_tags="rgb(34 197 94)")
            return render(request, "pdfman/includes/merged-file.html", context)
        
        except json.JSONDecodeError:
            messages.add_message(request, messages.WARNING, 'Merge Failed', extra_tags="rgb(220 38 38)")
            return HttpResponse('')

def view_file(request):
    file_path                = request.GET.get('file_path')
    response                 = HttpResponse(open(file_path, 'rb').read())
    response['Content-Type'] = 'application/pdf'
    return response

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
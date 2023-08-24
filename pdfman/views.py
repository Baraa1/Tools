# Python
#import string
#import random
#import mimetypes
# Django
from pathlib import Path
from django.shortcuts import render
#from django.urls import reverse
#from django.http import HttpResponse
#from django.views import View
#from django.views.generic import TemplateView
from django.views.generic.edit import FormView
#from django.core.files import File
from django.contrib import messages
# 3rd Party
from PyPDF2 import PdfWriter, PdfReader
#import magic
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
        context = {
            "form":form,
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
        # Get or Create Directory
        Path(f'{PDF_PATH}{request.session.session_key}').mkdir(parents=True, exist_ok=True)
        for f in files:
            try:
                pdf_handler = PdfWriter()
                pdf_handler.append(f)
                file_path = f'{PDF_PATH}{request.session.session_key}/{f}'
                pdf_handler.write(file_path)
                messages.add_message(request, messages.SUCCESS, f'<b>{f}</b> Uploaded <a href="my-file-view/{file_path}/" target="_blank">View</a>')
            except:
                messages.add_message(request, messages.WARNING, f"<b>{f}</b> not Uploaded - not a PDF file")

        return super().form_valid(form)

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
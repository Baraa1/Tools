from django.urls import path
from .views import *

urlpatterns = [
    #path('', pdfman, name='pdfman'),
    path('', PdfManFormView.as_view(), name='upload'),
    path('pdf_messages/', pdf_messages, name='pdf_messages'),
    path('delete_file/', delete_file, name='delete_file'),
    path('merger/', merger, name='merger'),
    path('splitter/', splitter, name='splitter'),
    path('pdf_compressor/', pdf_compressor, name='pdf_compressor'),
    path('convert_to_docx/', convert_to_docx, name='convert_to_docx'),
    path('convert_to_pdf/', convert_to_pdf, name='convert_to_pdf'),
    path('view_file/', view_file, name='view_file'),
    #path('viewpdf/', ViewPdfFile.as_view(), name='viewpdf'),
    #path('my-file-view/<path:file_name>/', MyFileView.as_view(), name='my_file_view'),
]
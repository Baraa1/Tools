# Python
from string import ascii_lowercase, digits
from random import choices
from math import floor
from pathlib import Path
from os import path as os_path, system as system_command
from mimetypes import guess_type
from subprocess import run as run_command, CalledProcessError
from PIL import Image
# Django
# 3rd Party
import fitz # PyMuPDF
from PyPDF2 import PdfWriter, PdfReader
from magic import from_file
from pdf2docx import Converter
from pdf2image import convert_from_path
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
    system_command(f'echo rm -rf {PDF_PATH}{k} | at now + 1 hour')
    return f'{PDF_PATH}{k}'

def get_file_data(file_path):
    # Path has useful functions
    pdf_file   = Path(file_path)
    if from_file(file_path, mime=True) == 'application/pdf':
        pdf_reader = len(PdfReader(file_path).pages)
    else:
        pdf_reader = '-'
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
        "file_name": str(pdf_file.name),
        "file_size": file_size,
        "file_type": from_file(file_path, mime=True),
        "file_pages": pdf_reader
    }
    return context

# Create a list of file dicts
def list_files(folder_path):
    # create a list of the files in this path
    files = Path(folder_path).glob('*')
    files_list = []
    for fl in files:
        files_list.append(get_file_data(f'{folder_path}/{fl.name}'))
    
    return files_list

# create a session if not created
def make_session(request):
    if not request.session.session_key:
        request.session.create()
    return

# returns True if file ext is invalid 
def validate_file_extension(uploaded_file, file_ext=None):
    # Get the file extension from the uploaded file's name
    ext = os_path.splitext(uploaded_file)[1]
    # Get the MIME type of the file using the mimetypes library
    mime_type, _ = guess_type(uploaded_file)
    
    # Define allowed MIME types (adjust this list as needed)
    allowed_mime_types = ['image/jpeg', 'image/png', 'application/pdf', '.doc', '.docx', 'application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    allowed_mime_dict = {
        'pdf': ['application/pdf', 'pdf'],
        'image': ['image/jpeg', 'jpeg', 'image/jpg', 'jpg', 'image/png', 'png'],
        'word': ['doc', 'docx', 'application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    }

    # Check if the MIME type is in the allowed list
    if file_ext == None:
        if mime_type not in allowed_mime_types:
            return True#f"Unsupported file type: {mime_type}. Allowed types are {', '.join(allowed_mime_types)}."
    elif mime_type not in allowed_mime_dict[file_ext]:
        print(file_ext, allowed_mime_dict[file_ext])
        return True
    return False

def upload_file(fh, file_path):
    destination = open(f'{file_path}', 'wb')
    for chunk in fh.chunks():
        destination.write(chunk)
    destination.close()

def merge_pdf(folder_path, ordered_list):
    merger             = PdfWriter()
    # generating random strings using random.choices()
    randomized_name    = ''.join(choices(ascii_lowercase + digits, k=N))

    # merges the files in the order chosen by the user
    for file_obj in ordered_list:
        if file_obj["startPage"] != "False":
            start_page = int(file_obj["startPage"])-1
            if file_obj["endPage"] != "False":
                end_page = int(file_obj["endPage"])
                pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
                merger.append(pdf_file,pages=(start_page, end_page))
            else:
                pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
                merger.append(pdf_file,pages=(start_page, start_page+1))
        else:
            pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
            merger.append(pdf_file)

    # Where to save the file and what to name it
    merged_pdf = f'{folder_path}/{randomized_name}.pdf'
    merger.write(merged_pdf)
    merger.close()
    
    return merged_pdf

def split_pdf(folder_path, ordered_list):
    split_message = ''
    # split the files in the order chosen by the user
    for file_obj in ordered_list:
        if validate_file_extension(file_obj["name"], file_ext='pdf'):
            continue
        splitter = PdfWriter()
        if file_obj["startPage"] != "False":
            start_page = int(file_obj["startPage"])-1
            if file_obj["endPage"] != "False":
                end_page = int(file_obj["endPage"])
                pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
                splitter.append(pdf_file,pages=(start_page, end_page))
                # Where to save the file and what to name it
                splitted_pdf = f'{folder_path}/({start_page}-{end_page}){file_obj["name"]}'
            else:
                pdf_file = open(f'{folder_path}/{file_obj["name"]}', 'rb')
                splitter.append(pdf_file,pages=(start_page, start_page+1))
                splitted_pdf = f'{folder_path}/({start_page}){file_obj["name"]}'
        else:
            continue

        split_message += f'<br><b>{file_obj["name"]}</b> split successful<br>'
        splitter.write(splitted_pdf)
        splitter.close()
    
    return split_message

def compress_pdf(folder_path, ordered_list):
    compress_message = ''
    # compress the files in the order chosen by the user
    for file_obj in ordered_list:
        if validate_file_extension(file_obj["name"], file_ext='pdf'):
            continue

        input_pdf_path = f'{folder_path}/{file_obj["name"]}'
        output_pdf_path = f'{folder_path}/compressed-{file_obj["name"]}'

        pdf_document = fitz.open(input_pdf_path)
        pdf_document.save(output_pdf_path, garbage=4, deflate=True, clean=True)
        pdf_document.close()
        compress_message += f'<br><b>{file_obj["name"]}</b> Compress Successful<br>'
    
    return compress_message

def pdf_to_docx(folder_path, ordered_list):
    docx_message = ''
    for file_obj in ordered_list:
        if validate_file_extension(file_obj["name"], file_ext='pdf'):
            continue
        pdf_file = f'{folder_path}/{file_obj["name"]}'
        docx_file = f'{folder_path}/{os_path.splitext(file_obj["name"])[0]}.docx'

        # convert pdf to docx
        cv = Converter(pdf_file)
        cv.convert(docx_file)      # all pages by default
        cv.close()
        docx_message += f'<br><b>{os_path.splitext(file_obj["name"])[0]}.docx</b> Converted Successfully<br>'
        #parse(pdf_file, docx_file)
    return docx_message

def docx_to_pdf(folder_path, ordered_list):
    docx_message = ''
    for file_obj in ordered_list:
        if validate_file_extension(file_obj["name"], file_ext='word'):
            continue

        docx_file = f'{folder_path}/{file_obj["name"]}'
        pdf_file = f'{os_path.splitext(file_obj["name"])[0]}.pdf'

        try:
        # Define the unoconv command
            unoconv_command = f"unoconv -f pdf {docx_file}"
        # Run the unoconv command
            run_command(unoconv_command, shell=True, check=True)
            docx_message += f'<br>Converted: <b>{file_obj["name"]}</b> to <b>{pdf_file}</b> Successfully<br>'
        except CalledProcessError as e:
            docx_message += f'<br>Error Converting: <b>{file_obj["name"]}</b> to <b>{pdf_file}</b><br>{e}<br>'
        except FileNotFoundError:
            docx_message += f'<br>System Error at <b>{file_obj["name"]}.pdf</b> Contact admin<br>'

    return docx_message

def pdf_to_png(folder_path, ordered_list):
    png_message = ''
    for file_obj in ordered_list:
        if validate_file_extension(file_obj["name"], file_ext='pdf'):
            continue

        pdf_file = f'{folder_path}/{file_obj["name"]}'
        png_file = f'{folder_path}/{os_path.splitext(file_obj["name"])[0]}.png'

        try:
            pages = convert_from_path(pdf_file)
            for page in pages:
                page.save(png_file, 'PNG')
            png_message += f'<p>Done converting <b>{file_obj["name"]}</b> to <b>{os_path.splitext(file_obj["name"])[0]}.png</b></p><br>'
        except:
            png_message += f'Error converting <b>{file_obj["name"]}</b> to <b>{os_path.splitext(file_obj["name"])[0]}.png</b><br>'

    return png_message

def png_to_pdf(folder_path, ordered_list):
    png_message = ''
    for file_obj in ordered_list:
        if validate_file_extension(file_obj["name"], file_ext='image'):
            continue

        png_file = Image.open(f'{folder_path}/{file_obj["name"]}')
        pdf_file = f'{folder_path}/{os_path.splitext(file_obj["name"])[0]}.pdf'

        im = png_file.convert('RGB')
        
        try:
            im.save(pdf_file, save_all=True)
            png_message += f'<p>Done converting <b>{file_obj["name"]}</b> to <b>{os_path.splitext(file_obj["name"])[0]}.pdf</b></p><br>'
        except:
            png_message += f'Error converting <b>{file_obj["name"]}</b> to <b>{os_path.splitext(file_obj["name"])[0]}.pdf</b><br>'

    return png_message
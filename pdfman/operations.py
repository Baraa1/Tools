# Python
from string import ascii_lowercase, digits
from random import choices
from math import floor
from pathlib import Path
from os import path as os_path
from mimetypes import guess_type
from subprocess import run as run_command, CalledProcessError
# Django
# 3rd Party
from fitz import open # PyMuPDF
from PyPDF2 import PdfWriter, PdfReader
from magic import from_file
from pdf2docx import Converter
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
    run_command(f'echo rm -rf {PDF_PATH}{k} | at now + 1 hour')
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

def validate_file_extension(uploaded_file):
    # Get the file extension from the uploaded file's name
    ext = os_path.splitext(uploaded_file.name)[1]
    # Get the MIME type of the file using the mimetypes library
    mime_type, _ = guess_type(uploaded_file.name)
    
    # Define allowed MIME types (adjust this list as needed)
    allowed_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', '.doc', '.docx', 'application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document']

    # Check if the MIME type is in the allowed list
    if mime_type not in allowed_mime_types:
        return True#f"Unsupported file type: {mime_type}. Allowed types are {', '.join(allowed_mime_types)}."
    return False

def validate_pdf_extension(uploaded_file):
    # Get the file extension from the uploaded file's name
    ext = os_path.splitext(uploaded_file)[1]
    # Get the MIME type of the file using the mimetypes library
    mime_type, _ = guess_type(uploaded_file)
    
    # Define allowed MIME types (adjust this list as needed)
    allowed_mime_types = ['.pdf', 'application/pdf']

    # Check if the MIME type is in the allowed list
    if mime_type not in allowed_mime_types:
        return True#f"Unsupported file type: {mime_type}. Allowed types are {', '.join(allowed_mime_types)}."
    return False

def validate_word_extension(uploaded_file):
    ext = os_path.splitext(uploaded_file)[1]
    # Get the MIME type of the file using the mimetypes library
    mime_type, _ = guess_type(uploaded_file)
    
    # Define allowed MIME types (adjust this list as needed)
    allowed_mime_types = ['.doc', '.docx', 'application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document']

    # Check if the MIME type is in the allowed list
    if mime_type not in allowed_mime_types:
        return True#f"Unsupported file type: {mime_type}. Allowed types are {', '.join(allowed_mime_types)}."
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
    split_list = []
    # split the files in the order chosen by the user
    for file_obj in ordered_list:
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

        split_list.append(splitted_pdf)
        splitter.write(splitted_pdf)
        splitter.close()
    
    return split_list

def compress_pdf(folder_path, ordered_list):
    compress_list = []
    # compress the files in the order chosen by the user
    for file_obj in ordered_list:
        input_pdf_path = f'{folder_path}/{file_obj["name"]}'
        output_pdf_path = f'{folder_path}/compressed-{file_obj["name"]}'

        pdf_document = open(input_pdf_path)
        pdf_document.save(output_pdf_path, garbage=4, deflate=True, clean=True)
        pdf_document.close()
        compress_list.append(f'{folder_path}/compressed-{file_obj["name"]}')
    
    return compress_list

def pdf_to_docx(folder_path, ordered_list):
    compress_list = []
    for file_obj in ordered_list:
        if validate_pdf_extension(file_obj["name"]):
            continue
        pdf_file = f'{folder_path}/{file_obj["name"]}'
        docx_file = f'{folder_path}/{file_obj["name"]}.docx'

        # convert pdf to docx
        cv = Converter(pdf_file)
        cv.convert(docx_file)      # all pages by default
        cv.close()
        #parse(pdf_file, docx_file)
    return compress_list

def docx_to_pdf(folder_path, ordered_list):
    compress_list = []
    for file_obj in ordered_list:
        if validate_word_extension(file_obj["name"]):
            continue

        docx_file = f'{folder_path}/{file_obj["name"]}'
        pdf_file = f'{folder_path}/{file_obj["name"]}.pdf'

        try:
        # Define the unoconv command
            unoconv_command = f"unoconv -f pdf {docx_file}"
        
        # Run the AbiWord command
            run_command(unoconv_command, shell=True, check=True)
            print(f"Conversion successful: {docx_file} to {pdf_file}")
        except CalledProcessError as e:
            print(f"Error converting {docx_file} to {pdf_file}: {e}")
        except FileNotFoundError:
            print("unoconv command not found. Please make sure unoconv is installed and in your PATH.")


    return compress_list
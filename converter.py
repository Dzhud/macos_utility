'''
import aspose.words as aw

doc = aw.Document("test_file.docx")
doc.save("Output.pdf")

#Next thing is to remove Aspose Watermark programmtically. 
'''
from docx2pdf import convert
import os
# One File Converter
'''
def convert_word_to_pdf(word_file, pdf_file):
    try:
        convert(word_file, pdf_file)
        print(f"\n\n\nConverted {word_file} to {pdf_file} successfully.\n\n\n")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
word_file_path = "test_file.docx"
pdf_file_path = "docx2pdf.pdf"
convert_word_to_pdf(word_file_path, pdf_file_path)
'''
# Multiple File Converter
def bulk_convert_to_pdf(folder_path):
    try:
        convert(folder_path)
        print(f"Converted DOCX files in {folder_path} to PDF successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
folder_path = "/path/to/your/docx/folder"
bulk_convert_to_pdf(folder_path)
'''
def bulk_convert_to_pdf():
    try:
        current_directory = os.getcwd()
        convert(current_directory)
        print(f"\n\nConverted DOCX files in {current_directory} to PDF successfully.\n\n")
    except Exception as e:
        print(f"Error: {e}")

bulk_convert_to_pdf()
'''
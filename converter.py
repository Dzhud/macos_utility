'''
import aspose.words as aw

doc = aw.Document("test_file.docx")
doc.save("Output.pdf")

#Next thing is to remove Aspose Watermark programmtically. 
'''
from docx2pdf import convert

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


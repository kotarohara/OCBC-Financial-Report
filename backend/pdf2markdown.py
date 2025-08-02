import PyPDF2
from markitdown import MarkItDown

# Use the existing unprotected PDF file
pdf_filename = 'Wealth Report-5728-Jun-25.pdf'
markdown_filename = pdf_filename.replace('.pdf', '.md')

with open(pdf_filename, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    reader.decrypt('your_password')
    
    writer = PyPDF2.PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    
    # Save unprotected version
    with open('unprotected.pdf', 'wb') as output:
        writer.write(output)

# Use MarkItDown to convert the unprotected PDF
md = MarkItDown()
result = md.convert("unprotected.pdf")

with open(markdown_filename, 'w') as md_file:
    md_file.write(result.text_content)

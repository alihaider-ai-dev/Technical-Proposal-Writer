import markdown
from docx import Document
from docx.shared import Pt
from bs4 import BeautifulSoup
from html2docx import html2docx


def convert(markdown_text, output_file):
    # Convert Markdown to HTML
    html = markdown.markdown(markdown_text, extensions=['extra'])

    # Save the HTML to a file
    with open(output_file, "w") as file:
        file.write(html)


def html_to_word(html_content, output_file, title):
    # Convert HTML content to a BytesIO object containing the Word document
    doc = html2docx(html_content, title)
    # Write the BytesIO object to a file
    with open(output_file, 'wb') as file:
        file.write(doc.getvalue())  # Write the bytes from BytesIO object

from pypdf import PdfReader

def extract_text_from_pdf(file):

    reader = PdfReader(file)

    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages.append({
                "page": i + 1,
                "text": text
            })

    return pages
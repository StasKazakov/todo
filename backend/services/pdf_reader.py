from pypdf import PdfReader
import re

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    full_text = ""
    page_map = []  

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            page_map.append((len(full_text), i + 1))
            full_text += text + "\n"

    section_pattern = re.compile(r'(\n|^)(\d+\.\s+[A-Z][^\n]+)')
    
    sections = []
    last_end = 0
    current_section = "General"


    for match in section_pattern.finditer(full_text):
        if last_end < match.start():
            sections.append({
                "text": full_text[last_end:match.start()].strip(),
                "section": current_section,
                "char_pos": last_end
            })
        current_section = match.group(2).strip()
        last_end = match.end()
        

    sections.append({
        "text": full_text[last_end:].strip(),
        "section": current_section,
        "char_pos": last_end
    })

    def get_page(char_pos):
        page = 1
        for start, num in page_map:
            if char_pos >= start:
                page = num
        return page

    return [
        {**s, "page": get_page(s["char_pos"])}
        for s in sections if s["text"]
    ]
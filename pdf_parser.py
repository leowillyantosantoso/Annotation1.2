# pdf_parser.py

import fitz  # PyMuPDF
import re


def extract_text_from_pdf(pdf_path):
    """Extracts raw text from a PDF file."""
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text()

    return full_text


def split_into_sentences(text):
    """Split text into simple sentences using regex."""
    # You can later improve this using spaCy or nltk if needed
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    return sentence_endings.split(text.strip())


def filter_sentences(sentences, keywords):
    """Return only the sentences containing any of the given keywords as whole words."""
    keywords_lower = [kw.lower() for kw in keywords]
    filtered = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        for kw in keywords_lower:
            # Match whole word using regex
            if re.search(r'\b' + re.escape(kw) + r'\b', sentence_lower):
                filtered.append(sentence)
                break
    return filtered


def extract_relevant_sentences(pdf_path, keywords=None):
    """High-level function to extract and filter PDF text by keywords."""
    raw_text = extract_text_from_pdf(pdf_path)
    sentences = split_into_sentences(raw_text)

    if keywords:
        sentences = filter_sentences(sentences, keywords)

    return sentences


# Optional CLI test
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_parser.py path_to_paper.pdf [keyword1 keyword2 ...]")
    else:
        pdf_path = sys.argv[1]
        keywords = sys.argv[2:] if len(sys.argv) > 2 else ["sodium", "membrane", "current"]
        sentences = extract_relevant_sentences(pdf_path, keywords)

        print(f"\n[Extracted Sentences Matching Keywords: {keywords}]")
        for s in sentences:
            print(f"- {s.strip()}")

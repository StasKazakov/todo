import pytest
from io import BytesIO
import asyncio
from services.pdf_reader import extract_text_from_pdf
from services.chunker import split_text
from services.embeddings import create_embeddings

# Test for split_text
def test_split_text():
    text = "Some text for testing. " * 100
    chunks = split_text(text, chunk_size=50, overlap=10)
    assert len(chunks) > 0
    for c in chunks:
        assert isinstance(c, str)

def test_split_text_respects_chunk_size():
    text = "Some text for testing. " * 100
    chunks = split_text(text, chunk_size=50, overlap=10)
    for c in chunks[:-1]:  
        assert len(c) <= 50

def test_split_text_empty_string():
    chunks = split_text("", chunk_size=50, overlap=10)
    assert chunks == []

def test_split_text_short_text():
    text = "Short text"
    chunks = split_text(text, chunk_size=500, overlap=10)
    assert len(chunks) == 1
    assert chunks[0] == text

# Test for extract_text_from_pdf
def test_extract_returns_list():
    with open("tests/example.pdf", "rb") as f:
        result = extract_text_from_pdf(BytesIO(f.read()))
    assert isinstance(result, list)


def test_extract_has_required_keys():
    with open("tests/example.pdf", "rb") as f:
        result = extract_text_from_pdf(BytesIO(f.read()))
    assert len(result) > 0
    assert "text" in result[0]
    assert "page" in result[0]
    assert "section" in result[0]


def test_extract_detects_section():
    with open("tests/example.pdf", "rb") as f:
        result = extract_text_from_pdf(BytesIO(f.read()))
    sections = [r["section"] for r in result]
    assert any(s != "General" for s in sections)

# Test for create_embeddings
def test_create_embeddings_returns_list():
    chunks = ["Hello world", "Test text"]
    result = asyncio.run(create_embeddings(chunks))
    assert isinstance(result, list)


def test_create_embeddings_correct_count():
    chunks = ["Hello world", "Test text", "Third chunk"]
    result = asyncio.run(create_embeddings(chunks))
    assert len(result) == len(chunks)


def test_create_embeddings_vectors_are_lists():
    chunks = ["Hello world"]
    result = asyncio.run(create_embeddings(chunks))
    assert isinstance(result[0], list)


def test_create_embeddings_empty():
    result = asyncio.run(create_embeddings([]))
    assert result == []


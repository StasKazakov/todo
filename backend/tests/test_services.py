import pytest

from services.chunker import split_text

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


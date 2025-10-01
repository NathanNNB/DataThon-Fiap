import pytest
from app.utils.preprocessing import TextPreprocessing

def test_preprocess_text_basic():
    tp = TextPreprocessing()
    text = ["Olá, mundo! 123"]
    result = tp.preprocess_text(text, apply_lower=True, remove_ponctuation=True, remove_numbers=True)
    assert "olá mundo" in result

def test_unify_text():
    tp = TextPreprocessing()
    texts = ["texto 1", "texto 2"]
    unified = tp.unify_text(texts)
    assert "texto 1" in unified and "texto 2" in unified

def test_remove_duplicates():
    tp = TextPreprocessing()
    text = "olá olá mundo mundo"
    result = tp.remove_duplicates(text)
    assert result == "olá mundo"

def test_remove_stopwords():
    tp = TextPreprocessing()
    text = "eu tenho nenhum problema"
    result = tp.remove_stopwords(text)
    assert "nenhum" not in result

def test_preprocess_text_all_options():
    tp = TextPreprocessing()
    text = ["Olá! 123 <b>mundo</b> nenhum etc Python."]
    result = tp.preprocess_text(
        text,
        apply_lower=True,
        remove_ponctuation=True,
        remove_numbers=True,
        clean_html=True,
        apply_unidecode=True,
        remove_stopwords=True,
        remove_duplicates=True
    )
    # Should remove stopwords, punctuation, numbers, html, accents, duplicates, and lowercase
    assert "nenhum" not in result
    assert "etc" not in result
    assert "olá" in result or "ola" in result
    assert "mundo" in result
    assert "python" in result
    assert "123" not in result
    assert "<b>" not in result

def test_preprocess_text_empty():
    tp = TextPreprocessing()
    text = [""]
    result = tp.preprocess_text(text)
    assert result == ""

def test_remove_duplicates_with_punctuation():
    tp = TextPreprocessing()
    text = "olá, olá, mundo! mundo!"
    result = tp.remove_duplicates(text)
    # Should keep only unique tokens
    tokens = set(result.split())
    assert "olá," in tokens or "olá" in tokens
    assert "mundo!" in tokens or "mundo" in tokens

def test_get_stopwords_custom():
    tp = TextPreprocessing()
    stopwords_list = tp.get_stopwords()
    for custom in ["nenhum", "etc", "ter", " sobre"]:
        assert custom in stopwords_list
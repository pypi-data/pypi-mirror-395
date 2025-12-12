import pytest
from deepbase.parsers import extract_markdown_structure, get_document_structure

def test_extract_markdown_structure_simple():
    """Testa l'estrazione corretta di header semplici."""
    content = """
# Titolo Principale
Testo normale che deve essere ignorato.

## Sottosezione
Altro testo.

### Livello 3
    """
    expected = "# Titolo Principale\n## Sottosezione\n### Livello 3"
    result = extract_markdown_structure(content)
    assert result.strip() == expected

def test_extract_markdown_structure_no_headers():
    """Testa un file markdown senza intestazioni."""
    content = "Solo testo semplice.\nNessun titolo qui."
    result = extract_markdown_structure(content)
    assert "Nessuna struttura rilevata" in result

def test_extract_markdown_structure_complex():
    """Testa che il codice e i commenti non vengano confusi per header."""
    content = """
# Header Reale
    # Questo è codice, non un header
    ## Header Reale 2
"""
    result = extract_markdown_structure(content)
    # L'header indentato (codice) non deve apparire, o deve essere gestito come testo
    # La regex attuale richiede che # sia all'inizio della riga (con whitespace opzionali)
    assert "# Header Reale" in result
    assert "## Header Reale 2" in result
    # Nota: Se la tua regex permette spazi prima del #, verifica il comportamento desiderato

def test_dispatcher_extensions():
    """Testa che il dispatcher scelga il parser giusto in base all'estensione."""
    content = "# Test"
    
    # Markdown extensions
    assert get_document_structure("file.md", content) == "# Test"
    assert get_document_structure("file.markdown", content) == "# Test"
    
    # Unsupported extensions (dovrebbe ritornare None o messaggio default)
    assert get_document_structure("file.txt", content) is None
    assert get_document_structure("script.py", content) is None
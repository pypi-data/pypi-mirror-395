# tests/test_cli.py

import os
from typer.testing import CliRunner
from deepbase.main import app

runner = CliRunner()

# ... (gli altri test sulle directory rimangono uguali) ...

def test_cli_single_file_default(tmp_path):
    """
    Testa che di default (senza -a) venga generata SOLO la struttura.
    """
    single_file = tmp_path / "README.md"
    unique_content_string = "Questo è il contenuto univoco del file."
    single_file.write_text(f"# Intro\n{unique_content_string}\n## Usage", encoding="utf-8")
    
    output_file = tmp_path / "structure_only.md"
    
    result = runner.invoke(app, [str(single_file), "-o", str(output_file)])
    
    assert result.exit_code == 0
    content = output_file.read_text(encoding="utf-8")
    
    # DEVE contenere la struttura
    assert "# Intro" in content
    assert "## Usage" in content
    
    # NON DEVE contenere il corpo del testo (perché non abbiamo passato -a)
    # Nota: la regex dei parser estrae solo le linee con #, quindi la stringa di testo puro
    # non dovrebbe apparire nell'output se stiamo stampando solo la structure section.
    assert unique_content_string not in content

def test_cli_single_file_with_all(tmp_path):
    """
    Testa che con il flag --all venga generato ANCHE il contenuto.
    """
    single_file = tmp_path / "DOCS.md"
    unique_content_string = "Dettagli molto importanti."
    single_file.write_text(f"# Title\n{unique_content_string}", encoding="utf-8")
    
    output_file = tmp_path / "full_context.md"
    
    # Passiamo il flag --all
    result = runner.invoke(app, [str(single_file), "--all", "-o", str(output_file)])
    
    assert result.exit_code == 0
    content = output_file.read_text(encoding="utf-8")
    
    # DEVE contenere la struttura
    assert "# Title" in content
    
    # DEVE contenere ANCHE il corpo del testo
    assert "--- START OF FILE: DOCS.md ---" in content
    assert unique_content_string in content
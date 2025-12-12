# src/deepbase/parsers.py

import os
import re
from typing import Optional

def extract_markdown_structure(content: str) -> str:
    """
    Estrae solo le intestazioni (headers) da un contenuto Markdown,
    preservando la gerarchia (#, ##, ###).
    """
    structure_lines = []
    lines = content.splitlines()
    
    # Regex per catturare le righe che iniziano con uno o più '#' seguiti da spazio
    header_pattern = re.compile(r'^\s*(#{1,6})\s+(.*)')
    
    for line in lines:
        match = header_pattern.match(line)
        if match:
            # Opzione 1: Manteniamo il formato Raw Markdown (# Titolo)
            # Questo è ideale per gli LLM perché capiscono nativamente il livello di importanza.
            structure_lines.append(line.strip())
            
            # Opzione 2 (Alternativa): Convertire in lista indentata
            # level = len(match.group(1))
            # indent = "    " * (level - 1)
            # structure_lines.append(f"{indent}- {match.group(2)}")
            
    if not structure_lines:
        return "(Nessuna struttura rilevata o file privo di intestazioni)"
        
    return "\n".join(structure_lines)

def get_document_structure(file_path: str, content: str) -> Optional[str]:
    """
    Funzione dispatcher che decide quale parser usare in base all'estensione.
    Restituisce una stringa formattata con la struttura del documento.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext in ['.md', '.markdown', '.mdown', '.mkd']:
        return extract_markdown_structure(content)
    
    # --- FUTURE IMPLEMENTAZIONI ---
    # elif ext == '.docx':
    #     return extract_docx_structure(file_path) # Richiederà python-docx
    # elif ext == '.tex':
    #     return extract_latex_structure(content)
    
    return None
# src/deepbase/toon.py

import ast
import os
import re
import json

class ToonVisitor(ast.NodeVisitor):
    def __init__(self):
        self.output = []
        self.indent_level = 0

    def _log(self, text):
        indent = "  " * self.indent_level
        self.output.append(f"{indent}{text}")

    def visit_ClassDef(self, node):
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        base_str = f"({', '.join(bases)})" if bases else ""
        self._log(f"C: {node.name}{base_str}")
        
        self.indent_level += 1
        docstring = ast.get_docstring(node)
        if docstring:
            short_doc = docstring.split('\n')[0].strip()
            self._log(f"\"\"\"{short_doc}...\"\"\"")
        
        self.generic_visit(node)
        self.indent_level -= 1

    def visit_FunctionDef(self, node):
        self._handle_function(node)

    def visit_AsyncFunctionDef(self, node):
        self._handle_function(node, is_async=True)

    def _handle_function(self, node, is_async=False):
        args = [arg.arg for arg in node.args.args]
        args_str = ", ".join(args)
        prefix = "async " if is_async else ""
        
        ret_anno = ""
        if node.returns:
            try:
                if isinstance(node.returns, ast.Name):
                    ret_anno = f" -> {node.returns.id}"
                elif isinstance(node.returns, ast.Constant):
                     ret_anno = f" -> {node.returns.value}"
            except:
                pass

        self._log(f"{prefix}F: {node.name}({args_str}){ret_anno}")
        
        docstring = ast.get_docstring(node)
        if docstring:
            self.indent_level += 1
            short_doc = docstring.split('\n')[0].strip()
            self._log(f"\"\"\"{short_doc}...\"\"\"")
            self.indent_level -= 1

    def generic_visit(self, node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                self.visit(child)

# --- Gestori per file Non-Python ---

def _handle_markdown(content: str) -> str:
    """Estrae solo gli header Markdown."""
    lines = []
    for line in content.splitlines():
        if line.strip().startswith("#"):
            lines.append(line.strip())
    if not lines:
        return "(Markdown file with no headers)"
    return "\n".join(lines)

def _handle_toml_ini(content: str) -> str:
    """Estrae sezioni [Title] e chiavi, ignorando valori lunghi."""
    lines = []
    for line in content.splitlines():
        clean = line.strip()
        if not clean or clean.startswith("#"):
            continue
        
        # Mantiene le sezioni [Project]
        if clean.startswith("[") and clean.endswith("]"):
            lines.append(clean)
        # Mantiene le chiavi (key = value), semplificando il valore
        elif "=" in clean:
            key = clean.split("=")[0].strip()
            lines.append(f"{key} = ...")
    return "\n".join(lines)

def _handle_json_structure(content: str) -> str:
    """Prova a parsare JSON e restituire solo le chiavi di primo/secondo livello."""
    try:
        data = json.loads(content)
        if isinstance(data, dict):
            lines = ["{"]
            for k, v in data.items():
                if isinstance(v, dict):
                    lines.append(f"  {k}: {{ ...keys: {list(v.keys())} }}")
                elif isinstance(v, list):
                    lines.append(f"  {k}: [ ...size: {len(v)} ]")
                else:
                    lines.append(f"  {k}: (value)")
            lines.append("}")
            return "\n".join(lines)
        return "(JSON Array or Scalar)"
    except:
        return "(Invalid JSON content)"

def _handle_minified_config(content: str) -> str:
    """Rimuove righe vuote e commenti (per .gitignore, requirements.txt)."""
    lines = []
    for line in content.splitlines():
        clean = line.strip()
        # Ignora righe vuote e commenti
        if clean and not clean.startswith("#"):
            lines.append(clean)
    
    if not lines:
        return "(Empty or comments-only file)"
    return "\n".join(lines)

def generate_toon_representation(file_path: str, content: str) -> str:
    """
    Genera una rappresentazione TOON (Token Oriented) in base al tipo di file.
    """
    _, ext = os.path.splitext(file_path)
    filename = os.path.basename(file_path)
    ext = ext.lower()

    # 1. PYTHON
    if ext == ".py":
        try:
            tree = ast.parse(content)
            visitor = ToonVisitor()
            visitor.visit(tree)
            return "\n".join(visitor.output)
        except SyntaxError:
            return f"(Syntax Error parsing {filename})"
    
    # 2. MARKDOWN (Documentazione)
    elif ext in [".md", ".markdown"]:
        return _handle_markdown(content)

    # 3. CONFIGURAZIONE STRUTTURATA (TOML, INI, CFG)
    elif ext in [".toml", ".ini", ".cfg"]:
        return _handle_toml_ini(content)

    # 4. DATI (JSON)
    elif ext == ".json":
        return _handle_json_structure(content)

    # 5. CONFIGURAZIONE A LISTA (.gitignore, requirements.txt, .env)
    # Lista di file noti per essere liste di regole
    elif ext in [".txt", ".dockerignore", ".gitignore"] or filename in [".gitignore", ".dockerignore", "Dockerfile", "Makefile"]:
        return _handle_minified_config(content)

    # 6. YAML (Struttura semplice basata su indentazione)
    elif ext in [".yml", ".yaml"]:
        # Per YAML facciamo un filtro semplice regex per mostrare solo le chiavi
        lines = [line for line in content.splitlines() if ":" in line and not line.strip().startswith("#")]
        # Semplificazione brutale: mostra solo le chiavi
        clean_lines = []
        for l in lines:
            key = l.split(":")[0]
            clean_lines.append(f"{key}:")
        return "\n".join(clean_lines)

    # 7. DEFAULT: Fallback minificato (o troncato)
    else:
        # Se non conosciamo il file, mostriamo le prime 5 righe minificate come anteprima
        minified = _handle_minified_config(content)
        lines = minified.splitlines()
        if len(lines) > 10:
            return "\n".join(lines[:10]) + f"\n... ({len(lines)-10} more meaningful lines hidden)"
        return minified
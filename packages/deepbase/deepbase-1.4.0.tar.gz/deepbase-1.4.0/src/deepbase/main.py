# src/deepbase/main.py

import os
import typer
import fnmatch  # Necessario per il pattern matching
from rich.console import Console
from rich.progress import Progress
import tomli
import chardet
from typing import List, Dict, Any, Set, Optional

from deepbase.toon import generate_toon_representation
from deepbase.parsers import get_document_structure

# ... (LE CONFIGURAZIONI DEFAULT_CONFIG e HELPER RIMANGONO INVARIATE) ...
# Assicurati di copiare le funzioni: load_config, is_significant_file, 
# generate_directory_tree, get_all_significant_files, read_file_content 
# dalla versione precedente.

DEFAULT_CONFIG = {
    "ignore_dirs": {
        "__pycache__", ".git", ".idea", ".vscode", "venv", ".venv", "env",
        ".env", "node_modules", "build", "dist", "target", "out", "bin",
        "obj", "logs", "tmp", "eggs", ".eggs", ".pytest_cache", ".tox",
        "site", "*.egg-info", "coverage"
    },
    "significant_extensions": {
        ".py", ".java", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss", ".sql", # Aggiunto jsx/tsx
        ".md", ".json", ".xml", ".yml", ".yaml", ".sh", ".bat", "Dockerfile",
        ".dockerignore", ".gitignore", "requirements.txt", "pom.xml", "gradlew",
        "pyproject.toml", "setup.py", "package.json", "tsconfig.json" # Aggiunto package/ts config
    }
}

app = typer.Typer(
    name="deepbase",
    help="Analyzes a project or file and creates a unified context document for an LLM.",
    add_completion=False
)
console = Console()

# ... [INSERISCI QUI LE FUNZIONI HELPER: load_config, generate_directory_tree, etc.] ...
# Per brevità non le ripeto se non sono cambiate, ma devono esserci nel file finale.

def load_config(root_dir: str) -> Dict[str, Any]:
    """Loads configuration from .deepbase.toml if available."""
    config_path = os.path.join(root_dir, ".deepbase.toml")
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, "rb") as f:
                user_config = tomli.load(f)
            config["ignore_dirs"].update(user_config.get("ignore_dirs", []))
            config["significant_extensions"].update(user_config.get("significant_extensions", []))
        except tomli.TOMLDecodeError:
            pass
    return config

def is_significant_file(file_path: str, significant_extensions: Set[str]) -> bool:
    file_name = os.path.basename(file_path)
    if file_name in significant_extensions: return True
    _, ext = os.path.splitext(file_name)
    return ext in significant_extensions

def generate_directory_tree(root_dir: str, config: Dict[str, Any]) -> str:
    tree_str = f"Project Structure in: {os.path.abspath(root_dir)}\n\n"
    ignore_dirs = config["ignore_dirs"]
    significant_exts = config["significant_extensions"]
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        tree_str += f"{indent}📂 {os.path.basename(dirpath) or os.path.basename(os.path.abspath(root_dir))}/\n"
        sub_indent = ' ' * 4 * (level + 1)
        for f in sorted(filenames):
            if is_significant_file(os.path.join(dirpath, f), significant_exts):
                tree_str += f"{sub_indent}📄 {f}\n"
    return tree_str

def get_all_significant_files(root_dir: str, config: Dict[str, Any]) -> List[str]:
    significant_files = []
    ignore_dirs = config["ignore_dirs"]
    significant_exts = config["significant_extensions"]
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith('.')]
        for filename in sorted(filenames):
            file_path = os.path.join(dirpath, filename)
            if is_significant_file(file_path, significant_exts):
                significant_files.append(file_path)
    return significant_files

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, "rb") as fb:
            raw_data = fb.read()
        detection = chardet.detect(raw_data)
        encoding = detection['encoding'] if detection['encoding'] else 'utf-8'
        return raw_data.decode(encoding, errors="replace")
    except Exception as e:
        return f"!!! Error reading file: {e} !!!"


# --- NEW HELPER FOR FOCUS ---
def matches_focus(file_path: str, root_dir: str, focus_patterns: List[str]) -> bool:
    """Check if the file path matches any of the focus patterns."""
    if not focus_patterns:
        return False
    
    # Rendi il path relativo per il matching (es. src/main.py)
    rel_path = os.path.relpath(file_path, root_dir)
    # Supporta anche slash normali su Windows
    rel_path_fwd = rel_path.replace(os.sep, '/')
    
    for pattern in focus_patterns:
        # Se il pattern finisce con /, matchiamo una directory e tutto il contenuto
        clean_pattern = pattern.replace(os.sep, '/')
        
        # Match esatto file, match wildcard o match startswith directory
        if fnmatch.fnmatch(rel_path_fwd, clean_pattern):
            return True
        if clean_pattern in rel_path_fwd: # Match parziale semplice (contiene stringa)
            return True
            
    return False

# --- Legge il file di focus ---
def load_focus_patterns_from_file(file_path: str) -> List[str]:
    """Legge pattern da un file di testo (uno per riga), ignorando # commenti."""
    patterns = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                # Ignora righe vuote o che iniziano con #
                if line and not line.startswith("#"):
                    patterns.append(line)
        except Exception as e:
            console.print(f"[bold yellow]Warning:[/bold yellow] Could not read focus file '{file_path}': {e}")
    else:
        console.print(f"[bold yellow]Warning:[/bold yellow] Focus file '{file_path}' not found.")
    return patterns
# --- MAIN COMMAND ---

@app.command()
def create(
    target: str = typer.Argument(..., help="The file or directory to scan."),
    output: str = typer.Option("llm_context.md", "--output", "-o", help="The output file."),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output."),
    include_all: bool = typer.Option(False, "--all", "-a", help="Include full content of ALL files."),
    toon_mode: bool = typer.Option(False, "--toon", "-t", help="Use 'Skeleton' mode for non-focused files."),
    
    # 1. Focus Flag (Manual)
    focus: Optional[List[str]] = typer.Option(
        None, "--focus", "-f", 
        help="Pattern to focus on. Can be used multiple times."
    ),
    
    # 2. Focus File (File based)
    focus_file: Optional[str] = typer.Option(
        None, "--focus-file", "-ff",
        help="Path to a text file containing a list of focus patterns (one per line)."
    )
):
    """
    Analyzes a directory OR a single file.
    Hybrid workflow with Context Skeleton + Focused Content.
    """
    if not os.path.exists(target):
        console.print(f"[bold red]Error:[/bold red] Target not found: '{target}'")
        raise typer.Exit(code=1)

    # --- LOGICA DI MERGE DEI FOCUS PATTERNS ---
    active_focus_patterns = []
    
    # Aggiungi quelli da CLI
    if focus:
        active_focus_patterns.extend(focus)
    
    # Aggiungi quelli da FILE
    if focus_file:
        file_patterns = load_focus_patterns_from_file(focus_file)
        if file_patterns:
            active_focus_patterns.extend(file_patterns)
            console.print(f"[green]Loaded {len(file_patterns)} patterns from '{focus_file}'[/green]")

    # Pulizia duplicati (opzionale ma utile)
    active_focus_patterns = list(set(active_focus_patterns))

    console.print(f"[bold green]Analyzing '{target}'...[/bold green]")
    
    if toon_mode and active_focus_patterns:
         console.print(f"[yellow]Hybrid Mode active: TOON + Focus on {len(active_focus_patterns)} patterns.[/yellow]")
    elif toon_mode:
        console.print("[yellow]TOON Mode active: Minimalist output.[/yellow]")

    # --- STYLE CONFIGURATION ---
    if toon_mode:
        def fmt_header(title): return f"### {title}\n\n"
        def fmt_file_start(path): return f"> FILE: {path}\n"
        def fmt_file_end(path):   return "\n"
        def fmt_separator():      return "" 
    else:
        def fmt_header(title): 
            line = "="*80 
            return f"{line}\n### {title} ###\n{line}\n\n"
        def fmt_file_start(path): return f"--- START OF FILE: {path} ---\n\n"
        def fmt_file_end(path):   return f"\n\n--- END OF FILE: {path} ---\n"
        def fmt_separator():      return "-" * 40 + "\n\n"

    try:
        with open(output, "w", encoding="utf-8") as outfile:
            
            # CASE 1: SINGLE FILE (Minimally affected)
            if os.path.isfile(target):
                filename = os.path.basename(target)
                outfile.write(f"# File Structure Analysis: {filename}\n\n")
                content = read_file_content(target)
                structure = get_document_structure(target, content)
                outfile.write(fmt_header("DOCUMENT STRUCTURE (Outline)"))
                outfile.write(structure or "N/A")
                outfile.write("\n\n")
                if include_all or toon_mode:
                     section = "SEMANTIC SKELETONS (TOON)" if toon_mode else "FILE CONTENT"
                     outfile.write(fmt_header(section))
                     outfile.write(fmt_file_start(filename))
                     if toon_mode: outfile.write(generate_toon_representation(target, content))
                     else: outfile.write(content)
                     outfile.write(fmt_file_end(filename))

            # CASE 2: DIRECTORY
            elif os.path.isdir(target):
                config = load_config(target)
                outfile.write(f"# Project Context: {os.path.basename(os.path.abspath(target))}\n\n")
                
                # 1. Structure
                outfile.write(fmt_header("PROJECT STRUCTURE"))
                directory_tree = generate_directory_tree(target, config)
                outfile.write(directory_tree)
                outfile.write("\n\n")

                # 2. Content Generation
                # Check based on MERGED active_focus_patterns
                if include_all or toon_mode or active_focus_patterns:
                    
                    section_title = "FILE CONTENTS (HYBRID)" if (toon_mode and active_focus_patterns) else \
                                    ("SEMANTIC SKELETONS (TOON)" if toon_mode else "FILE CONTENTS")
                                    
                    outfile.write(fmt_header(section_title))
                    
                    files = get_all_significant_files(target, config)
                    
                    with Progress(console=console) as progress:
                        task = progress.add_task("[cyan]Processing...", total=len(files))
                        for fpath in files:
                            rel_path = os.path.relpath(fpath, target).replace('\\', '/')
                            
                            # DECISION MATRIX based on active_focus_patterns
                            is_in_focus = active_focus_patterns and matches_focus(fpath, target, active_focus_patterns)
                            
                            should_write_full = include_all or is_in_focus
                            should_write_toon = toon_mode and not should_write_full
                            
                            if not should_write_full and not should_write_toon:
                                progress.update(task, advance=1)
                                continue

                            progress.update(task, advance=1, description=f"[cyan]{rel_path}[/cyan]")
                            
                            marker = ""
                            if is_in_focus and toon_mode: marker = " [FOCUSED - FULL CONTENT]"
                            
                            outfile.write(fmt_file_start(rel_path + marker))
                            content = read_file_content(fpath)
                            
                            if should_write_full:
                                outfile.write(content)
                            elif should_write_toon:
                                outfile.write(generate_toon_representation(fpath, content))
                                
                            outfile.write(fmt_file_end(rel_path))
                            outfile.write(fmt_separator())
                else:
                     console.print("[dim]Note: Only directory tree generated. Use --toon, --all, or --focus to see content.[/dim]")

        console.print(f"\n[bold green]✓ SUCCESS[/bold green]: Context created in [cyan]'{output}'[/cyan]")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
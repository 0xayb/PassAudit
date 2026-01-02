#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.align import Align
from getpass import getpass

from core.checker import PasswordChecker
from core.generator import PasswordGenerator
from core.analyzer import PasswordAnalyzer
from utils.dictionary_loader import load_password_dictionaries
from utils.report_generator import ReportGenerator
from utils.display import DisplayManager

BANNER = r"""
  _____                                _ _ _   
 |  __ \                /\            | (_) |  
 | |__) |_ _ ___ ___   /  \  _   _  __| |_| |_ 
 |  ___/ _` / __/ __| / /\ \| | | |/ _` | | __|
 | |  | (_| \__ \__ \/ ____ \ |_| | (_| | | |_ 
 |_|   \__,_|___/___/_/    \_\__,_|\__,_|_|\__|
                                               
    Password Strength and Breach Detection Tool
            Author: Ayoub SERARFI
"""

app = typer.Typer(help="Professional Password Security Analyzer")
console = Console()
console.print(BANNER, style="bold cyan")
display = DisplayManager()
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

@app.command()
def check(
    password: Optional[str] = typer.Option(
        None,
        "--password",
        "-p",
        help="Password to check (use interactive mode if not provided)"
    ),
    show_password: bool = typer.Option(
        False,
        "--show",
        "-s",
        help="Display password in output (default: masked)"
    ),
    dict_paths: Optional[list[str]] = typer.Option(
        None,
        "--dict",
        "-d",
        help="Additional password dictionary files to check against"
    ),
    export: Optional[str] = typer.Option(
        None,
        "--export",
        "-e",
        help="Export report to file (json or csv)"
    )
):
    
    # Load password dictionaries
    console.print("[dim]Loading password dictionaries...[/dim]")
    default_dicts = [
        DATA_DIR / '10k-most-common.txt',
        DATA_DIR / '10-million-password-list-top-1000000.txt',
        DATA_DIR / '500-worst-passwords.txt'
    ]
    
    extra_dicts = [Path(p) for p in dict_paths] if dict_paths else []
    all_dicts = default_dicts + extra_dicts
    password_hashes = load_password_dictionaries(all_dicts)
    console.print(f"[dim]Loaded {len(password_hashes):,} password hashes[/dim]\n")
    
    # Initialize components
    checker = PasswordChecker(password_hashes)
    analyzer = PasswordAnalyzer()
    
    # Get password
    if password is None:
        try:
            password = getpass("Enter password to check (hidden): ")
        except KeyboardInterrupt:
            console.print("\n[yellow]Cancelled[/yellow]")
            raise typer.Exit()
    
    if not password:
        console.print("[red]Error: Password cannot be empty[/red]")
        raise typer.Exit(code=1)
    
    # Analyze password
    result = analyzer.analyze(password, checker)
    
    # Display report
    display.show_strength_report(result, password, show_password)
    
    # Suggest better password
    console.print("\n[bold]Suggested Strong Password:[/bold]")
    generator = PasswordGenerator()
    suggested = generator.generate_passphrase(entropy=52)
    suggested_result = analyzer.analyze(suggested, checker)
    
    console.print(f"  {suggested}")
    console.print(f"  Strength: [green]{suggested_result['score']}/4[/green]")
    
    # Export if requested
    if export:
        result['suggested_password'] = suggested
        result['suggested_score'] = suggested_result['score']
        report_gen = ReportGenerator()
        report_gen.export(result, export)
        console.print(f"\n[green]✓ Report exported to {export}[/green]")


@app.command()
def generate(
    count: int = typer.Option(
        1,
        "--count",
        "-c",
        help="Number of passwords to generate"
    ),
    entropy: int = typer.Option(
        52,
        "--entropy",
        "-e",
        help="Target entropy in bits (higher = stronger)"
    ),
    style: str = typer.Option(
        "passphrase",
        "--style",
        "-s",
        help="Password style: passphrase, mixed, alphanumeric"
    )
):
    generator = PasswordGenerator()
    display.show_generated_passwords(generator, count, entropy, style)


@app.command()
def batch(
    input_file: str = typer.Argument(..., help="File containing passwords (one per line)"),
    output_file: str = typer.Option(
        "batch_report.csv",
        "--output",
        "-o",
        help="Output report file"
    )
):
    
    # Load dictionaries
    console.print("[dim]Loading password dictionaries...[/dim]")
    default_dicts = [
        DATA_DIR / '10k-most-common.txt',
        DATA_DIR / '10-million-password-list-top-1000000.txt',
        DATA_DIR / '500-worst-passwords.txt'
    ]
    password_hashes = load_password_dictionaries(default_dicts)
    checker = PasswordChecker(password_hashes)
    analyzer = PasswordAnalyzer()
    
    # Read passwords
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {input_file}[/red]")
        raise typer.Exit(code=1)
    
    console.print(f"[dim]Analyzing {len(passwords)} passwords...[/dim]\n")
    
    # Analyze all passwords
    results = []
    for i, pwd in enumerate(passwords, 1):
        result = analyzer.analyze(pwd, checker)
        result['password'] = pwd
        results.append(result)
        
        if i % 100 == 0 or i == len(passwords):
            console.print(f"[dim]Progress: {i}/{len(passwords)}[/dim]", end="\r")
    
    console.print("\n")
    
    # Export and display summary
    report_gen = ReportGenerator()
    report_gen.export_batch(results, output_file)
    display.show_batch_summary(results, len(passwords), output_file)


@app.command()
def info():
    display.show_info()


if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user[/yellow]")
        sys.exit(0)
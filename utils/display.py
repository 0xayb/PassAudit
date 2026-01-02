from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from utils.crypto import calculate_entropy


class DisplayManager:
    
    def __init__(self):
        self.console = Console()
        
        self.strength_colors = {
            0: "red",
            1: "red",
            2: "yellow",
            3: "green",
            4: "bright_green"
        }
        
        self.strength_labels = {
            0: "Very Weak",
            1: "Weak",
            2: "Fair",
            3: "Strong",
            4: "Very Strong"
        }
    
    def show_strength_report(
        self, 
        result: Dict, 
        password: str, 
        show_password: bool = False
    ) -> None:
        score = result['score']
        color = self.strength_colors.get(score, "white")
        label = self.strength_labels.get(score, "Unknown")
        
        # Display password (masked or visible)
        pwd_display = password if show_password else "*" * len(password)
        
        self.console.print(f"\n[bold]Password:[/bold] {pwd_display}")
        self.console.print(f"[bold]Length:[/bold] {len(password)} characters")
        self.console.print(f"[bold]Strength:[/bold] [{color}]{label} ({score}/4)[/{color}]")
        self.console.print(f"[bold]Entropy:[/bold] {result['entropy']:.1f} bits")
        self.console.print(f"[bold]SHA-256 Hash:[/bold] {result['hash'][:16]}...{result['hash'][-16:]}")
        
        # Common password warning
        if result['is_common']:
            self.console.print(
                Panel(
                    "[bold red]⚠ WARNING: This is a commonly used password![/bold red]\n"
                    "It appears in known password breach databases and should not be used.",
                    title="Security Alert",
                    border_style="red"
                )
            )
        
        # Feedback and suggestions
        if result['feedback']:
            self.console.print("\n[bold]Security Recommendations:[/bold]")
            for i, suggestion in enumerate(result['feedback'], 1):
                self.console.print(f"  {i}. {suggestion}")
        
        # Crack time estimate
        if 'crack_times' in result and result['crack_times']:
            self.console.print("\n[bold]Estimated Crack Time (offline attack):[/bold]")
            crack_time = result['crack_times'].get(
                'offline_slow_hashing_1e4_per_second', 
                'Unknown'
            )
            self.console.print(f"  {crack_time}")
        
        # Pattern information
        if result.get('pattern_matches'):
            self.console.print("\n[bold]Detected Patterns:[/bold]")
            for pattern in result['pattern_matches'][:3]:
                pattern_type = pattern.get('pattern', 'unknown')
                token = pattern.get('token', '')
                if token:
                    self.console.print(f"  • {pattern_type}: '{token}'")
    
    def show_generated_passwords(
        self, 
        generator, 
        count: int, 
        entropy: int, 
        style: str
    ) -> None:
        self.console.print(f"\n[bold]Generating {count} strong password(s):[/bold]\n")
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", style="dim", width=4)
        table.add_column("Password", style="green")
        table.add_column("Length", justify="center")
        table.add_column("Entropy", justify="center")
        
        for i in range(count):
            try:
                if style == "passphrase":
                    pwd = generator.generate_passphrase(entropy=entropy)
                elif style == "mixed":
                    pwd = generator.generate_mixed(length=max(16, entropy // 4))
                elif style == "alphanumeric":
                    pwd = generator.generate_alphanumeric(length=max(12, entropy // 5))
                elif style == "pin":
                    pwd = generator.generate_pin(length=max(6, entropy // 3))
                else:
                    self.console.print(f"[red]Unknown style: {style}[/red]")
                    return
                
                # Calculate actual entropy
                actual_entropy = calculate_entropy(pwd)
                
                table.add_row(
                    str(i + 1),
                    pwd,
                    str(len(pwd)),
                    f"{actual_entropy:.1f} bits"
                )
            except Exception as e:
                self.console.print(f"[red]Error generating password: {e}[/red]")
        
        self.console.print(table)
        
        if style == "passphrase":
            self.console.print("\n[dim]Tip: Passphrases are easier to remember than random characters[/dim]")
        elif style == "pin":
            self.console.print("\n[dim]Warning: PINs have low entropy and should only be used where required[/dim]")
    
    def show_batch_summary(
        self, 
        results: List[Dict], 
        total: int, 
        output_file: str
    ) -> None:
        weak_count = sum(1 for r in results if r['score'] < 3)
        common_count = sum(1 for r in results if r['is_common'])
        
        # Calculate average score
        avg_score = sum(r['score'] for r in results) / len(results) if results else 0
        
        self.console.print(Panel(
            f"[bold]Batch Analysis Complete[/bold]\n\n"
            f"Total passwords analyzed: {total}\n"
            f"Average strength score: {avg_score:.1f}/4\n"
            f"Weak passwords (score < 3): {weak_count} ({weak_count/total*100:.1f}%)\n"
            f"Common passwords: {common_count} ({common_count/total*100:.1f}%)\n\n"
            f"Report saved to: {output_file}",
            title="Summary",
            border_style="green"
        ))
    
    def show_info(self) -> None:
        self.console.print(Panel(
            "[bold cyan]PassAudit[/bold cyan]\n\n"
            "A professional tool for analyzing password strength and security.\n\n"
            "[bold]Features:[/bold]\n"
            "• Checks against millions of known compromised passwords\n"
            "• Uses zxcvbn for realistic strength estimation\n"
            "• Generates strong, memorable passphrases using EFF wordlist\n"
            "• Provides detailed security recommendations\n"
            "• Batch processing capabilities\n"
            "• Export reports in JSON/CSV formats\n"
            "• Pattern detection and analysis\n\n"
            "[bold]Security:[/bold]\n"
            "• Passwords are never logged or stored\n"
            "• Dictionary lookups use cryptographic hashes (SHA-256)\n"
            "• Interactive mode hides password input\n"
            "• Uses cryptographically secure random number generator\n\n"
            "[bold]Wordlist:[/bold]\n"
            "• EFF Long Wordlist (7,776 words)\n"
            "• ~12.925 bits of entropy per word\n"
            "• Optimized for memorability and security\n",
            title="About",
            border_style="blue"
        ))
    
    def show_progress(self, message: str) -> None:
        self.console.print(f"[dim]{message}[/dim]")
    
    def show_error(self, message: str) -> None:
        self.console.print(f"[red]Error: {message}[/red]")
    
    def show_success(self, message: str) -> None:
        self.console.print(f"[green]✓ {message}[/green]")
    
    def show_warning(self, message: str) -> None:
        self.console.print(f"[yellow]⚠ {message}[/yellow]")
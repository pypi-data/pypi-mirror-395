"""
Visual Enhancement Utilities for Genuity

Provides beautiful CLI output, progress bars, and informative logging.
"""

import sys
from typing import Optional
from tqdm import tqdm


# Color codes for beautiful terminal output
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner(text: str):
    """Print a beautiful banner."""
    width = max(60, len(text) + 10)
    border = "═" * width
    
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}")
    print(f"╔{border}╗")
    print(f"║{text.center(width)}║")
    print(f"╚{border}╝")
    print(f"{Colors.ENDC}\n")


def print_section(text: str):
    """Print a section header."""
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}▶ {text}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'─' * (len(text) + 2)}{Colors.ENDC}")


def print_success(text: str):
    """Print a success message."""
    print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")


def print_info(text: str):
    """Print an info message."""
    print(f"{Colors.OKCYAN}[INFO] {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print a warning message."""
    print(f"{Colors.WARNING}[WARNING] {text}{Colors.ENDC}")


def print_error(text: str):
    """Print an error message."""
    print(f"{Colors.FAIL}[ERROR] {text}{Colors.ENDC}")



def create_progress_bar(total: int, desc: str = "Processing") -> tqdm:
    """
    Create a beautiful progress bar.
    
    Args:
        total: Total number of items
        desc: Description text
        
    Returns:
        tqdm progress bar
    """
    return tqdm(
        total=total,
        desc=f"{Colors.OKCYAN}{desc}{Colors.ENDC}",
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
        ncols=80,
        colour='cyan'
    )

def print_genuity_banner():
    """Print the Genuity ASCII art banner with welcome message."""
    banner = f"""{Colors.OKCYAN}{Colors.BOLD}
╔═════════════════════════════════════════════════════════════════════╗
║                                                                     ║
║     ██████╗ ███████╗███╗   ██╗██╗   ██╗██╗████████╗██╗   ██╗        ║
║    ██╔════╝ ██╔════╝████╗  ██║██║   ██║██║╚══██╔══╝╚██╗ ██╔╝        ║
║    ██║  ███╗█████╗  ██╔██╗ ██║██║   ██║██║   ██║    ╚████╔╝         ║
║    ██║   ██║██╔══╝  ██║╚██╗██║██║   ██║██║   ██║     ╚██╔╝          ║
║    ╚██████╔╝███████╗██║ ╚████║╚██████╔╝██║   ██║      ██║           ║
║     ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝   ╚═╝      ╚═╝           ║
║                                                                     ║
╚═════════════════════════════════════════════════════════════════════╝
                                                                    
             {Colors.OKGREEN}✨ Synthetic Data Generation Suite ✨{Colors.OKCYAN}                
                                                                    
        {Colors.ENDC}Transform Real Data → Secure Synthetic Datasets{Colors.OKCYAN}          

     {Colors.WARNING}[{Colors.ENDC} Privacy-Preserving {Colors.WARNING}]{Colors.OKCYAN}  {Colors.WARNING}[{Colors.ENDC} Enterprise-Grade {Colors.WARNING}]{Colors.OKCYAN}  {Colors.WARNING}[{Colors.ENDC} AI-Powered {Colors.WARNING}]{Colors.OKCYAN}     

{Colors.ENDC}
    """
    
    try:
        # Try to print with UTF-8 encoding
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        print(banner)
        
        # Welcome message
        print(f"{Colors.OKCYAN}{Colors.BOLD}    Welcome to Genuity - A premium library for synthetic data operations.{Colors.ENDC}\n")
        
        # Version and status info
        print(f"{Colors.OKGREEN}    ⚡ Version 1.0.0{Colors.ENDC} {Colors.OKCYAN}|{Colors.ENDC} {Colors.OKBLUE}Powering Data Innovation{Colors.ENDC} {Colors.OKCYAN}|{Colors.ENDC} {Colors.WARNING}Ready to Generate ✓{Colors.ENDC}\n")
    except (UnicodeEncodeError, AttributeError):
        # Fallback: simpler banner without Unicode box characters
        print(f"{Colors.OKCYAN}{Colors.BOLD}")
        print("=" * 75)
        print("                        G E N U I T Y")
        print("              Synthetic Data Generation Suite")
        print("=" * 75)
        print(f"{Colors.ENDC}")
        print(f"\n    Welcome to Genuity - A premium library for synthetic data operations.")
        print(f"    Transform Real Data → Secure Synthetic Datasets")
        print(f"{Colors.OKGREEN}    Version: 0.1.1 | Enterprise-Grade Synthetic Data\n{Colors.ENDC}")


def print_model_info(model_name: str, config: dict):
    """
    Print model configuration info beautifully.
    
    Args:
        model_name: Name of the model
        config: Configuration dictionary
    """
    print_section(f"{model_name} Configuration")
    
    for key, value in config.items():
        if isinstance(value, bool):
            icon = "✓" if value else "✗"
            color = Colors.OKGREEN if value else Colors.FAIL
            print(f"  {color}{icon}{Colors.ENDC} {key}: {value}")
        else:
            print(f"  {Colors.OKCYAN}•{Colors.ENDC} {key}: {Colors.BOLD}{value}{Colors.ENDC}")
    
    print()


def print_metrics_table(metrics: dict, title: str = "Evaluation Metrics"):
    """
    Print metrics in a beautiful table format.
    
    Args:
        metrics: Dictionary of metric name -> value
        title: Table title
    """
    print_section(title)
    
    # Header
    print(f"  {'Metric':<40} {'Value':>15}")
    print(f"  {'-' * 56}")
    
    # Metrics
    for name, value in metrics.items():
        if isinstance(value, float):
            # Color code based on value
            if value >= 0.8:
                color = Colors.OKGREEN
            elif value >= 0.5:
                color = Colors.WARNING
            else:
                color = Colors.FAIL
            
            print(f"  {name:<40} {color}{value:>15.4f}{Colors.ENDC}")
        else:
            print(f"  {name:<40} {value:>15}")
    
    print()


class ProgressTracker:
    """Track progress of multi-step processes."""
    
    def __init__(self, total_steps: int, title: str = "Progress"):
        self.total_steps = total_steps
        self.current_step = 0
        self.title = title
        
    def step(self, description: str):
        """Move to next step."""
        self.current_step += 1
        percentage = (self.current_step / self.total_steps) * 100
        
        # Create progress bar
        filled = int(percentage / 2)
        bar = "█" * filled + "░" * (50 - filled)
        
        print(f"\r{Colors.OKCYAN}[{bar}] {percentage:.0f}% - {description}{Colors.ENDC}", end='', flush=True)
        
        if self.current_step == self.total_steps:
            print()  # New line when complete
